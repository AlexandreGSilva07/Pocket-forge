#!/usr/bin/env python3
"""Static-only inventory of a public J2ME bulk archive. No JAR code is executed."""
import argparse, collections, csv, hashlib, io, json, pathlib, statistics, sys, zipfile
from datetime import datetime, timezone

MAX_JAR = 12 * 1024 * 1024
MAX_MEMBERS = 100000
API_MARKERS = {
    "MIDP Graphics": b"javax/microedition/lcdui/Graphics",
    "GameCanvas": b"javax/microedition/lcdui/game/GameCanvas",
    "Sprite": b"javax/microedition/lcdui/game/Sprite",
    "TiledLayer": b"javax/microedition/lcdui/game/TiledLayer",
    "Nokia DirectGraphics": b"com/nokia/mid/ui/DirectGraphics",
    "J2ME M3G": b"javax/microedition/m3g/",
    "RMS persistence": b"javax/microedition/rms/RecordStore",
    "MMAPI audio": b"javax/microedition/media/Manager",
    "Bluetooth": b"javax/bluetooth/",
    "FileConnection": b"javax/microedition/io/file/",
    "Float operations": b"java/lang/Float",
    "Thread.sleep": b"java/lang/Thread",
}
EXT_AUDIO = (".mid", ".midi", ".wav", ".mp3", ".amr", ".ott", ".imy")
EXT_BITMAP = (".png", ".gif", ".jpg", ".jpeg", ".bmp")

def guarded_read(z, info, limit=MAX_JAR):
    if info.file_size > limit or info.compress_size > limit:
        raise ValueError("oversized entry")
    if info.compress_size and info.file_size > 300 * info.compress_size and info.file_size > 131072:
        raise ValueError("suspicious compression ratio")
    with z.open(info) as f:
        data = f.read(limit+1)
    if len(data)>limit: raise ValueError("entry exceeded safe limit")
    return data

def read_manifest(j):
    try:
        raw=j.read("META-INF/MANIFEST.MF").decode("latin-1","replace")
        unfolded=raw.replace("\r\n ","").replace("\n ","")
        attrs={}
        for line in unfolded.splitlines():
            if ":" in line:
                k,v=line.split(":",1)
                attrs[k.strip()]=v.strip()
        return attrs
    except (KeyError,RuntimeError,BadZip): return {}

BadZip=zipfile.BadZipFile

def analyze_jar(data, name):
    row={"file":name, "bytes":len(data), "sha256":hashlib.sha256(data).hexdigest(),
         "classes":0,"images":0,"png_indexed":0,"png_truecolor":0,"audio":0,
         "resources_other":0,"total_uncompressed":0,"midp":"","cldc":"","title":"",
         "apis":[], "errors":""}
    with zipfile.ZipFile(io.BytesIO(data)) as jar:
        infos=jar.infolist()
        if len(infos)>2500: raise ValueError("jar has >2500 entries")
        m=read_manifest(jar)
        row["midp"]=m.get("MicroEdition-Profile","")
        row["cldc"]=m.get("MicroEdition-Configuration","")
        row["title"]=m.get("MIDlet-Name","")
        markers=set()
        for info in infos:
            if info.is_dir():continue
            row["total_uncompressed"]+=info.file_size
            fn=info.filename.lower()
            if fn.endswith(".class"):
                row["classes"]+=1
                if info.file_size<=1024*1024:
                    try:
                        binary=guarded_read(jar,info,1024*1024)
                        for label,needle in API_MARKERS.items():
                            if needle in binary:markers.add(label)
                    except Exception: pass
            elif fn.endswith(EXT_BITMAP):
                row["images"]+=1
                if fn.endswith(".png") and info.file_size<=2*1024*1024:
                    try:
                        b=guarded_read(jar,info,2*1024*1024)
                        if b.startswith(b"\x89PNG\r\n\x1a\n") and len(b)>=26:
                            color=b[25]
                            if color==3:row["png_indexed"]+=1
                            elif color in (0,2,4,6):row["png_truecolor"]+=1
                    except Exception:pass
            elif fn.endswith(EXT_AUDIO):row["audio"]+=1
            elif not fn.startswith("meta-inf/"):row["resources_other"]+=1
        row["apis"]=sorted(markers)
    return row

def scan(z, rows, errors, prefix="", level=0):
    infos=z.infolist()
    if len(infos)>MAX_MEMBERS: raise ValueError("too many outer entries")
    for i,info in enumerate(infos):
        if info.is_dir():continue
        fn=info.filename
        low=fn.lower()
        if low.endswith(".jar") or (level<1 and low.endswith(".zip")):
            try:
                raw=guarded_read(z,info)
                if low.endswith(".jar"):
                    rows.append(analyze_jar(raw,prefix+fn))
                else:
                    with zipfile.ZipFile(io.BytesIO(raw)) as nested:
                        scan(nested,rows,errors,prefix+fn+"!/",level+1)
            except Exception as exc:
                errors.append({"file":prefix+fn,"error":str(exc)[:160]})
        if (i+1)%500==0:print("outer entries:",i+1,"JARs:",len(rows),flush=True)

def pct(vals,q):
    if not vals:return 0
    vals=sorted(vals)
    return vals[round((len(vals)-1)*q)]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("archive");parser.add_argument("--out",default="j2me-results")
    args=parser.parse_args()
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    rows=[];errors=[]
    zpath=pathlib.Path(args.archive)
    print("archive",zpath.name,"bytes",zpath.stat().st_size,flush=True)
    with zipfile.ZipFile(zpath) as z:
        outer=len(z.infolist())
        scan(z,rows,errors)
    unique={r["sha256"]:r for r in rows}
    sizes=[r["bytes"] for r in rows]
    api=collections.Counter(label for r in rows for label in r["apis"])
    midp=collections.Counter(r["midp"] or "unknown" for r in rows)
    totals={k:sum(r[k] for r in rows) for k in ("bytes","classes","images","png_indexed","png_truecolor","audio","resources_other")}
    result={"provenance":{"source":"https://archive.org/details/1000_J2ME_Games_Pack","file":zpath.name,"archive_size_bytes":zpath.stat().st_size,"date_utc":datetime.now(timezone.utc).isoformat()},
        "outer_entries":outer,"jar_entries":len(rows),"unique_sha256":len(unique),"duplicates":len(rows)-len(unique),
        "errors_count":len(errors),"errors_sample":errors[:40],"total":totals,
        "jar_bytes":{"min":min(sizes,default=0),"median":int(statistics.median(sizes)) if sizes else 0,"p90":pct(sizes,.90),"max":max(sizes,default=0)},
        "midp_profiles":dict(midp),"api_presence":dict(api),
        "scope":"Static ZIP/classfile inspection only. No original games executed; not a benchmark."}
    (out/"summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    fields=[k for k in rows[0].keys() if k!="apis"]+["apis"] if rows else []
    with (out/"catalog.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:w.writerow({**row,"apis":";".join(row["apis"])})
    md=[
        "# Auditoria estática — coleção de 1.000+ jogos J2ME",
        "",
        f"Fonte: https://archive.org/details/1000_J2ME_Games_Pack",
        f"Arquivo ZIP recebido: **{zpath.stat().st_size:,} bytes**; {outer:,} entradas.",
        f"JARs inspecionados: **{len(rows):,}**; SHA-256 distintos: **{len(unique):,}**; duplicatas exatas: **{len(rows)-len(unique):,}**.",
        f"Falhas de leitura: **{len(errors)}**. Números apurados por programa, não apenas a descrição do acervo.",
        f"Tamanho JAR: mediana **{result['jar_bytes']['median']:,} bytes**, p90 **{result['jar_bytes']['p90']:,} bytes**, máximo **{result['jar_bytes']['max']:,} bytes**.",
        f"Recursos em conjunto: **{totals['classes']:,} classes**, **{totals['images']:,} imagens**, **{totals['png_indexed']:,} PNG paletizados**, **{totals['audio']:,} áudios**.",
        "",
        "## APIs referenciadas",
        "| API | JARs com referência |","|---|---:|",
    ]
    md += [f"| {k} | {v:,} |" for k,v in api.most_common()]
    md += ["","## Perfis MIDP","| Perfil | JARs |","|---|---:|"]
    md += [f"| {k} | {v:,} |" for k,v in midp.most_common()]
    md += ["","## Limitações de interpretação",
        "- Apenas análise estática: nenhum JAR executado, nenhuma medição de FPS, RAM ou consumo de bateria.",
        "- Detecção de API pela presença de símbolos no classfile, que não garante que o método seja usado.",
        "- Arquivos com binários proprietários ficam somente no job temporário; não são redistribuídos.",
        "- O acervo pode conter versões duplicadas ou JARs sem manifesto; deduplicação aqui é exata por SHA-256.",
        "- O formato de imagem declarado por extensão pode omitir imagens sem extensão; PNG indexado detectado por cabeçalho.",
        "- A referência J2ME informa oportunidades de experimentação, não obrigações para jogos HTML5 modernos.",
        "",
        "## Experimentos propostos",
        "1. Benchmark de atlas/spritesheets e batching em WebGL/Canvas vs texturas soltas.",
        "2. Comparar tilemaps em binário e JSON comprimido, incluindo tempo de parse.",
        "3. Comparar PNG paletizado, WebP e AVIF com memória de GPU e qualidade percebida controladas.",
        "4. Isolar rendering 2.5D de software e medir CPU/frame time em dispositivos reais.",
        "5. Reconstruir um jogo original de referência com testes de jogabilidade e orçamento fechado.",
        "",
    ]
    (out/"report.md").write_text("\n".join(md),encoding="utf-8")
    print("FINAL_SUMMARY",json.dumps({k:result[k] for k in ["jar_entries","unique_sha256","duplicates","errors_count","total","jar_bytes","midp_profiles","api_presence"]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
