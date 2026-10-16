#!/usr/bin/env python3
"""PocketForge J2ME batch ledger. Static, reproducible, exactly 100 unique JAR hashes per full batch.
Never execute MIDlet code. Never publish game JAR/JAD or art. Source: Nokia64 1000JavaGames.zip.
"""
import argparse, collections, csv, hashlib, io, json, pathlib, re, sys, zipfile
from audit_j2me_archive import analyze_jar, guarded_read, API_MARKERS

SOURCE_URL = "https://archive.org/download/1000_J2ME_Games_Pack/1000JavaGames.zip"
BATCH_SIZE = 100
IMAGE_EXT = (".png", ".gif", ".jpg", ".jpeg", ".bmp")
AUDIO_EXT = (".mid", ".midi", ".wav", ".mp3", ".amr", ".ott", ".imy")
SYMBOLS = {
    "drawImage": b"drawImage", "drawRegion": b"drawRegion", "drawRGB": b"drawRGB",
    "drawPixels": b"drawPixels", "fillRect": b"fillRect",
    "repaint": b"repaint", "flushGraphics": b"flushGraphics",
    "getResourceAsStream": b"getResourceAsStream", "minimax": b"minimax",
}
def safe_text(s):
    return re.sub(r"[\x00-\x1f\x7f|]", " ", str(s or "")).strip()[:160]

def collect(z, prefix=""):
    result = []
    if len(z.infolist()) > 100000: raise ValueError("archive has excessive entries")
    for info in z.infolist():
        if info.is_dir(): continue
        path = prefix + info.filename
        p = info.filename.lower()
        if p.endswith((".jar",".jad")):
            try:
                if p.endswith(".jad"):
                    if info.file_size > 200000: raise ValueError("huge JAD")
                    raw = guarded_read(z, info, 200000)
                else:
                    raw = guarded_read(z, info)
                result.append((path, raw))
            except Exception as exc:
                result.append((path, exc))
        elif p.endswith(".zip") and prefix.count("!/") < 1:
            try:
                with zipfile.ZipFile(io.BytesIO(guarded_read(z,info))) as nested:
                    result.extend(collect(nested,prefix+info.filename+"!/"))
            except Exception: pass
    return result

def key(path):
    # JAR/JAD filenames are matched exactly by path/stem, ignoring case.
    return path.rsplit(".",1)[0].casefold()

def parse_jad(raw):
    text = raw.decode("latin-1","replace").replace("\r\n ","").replace("\n ","")
    attrs={}
    for line in text.splitlines():
        if ":" in line:
            a,b=line.split(":",1);attrs[a.strip()]=safe_text(b)
    return attrs

def inspect_jar(raw, path):
    row=analyze_jar(raw,path)
    symbols=set(); classes=[]; class_digests=[]
    pixel_bytes=0; png_palette=0; entry_errors=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for info in z.infolist():
            if info.is_dir():continue
            name=info.filename
            if name.lower().endswith(".class"):
                if info.file_size > 1024*1024:continue
                try:
                    b=guarded_read(z,info,1024*1024)
                except Exception as exc:
                    entry_errors.append(safe_text(name+": "+str(exc)))
                    continue
                classes.append(name)
                class_digests.append(hashlib.sha256(b).hexdigest())
                for label,needle in SYMBOLS.items():
                    if needle in b:symbols.add(label)
            if name.lower().endswith(".png") and info.file_size <= 2*1024*1024:
                try:
                    b=guarded_read(z,info,2*1024*1024)
                except Exception as exc:
                    entry_errors.append(safe_text(name+": "+str(exc)))
                    continue
                if b.startswith(b"\x89PNG\r\n\x1a\n") and len(b)>=26:
                    if b[25]==3: png_palette+=1
                    if len(b)>=24:pixel_bytes+=int.from_bytes(b[16:20],"big")*int.from_bytes(b[20:24],"big")*4
    return row, sorted(symbols), classes, class_digests, pixel_bytes, entry_errors

def main():
    a=argparse.ArgumentParser()
    a.add_argument("archive")
    a.add_argument("--batch",type=int,default=1)
    a.add_argument("--out",default="docs/research/batches")
    args=a.parse_args()
    if args.batch<1 or args.batch>1000:raise ValueError("batch must be 1..1000")
    archive=pathlib.Path(args.archive)
    source_hash=hashlib.sha256(archive.read_bytes()).hexdigest()
    with zipfile.ZipFile(archive) as z:
        entries=collect(z)
    jar_sources=sorted(((p,b) for p,b in entries if p.lower().endswith(".jar")),
                       key=lambda t:(t[0].casefold(),t[0]))
    jad_by_path={}
    for path,raw in entries:
        if path.lower().endswith(".jad") and isinstance(raw,bytes):
            jad_by_path.setdefault(key(path),(path,parse_jad(raw)))
    candidates=[]; failures=[]; seen=set()
    for path,raw in jar_sources:
        if isinstance(raw,Exception):
            failures.append((path,safe_text(raw)));continue
        digest=hashlib.sha256(raw).hexdigest()
        if digest in seen:continue
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as test:
                if len(test.infolist())>2500:raise ValueError("too many nested files")
        except Exception as exc:
            failures.append((path,safe_text(exc)));continue
        candidates.append((path,raw,digest))
        seen.add(digest)
    start=(args.batch-1)*BATCH_SIZE
    selected=candidates[start:start+BATCH_SIZE]
    if not selected:raise ValueError(f"batch {args.batch}: corpus has only {len(candidates)} valid unique JARs")
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    batchid=f"{args.batch:03d}"
    records=[];class_groups=collections.defaultdict(list)
    for offset,(path,raw,digest) in enumerate(selected):
        static,symbols,classes,class_digests,rgba_budget,entry_errors=inspect_jar(raw,path)
        jad=jad_by_path.get(key(path))
        jad_path,jad_props = jad if jad else ("",{})
        title=static.get("title") or jad_props.get("MIDlet-Name") or pathlib.PurePosixPath(path).stem
        rec={
            "sequence":start+offset+1, "id":digest[:16], "jar_path":path, "jad_path":jad_path,
            "jar_sha256":digest, "game_title":safe_text(title), "bytes":static["bytes"],
            "classes":static["classes"], "images":static["images"],"png_indexed":static["png_indexed"],
            "audio":static["audio"], "midp":safe_text(static["midp"] or jad_props.get("MicroEdition-Profile")),
            "cldc":safe_text(static["cldc"] or jad_props.get("MicroEdition-Configuration")),
            "api_refs":static["apis"],"method_symbols":symbols,
            "class_names":classes,"estimated_png_rgba_bytes":rgba_budget,
            "jad_available":bool(jad), "entry_errors": entry_errors
        }
        records.append(rec)
        for classhash in class_digests:class_groups[classhash].append(digest[:16])
    shared=sorted(
        [{"class_sha256":h,"file_ids":sorted(set(ids)),"distinct_jars":len(set(ids))}
         for h,ids in class_groups.items() if len(set(ids))>1],
         key=lambda g:(-g["distinct_jars"],g["class_sha256"]))
    apis=collections.Counter(s for r in records for s in r["api_refs"])
    symbols=collections.Counter(s for r in records for s in r["method_symbols"])
    summary={
        "protocol_version":1,"batch":args.batch,"batch_size_expected":BATCH_SIZE,
        "count":len(records),"selection":"First 100 unique valid JAR SHA256 per batch, sorted casefold by complete ZIP path; first occurrence representative",
        "source":SOURCE_URL,"archive_filename":archive.name,"archive_bytes":archive.stat().st_size,
        "archive_sha256":source_hash,"eligible_unique_jars":len(candidates),
        "total_batches":(len(candidates)+99)//100,"excluded_corrupt_count":len(failures),
        "exclusion_examples":failures[:8],
        "jad_matched":sum(r["jad_available"] for r in records),
        "total_classes":sum(r["classes"] for r in records),
        "total_images":sum(r["images"] for r in records),
        "total_indexed_png":sum(r["png_indexed"] for r in records),
        "total_audio":sum(r["audio"] for r in records),
        "total_jar_bytes":sum(r["bytes"] for r in records),
        "jar_entries_with_read_errors":sum(bool(r["entry_errors"]) for r in records),
        "api_references":dict(apis.most_common()),
        "method_symbols":dict(symbols.most_common()),
        "identical_classfile_fingerprints_across_jars":len(shared),
        "shared_class_examples":shared[:15],
        "scope":"Static classfile/resource inspection. No MIDlet execution. No equivalence to 100 unique game titles.",
        "records":records
    }
    with (out/f"{batchid}.json").open("w",encoding="utf-8") as f:
        json.dump(summary,f,ensure_ascii=False,indent=2)
    csv_cols=["sequence","id","jar_path","jad_path","jar_sha256","game_title",
        "bytes","classes","images","png_indexed","audio","midp","cldc","api_refs","method_symbols","jad_available"]
    with (out/f"{batchid}.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=csv_cols);w.writeheader()
        for r in records:
            w.writerow({k:"; ".join(r[k]) if isinstance(r[k],list) else r[k] for k in csv_cols})
    md=[
        f"# PocketForge — auditoria do lote {batchid}",
        "",
        f"**100 arquivos JAR distintos por SHA-256**" if len(records)==100 else f"**{len(records)} arquivos JAR distintos por SHA-256** (lote final)",
        "",
        f"Fonte: [{archive.name}]({SOURCE_URL}) — SHA-256 do ZIP: \`{source_hash}\`.",
        f"Critério de seleção: {summary['selection']}.",
        f"Disponíveis neste corpus: {len(candidates)} JARs binariamente distintos; {summary['total_batches']} lotes.",
        f"Escopo: **inspeção estática por jogo, sem execução**; nenhum arquivo JAR/JAD original redistribuído.",
        "",
        "## Resultados deste lote",
        f"- Classes Java: **{summary['total_classes']}**",
        f"- Imagens: **{summary['total_images']}** (PNG indexados: **{summary['total_indexed_png']}**)",
        f"- Áudios: **{summary['total_audio']}**",
        f"- Metadados JAD correspondentes localizados: **{summary['jad_matched']}/{len(records)}**",
        f"- JARs com entradas internas ilegíveis: **{summary['jar_entries_with_read_errors']}**",
        f"- Classfiles idênticos compartilhados entre JARs: **{len(shared)} fingerprints** (não prova engine compartilhada).",
        "",
        "## Registro de todos os arquivos auditados",
        "",
        "| # | ID SHA-256 | Título | Nome/caminho JAR | Nome/caminho JAD | Classes | Imagens | Bytes |",
        "|---:|---|---|---|---|---:|---:|---:|",
    ]
    for r in records:
        md.append("| {sequence} | \`{id}\` | {game_title} | \`{jar_path}\` | {jad_path} | {classes} | {images} | {bytes} |".format(
            **{**r,"jad_path": "\`"+r["jad_path"]+"\`" if r["jad_path"] else "não encontrado"}))
    md.extend(["","## Indícios de engenharia encontrados",
        "Estes são símbolos e referências de bytecode, **não confirmação de comportamento em runtime**.",
        "",
        "| Referência de API | JARs no lote |","|---|---:|"])
    md.extend(f"| {k} | {v} |" for k,v in apis.most_common())
    md.extend(["","| Método/símbolo | JARs no lote |","|---|---:|"])
    md.extend(f"| {k} | {v} |" for k,v in symbols.most_common())
    md.extend(["","## Relação com o motor PocketForge",
        "O módulo original \`demo/engine/compact.js\` implementa atlas Canvas + mapas tipados/RLE + culling e é integrado ao Lumen Shift.",
        "O ganho de performance e de compressão **ainda não foi medido** frente a uma implementação baseline. Não confundir engenharia original inspirada em padrões com port de código destes JARs.",
        "",
        "## Auditoria reproduzível",
        "\`\`\`bash",
        f"python3 scripts/audit_j2me_batch.py 1000JavaGames.zip --batch {args.batch} --out docs/research/batches",
        "node --test tests/compact_engine.test.cjs",
        "\`\`\`",
        "",
        f"Registros detalhados: [JSON](./{batchid}.json) e [CSV](./{batchid}.csv). Os SHA-256 completos e a lista de nomes das classes estão no JSON.",
        "",
        "## Conclusão e pendências",
        f"- {len(records)} JARs inspecionados de modo reprodutível (tamanho, classes, assets, manifestos, presença de APIs/símbolos).",
        "- Necessário aprofundar a desmontagem de render/AI/loops dos representantes e medir protótipos modernos.",
        "- **Nenhum resultado de FPS/RAM nem teste de jogabilidade pode ser inferido deste inventário.**",
        "",
    ])
    (out/f"{batchid}.md").write_text("\n".join(md),encoding="utf-8")
    registry=out/"registry.json"
    if registry.exists():
        doc=json.loads(registry.read_text(encoding="utf-8"))
    else:
        doc={"source":SOURCE_URL,"archive_sha256":source_hash,"batch_size":BATCH_SIZE,"batches":[]}
    if doc["archive_sha256"]!=source_hash:raise ValueError("ZIP changed: source archive checksum mismatch")
    previous={i for b in doc["batches"] if b["batch"]!=args.batch for i in b["file_ids_sha256"]}
    repeated=previous.intersection(r["jar_sha256"] for r in records)
    if repeated:raise ValueError(f"REPEATED IDs ACROSS BATCHES: {len(repeated)}")
    item={"batch":args.batch,"count":len(records),"record_file":f"{batchid}.json",
          "names_file":f"{batchid}.md","file_ids_sha256":[r["jar_sha256"] for r in records],
          "status":"static_inspected","runtime_reconstructed":False}
    doc["batches"]=[b for b in doc["batches"] if b["batch"]!=args.batch]+[item]
    doc["batches"].sort(key=lambda b:b["batch"])
    doc["total_recorded"]=sum(b["count"] for b in doc["batches"])
    registry.write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8")
    print("BATCH_AUDIT",json.dumps({
        k:summary[k] for k in ("batch","count","eligible_unique_jars","total_batches","jad_matched",
        "total_classes","total_images","total_indexed_png","total_audio","api_references",
        "method_symbols","identical_classfile_fingerprints_across_jars")},ensure_ascii=False))
    print("LEDGER",json.dumps({"batch":args.batch,"first":records[0]["jar_path"],
         "last":records[-1]["jar_path"],"records":len(records),"registry_total":doc["total_recorded"]},ensure_ascii=False))
if __name__=="__main__":main()
