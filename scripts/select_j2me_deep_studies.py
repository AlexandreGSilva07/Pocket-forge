#!/usr/bin/env python3
"""Select research candidates from ALL 1649 audited JARs, without executing them.
100 prioritized + 25 reserves. Evidence is static metadata, not decompilation.
"""
import collections
import csv
import json
import pathlib
import re
import unicodedata

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=ROOT/"docs/research/batches"
DEST=ROOT/"docs/research/deep"
TRACKS={
 "render3d":("3D e rasterização",20,"Identificar algoritmos reais de projeção, buffers, M3G e rasterização em software."),
 "worlds":("Mundos, mapas, sprites",20,"Examinar formatos de mapas, colisão, câmera, atlas e ciclos de animação."),
 "strategy":("IA, regras e estratégia",17,"Analisar busca, heurísticas, regras, simulação e serialização."),
 "assets":("Arte, recursos e animação",16,"Investigar compressão de texturas, spritesheets, efeitos e carregamento."),
 "physics":("Física, corrida e esportes",15,"Investigar movimento, colisão, física simplificada e ritmo de atualização."),
 "compact":("Compactação, áudio e minimalismo",12,"Investigar recursos binários, som e estruturas ultraleves.")
}
# All basenames are search targets, not assumed facts about game behavior.
PINS={
 "render3d":"""3D-Adventure.jar|doom_rpg_kr.jar|Speedchaser3D_6630_6680.jar|GeopodDC3D.jar|3DFerrariExperience.jar|3D Sentry.jar|FreeFlight3D.jar|FormulaGP3D.jar|fastNfourious3D_6630_6680.jar|River Storm 3D.jar|wolf.jar|mdoom.jar|3DAlphaZone.jar|AlphaWing2.NP.jar|Submarine3D.jar|BOMBERMAN3D.jar|3DBalloonRace.jar|Mini Golf Castles 3D From Sumea.jar|PlaymanWinterGames3D_K750I.jar|RacingFeverGT3D.jar|3d_qblast.jar|Xmas_Gifts_3D.jar|3DBoxing.jar|Speedchaser3D_6630_6680.jar""",
 "worlds":"""princepersia_tt.jar|MarioMp2.jar|Lemmings.jar|MetalSlug.jar|ForsakenFortress.jar|sabrewulfmod.jar|Arkanoid_Revenge_of_DOTH_6230i.jar|AtomicBetty-byhizir.jar|Rayman3.jar|PrinceOfPersia.jar|SplinterCell.jar|Warior_Within_kr.jar|LotrTwoTowers.jar|LordoftheRings-TwoTowers.jar|DragonIsland.jar|GalleonDawn.jar|TombRaide1osiriscodex.jar|underworldVampiresNight.jar|DragonFire2Episode1.jar|Scooby-Doo2DarkDungeons.jar|Caveman.jar|PrinceHA.jar|Mad Monkey.jar|MikisWorld.jar""",
 "strategy":"""1XCrossingDice.jar|AncientEmpires.jar|age_kr.jar|anno_1503.jar|ChessBuddy3.jar|StrategyWar-1[1].3.2.jar|BattleOfEmpires.jar|200611230940787945.jar|Chessmaster.jar|NetMobileChess.jar|SoccerManager.jar|5Chess.jar|ChessPuzzle.jar|ChineseChess.jar|SpruceChess.jar|FiveStones.jar|ConcealedChess.jar|KX3D Chess.jar|chessbuddy2.jar|AirTraffic.jar|Age Of Marco Polo Gold.jar""",
 "assets":"""DragonFire2Episode1.jar|WorldFighting.jar|SpeedAddict.jar|AgassiTennis.jar|C2S_ProBaseball__v600_.jar|C2S__Dragon.jar|King_Of_Fighters_M2_K750.jar|MetalSlug.jar|AtomicBetty-byhizir.jar|KamikazeQuest.jar|RacingFeverDeluxe2.jar|SpaceEncounter.jar|PuzzleBobble.jar|5Goldminer.jar|EontheDragon.jar|C2S_Bowling2.jar|Stealth.jar|FreeFlight.jar|StreetSoccer.jar|Dragon_Fire2.jar""",
 "physics":"""Colin McRae 04 (s60).jar|Colin_McRae_Rally_4-N6230.jar|VRally.jar|vrally.jar|RacingFever.jar|AlonsoRacing.jar|beachrally.jar|FarmRacing.jar|Fifa2004.jar|FIFA2005.jar|SensibleSoccer.jar|SpaceTaxiPinball.jar|Icy Pinball.jar|GPPinball.jar|pinbdream.jar|RaymanGolf.jar|Kawai_kart_kr.jar|Stuntman.jar|StreetSoccer.jar|FormulaGP3D.jar|Seve B 3D.jar""",
 "compact":"""SpaceAttack.jar|SpaceTravel.jar|Tetris.jar|SpruceInvaders.jar|Space Impact III.jar|7Zwerge.jar|5Goldminer.jar|DieHard.jar|AbsolutePuzzle1.jar|Tetrisbl.jar|GPPinball.jar|PuzzleBobble.jar|RacingFever2.jar|Space Invaders.jar|1000Words.jar|AAFlak88.jar|SpaceWarrior.jar|AtomicSpaceRocks.jar|PhotoPuzzle.jar|funtetris.jar"""
}
KEYWORDS={
 "render3d":r"3d|doom|quake|wolf|flight|pilot|rally|ferrari|racing|formula|submarine|geopod",
 "worlds":r"prince|rayman|mario|metal|lemming|dungeon|tomb|castle|adventure|splinter|dragon|platform|underworld|caveman",
 "strategy":r"chess|empires?|strategy|anno|war|soccer.?manager|sim|battle|city|tactical|air.?traffic|minimax",
 "assets":r"fighter|fighting|tennis|soccer|dragon|puzzle|racing|impact|saga|fire|combat|bowling|metal",
 "physics":r"racing|rally|soccer|fifa|golf|pinball|tennis|ball|stunt|formula|basket|skater",
 "compact":r"tetris|space|attack|mini|sound|music|puzzle|arcade|invaders|miner|audio|blocks"
}
RARE={"J2ME M3G","TiledLayer","Sprite","GameCanvas"}
AVOID=re.compile(r"strip|adult|xxx|porn|erotic|casino|poker|blackjack|hentai|sexy",re.I)

def norm(s):
 s=unicodedata.normalize("NFKD",s or "").casefold()
 return re.sub("[^a-z0-9]","",s)
def family(r):
 t=norm(r["game_title"])
 if t in ("","game","midlet","mymidletsuite","mymidlet","unnamed"):
  t=norm(pathlib.PurePosixPath(r["jar_path"]).stem)
 for suf in ("masyaka","terjef","nokia","n6230","k750i","k700","s60","s40","kr","uk"):
  if t.endswith(suf) and len(t)>len(suf)+5:t=t[:-len(suf)]
 return t
def score(r,g):
 title=r["game_title"]+" "+pathlib.PurePosixPath(r["jar_path"]).stem
 a=set(r["api_refs"]);m=set(r["method_symbols"]);size=r["bytes"]
 n=r["classes"];img=r["images"];aud=r["audio"]
 s=(22 if re.search(KEYWORDS[g],title,re.I) else 0)+(4 if r["jad_available"] else 0)
 if r.get("entry_errors"):s-=75
 if AVOID.search(title):s-=100
 if g=="render3d":s+=48*("J2ME M3G" in a)+22*("drawPixels" in m)+9*("drawRegion" in m)+min(n,28)*.3
 if g=="worlds":s+=42*("TiledLayer" in a)+20*("Sprite" in a)+14*("drawRegion" in m)+min(img,90)*.17
 if g=="strategy":s+=95*("minimax" in m)+min(n,45)*.8+9*("RMS persistence" in a)+9*("drawPixels" in m)
 if g=="assets":s+=min(img,180)*.55+min(aud,40)*.55+15*("Sprite" in a)+8*("GameCanvas" in a)
 if g=="physics":s+=18*("GameCanvas" in a)+16*("Sprite" in a)+min(n,40)*.44+min(img,80)*.16+10*("drawPixels" in m)
 if g=="compact":s+=min(aud,30)*2.1+(25 if size<27000 else 12 if size<55000 else 0)+min(n,20)*.3+12*("MMAPI audio" in a)
 return round(s+(7 if 20000<=size<=220000 else 0),2)
def investigation_targets(r,g):
 a=set(r["api_refs"]);m=set(r["method_symbols"]);q=[]
 if "J2ME M3G" in a:q.append("Verificar se usa cenas, modelos, transformações e animações M3G; medir custo da representação.")
 if "drawPixels" in m:q.append("Desmontar chamadas drawPixels e decidir se são efeitos, blit ou render de software.")
 if "drawRegion" in m:q.append("Identificar retângulos de atlas, pivôs e extração de frames por região.")
 if "TiledLayer" in a:q.append("Investigar layout/colisão de tilemaps e formato dos dados de nível.")
 if "Sprite" in a:q.append("Examinar estados, frames, colisão e composição de sprites.")
 if "minimax" in m:q.append("Reconstituir minimax: avaliação, profundidade e possível poda.")
 if r["images"]>=50:q.append("Catalogar atlas, recursos gráficos e quantização; quantificar custo descompactado.")
 if r["audio"]>=8:q.append("Identificar formatos de áudio, política de disparos e armazenamento.")
 if r["classes"]<=4:q.append("Examinar como lógica e recursos são representados com poucas classes.")
 if r["bytes"]<30000:q.append("Auditar distribuição dos bytes entre lógica e recursos, inclusive formatos binários.")
 if not q:q.append(TRACKS[g][2]+" Confirmar a hipótese com classes e métodos reais.")
 return q

def read_all():
 ledger=json.loads((SOURCE/"registry.json").read_text(encoding="utf-8"))
 assert ledger["total_recorded"]==1649 and len(ledger["batches"])==17
 rows=[]
 for i,b in enumerate(ledger["batches"],1):
  assert b["batch"]==i
  obj=json.loads((SOURCE/(f"{i:03d}.json")).read_text(encoding="utf-8"))
  assert [r["jar_sha256"] for r in obj["records"]]==b["file_ids_sha256"]
  for r in obj["records"]:
   r["batch"]=i;r["family"]=family(r);rows.append(r)
 assert len(rows)==len(set(r["jar_sha256"] for r in rows))==1649
 return rows,ledger
def main():
 rows,ledger=read_all()
 index=collections.defaultdict(list)
 for r in rows:index[pathlib.PurePosixPath(r["jar_path"]).name.casefold()].append(r)
 primary=[];reserves=[];ids=set();families=set();batch_counts=collections.Counter();missing=[]
 def put(r,g,primary_status,manual):
  if r["jar_sha256"] in ids or r["family"] in families or r.get("entry_errors"):return False
  if AVOID.search(r["game_title"]+" "+r["jar_path"]):return False
  dest=primary if primary_status else reserves
  item={k:r.get(k) for k in ("jar_sha256","jar_path","jad_path","game_title","batch","bytes","classes","images","audio","png_indexed","api_refs","method_symbols","class_names","estimated_png_rgba_bytes")}
  item.update({"rank":len(dest)+1,"tier":"principal" if primary_status else "reserva","track":g,
               "track_name":TRACKS[g][0],"study_question":TRACKS[g][2],
               "id":r["jar_sha256"][:16],"score_metadata":score(r,g),
               "selection_basis":"âncora verificada" if manual else "pontuação estrutural",
               "status":"selected_not_decompiled",
               "investigation_targets":investigation_targets(r,g)})
  dest.append(item);ids.add(r["jar_sha256"]);families.add(r["family"]);batch_counts[r["batch"]]+=1
  return True
 anchors={}
 for g,names in PINS.items():
  found=[]
  for name in names.split("|"):
   opts=index.get(name.casefold(),[])
   if not opts:missing.append({"track":g,"basename":name});continue
   best=max(opts,key=lambda r:(score(r,g),bool(r["jad_path"]),-r["bytes"]))
   found.append(best)
  anchors[g]=found
 for g,(_,quota,_) in TRACKS.items():
  begin=len(primary)
  for r in anchors[g]:
   if len(primary)-begin>=quota:break
   put(r,g,True,True)
  others=sorted(rows,key=lambda r:(-score(r,g)-min(16,28/(1+batch_counts[r["batch"]])),r["bytes"],r["jar_sha256"]))
  for r in others:
   if len(primary)-begin>=quota:break
   put(r,g,True,False)
  assert len(primary)-begin==quota,(g,len(primary)-begin)
 assert len(primary)==100
 for g,found in anchors.items():
  for r in found:
   if len(reserves)>=25:break
   put(r,g,False,True)
 if len(reserves)<25:
  more=sorted([(score(r,g),r,g) for r in rows for g in TRACKS],key=lambda x:(-x[0],x[1]["jar_sha256"]))
  for _,r,g in more:
   if len(reserves)>=25:break
   put(r,g,False,False)
 assert len(reserves)==25 and len(ids)==125
 stats={"principal":len(primary),"reserva":len(reserves),
        "por_frente":dict(collections.Counter(r["track"] for r in primary)),
        "por_lote":dict(sorted(collections.Counter(r["batch"] for r in primary).items())),
        "api_raras":dict(collections.Counter(a for r in primary for a in r["api_refs"] if a in RARE)),
        "com_jad":sum(bool(r["jad_path"]) for r in primary),
        "ancoras_verificadas":sum(r["selection_basis"]=="âncora verificada" for r in primary),
        "âncoras_não_encontradas":missing}
 control=index.get("jbenchmark3d.jar",[])
 technical_controls=[{"jar_sha256":x["jar_sha256"],"jar_path":x["jar_path"],"purpose":"Benchmark M3G, não jogo: controle técnico separado das 100 vagas."} for x in control[:1]]
 output={"schema_version":1,"status":"seleção_sem_descompilação","source_zip_sha256":ledger["archive_sha256"],
         "source":"17 arquivos JSON sintéticos versionados","statistics":stats,"principal":primary,"reserva":reserves,"technical_controls_not_games":technical_controls,
         "limitations":"Títulos, APIs, símbolos, quantidades e classes são indícios, não prova de comportamento nem qualidade"}
 DEST.mkdir(parents=True,exist_ok=True)
 (DEST/"selection-100.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 fields=["tier","rank","track_name","batch","id","jar_sha256","game_title","jar_path","jad_path",
         "bytes","classes","images","audio","png_indexed","score_metadata","selection_basis","status"]
 with (DEST/"selection-100.csv").open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in primary+reserves:w.writerow({k:r.get(k,"") for k in fields})
 q=chr(96)
 md=["# PocketForge — 100 jogos prioritários para engenharia reversa completa (+25 reservas)","",
    "> Seleção baseada nos 17 inventários, ainda SEM decompilar ou executar os JARs nesta fase. Gênero e técnica são hipóteses a verificar.","",
    "## Método e limites","",
    "- Foram lidos e confrontados os 17 JSONs (1.649 SHA-256 distintos) com o ledger.",
    "- Preferência por exemplos âncora com metadados já examinados; complementação por pontuação estrutural verificável.",
    "- Cotas temáticas garantem diversidade; normalização de títulos limita variantes aparentemente repetidas.",
    "- O escore mede potencial investigativo, NÃO qualidade ou eficiência confirmada.",
    "- JAD não encontrado significa ausência de descritor com nome/caminho correspondente; não inventar.",
    "- Nenhum JAR, código proprietário ou asset original é incluído.",
    "- JBenchmark3D é uma ferramenta de benchmark, não um jogo: fica apenas como controle técnico fora das 100 vagas.",
    "",f"Selecionados: {len(primary)} principais + {len(reserves)} reservas; "+str(stats["ancoras_verificadas"])+" âncoras verificadas; "+str(stats["com_jad"])+" principais com JAD associado.",
    "","## Frentes e metas de pesquisa","",
    "| Área | Vagas | Investigação real planejada |","|---|---:|---|"]
 for g,(name,quota,question) in TRACKS.items():
  md.append(f"| {name} | {quota} | {question} |")
 md+=["","## 100 candidatos principais","","| # | Área | Arquivo JAR exato | ID SHA-256 | Classes | Imagens | Áudio | Referências discriminantes |",
      "|---:|---|---|---|---:|---:|---:|---|"]
 def safe(s):return str(s).replace("|","/").replace("\n"," ").replace("\r"," ")
 for r in primary:
  sig=", ".join([s for s in r["api_refs"] if s in RARE]+[s for s in r["method_symbols"] if s in ("drawPixels","drawRegion","drawRGB","minimax")]) or "estrutura e assets"
  path="/".join(r["jar_path"].split("/")[-2:])
  md.append(f'| {r["rank"]} | {r["track_name"]} | {q}{safe(path)}{q} | {q}{r["id"]}{q} | {r["classes"]} | {r["images"]} | {r["audio"]} | {safe(sig)} |')
 md+=["","## 25 reservas","","| # | Área | Arquivo JAR exato | SHA prefixo | Classes | Imagens |",
      "|---:|---|---|---|---:|---:|"]
 for r in reserves:
  path="/".join(r["jar_path"].split("/")[-2:])
  md.append(f'| {r["rank"]} | {r["track_name"]} | {q}{safe(path)}{q} | {q}{r["id"]}{q} | {r["classes"]} | {r["images"]} |')
 md+=["","## Protocolo para investigar, não apenas catalogar","",
      "1. Confirmar nome, hash, MIDP, JAD e capacidade de emulação de cada exemplar.",
      "2. Analisar bytecode real de classes e métodos, distinguindo APIs referenciadas de chamadas que ocorrem em runtime.",
      "3. Detectar famílias de motores por semelhança de classfiles, recursos e código; trocar variantes redundantes por reservas documentadas.",
      "4. Reconstruir pseudocódigo autoral de algoritmos e explicar invariantes, estruturas de dados e limites.",
      "5. Executar o original em emulador quando possível, registrar comportamento observado e contradições com hipóteses.",
      "6. Selecionar os padrões realmente úteis à web moderna, desenvolver módulos autorais do PocketForge e integrá-los em jogo de referência.",
      "7. Testar e fazer benchmarks comparativos antes de qualquer alegação de aumento de FPS, economia de RAM ou tamanho.",
      "",
      "## Arquivos e continuidade","",
      "- selection-100.json contém 125 SHA-256 completos, nomes, caminhos JAR/JAD e perguntas técnicas individualizadas por candidato.",
      "- selection-100.csv permite filtrar por frente, tamanho, origem e prioridade.",
      "- A situação atual da engenharia reversa profunda permanece registrada em deep/registry.json: nenhum jogo promovido automaticamente.",
      "- Script reprodutível: scripts/select_j2me_deep_studies.py.",
      "- Testar candidaturas com amostras e revisar as reservas antes de iniciar engenharia completa do corpus selecionado."]
 (DEST/"selection-100.md").write_text("\n".join(md)+"\n",encoding="utf-8")
 print("SELECTION",json.dumps(stats,ensure_ascii=False),flush=True)
 print("FIRST_20",json.dumps([{"name":r["game_title"],"jar":r["jar_path"],"area":r["track"]} for r in primary[:20]],ensure_ascii=False),flush=True)
if __name__=="__main__":main()
