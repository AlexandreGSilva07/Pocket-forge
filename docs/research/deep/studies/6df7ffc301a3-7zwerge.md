# Estudo dirigido de bytecode — 7 Zwerge

**JAR SHA-256:** `6df7ffc301a3524aa0935ac23311d9e132ce4c1dbf81129e5485052afc0828f2`

**Status:** `METHOD_REVIEW_PARTIAL` — métodos reais desmontados/interpretados, **não** jogo inteiro plenamente compreendido, portado ou executado. Ferramenta: OpenJDK 21 `javap -c -p` sobre binários originais enviados em conversa; recursos ZIP lidos sem executar MIDlets. Data: 15/10/2026.

### Evidência de bytecode e recursos reais

- SHA-256 do JAR original enviado: `6df7ffc301a3524aa0935ac23311d9e132ce4c1dbf81129e5485052afc0828f2`.
- `javap -classpath 7Zwerge.jar -c -p e`, método `e.a(String,int,int)` (retorna boolean): monta recurso `"/" + nome + ".bin"`, usa `Class.getResourceAsStream` e lê quatro bytes iniciais (largura, altura e duas dimensões de tile), seguidos por um byte de modo; aloca `width*height` células.
- No modo de **1 byte**, usa um `byte[]` por célula; no de **2 bytes**, um `short[]` e compõe valores **little-endian** usando o byte baixo e o byte alto deslocado oito bits. Um byte extra indica uma camada opcional de dados.
- Arquivos físicos inspecionados: `botlay00.bin` = **1.116 bytes** (37×30×1 + 6), `lvnm00.bin` = **2.226 bytes** (37×30×2 + 6, camada extra desativada), `lvnm01.bin` = **3.336 bytes** (37×30×3 + 6, camada extra ativada).
- Cabeçalhos reais `lvnm00.bin` e `lvnm01.bin`: `25 1e 10 10 02` (hex): largura 37, altura 30, tile 16×16, modo 2; no deslocamento **2225**, a flag vale 0 em `lvnm00` e 1 em `lvnm01`.
- O ZIP contém **21** mapas numerados `lvnm00.bin` a `lvnm20.bin` e **8 trilhas MIDI**. O jogo tem 10 classes de bytecode.
- `i.a(String)` é um segundo leitor de recursos que monta `"/"+nome+".bin"` e lê tamanho e dados para imagens; ainda precisa ser ligado a uma chamada exata do sistema de levels.
- `c` referencia `javax.microedition.media.Manager.createPlayer(InputStream,String)`, evidenciando uma via de áudio por streaming de recurso.

### Contribuição ao PocketForge

Criado `demo/engine/tilepack.js`: decoder de mapas binários no formato observado (1/2 bytes e camada opcional), com validações de dimensões/truncamento; **também** um codec original `PFL v1` com cabeçalho versionado para novos jogos. O Lumen Shift integra encode/decode deste codec próprio. Testes `tests/tilepack_engine.test.cjs` cobrem casos sintéticos de 37×30 e corrupção.

### Limites

O leitor de bytes foi interpretado a partir do bytecode e cruzado com cabeçalhos/tamanhos de recursos do JAR, mas ainda não executamos o jogo original nem validamos visualmente mapas reais. Os arquivos binários do jogo **não** foram publicados. Não foi demonstrado ganho de tamanho do novo codec face ao RLE ou ao ZIP. Testes de variantes e benchmarks são pendentes.
