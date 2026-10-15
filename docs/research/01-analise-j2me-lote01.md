# Pesquisa PocketForge — lote 01: dez jogos J2ME

> **Estado:** análise estática de **10 JARs** enviados pelo usuário em 15/10/2026. **Não representa análise de 1.000 jogos, não inclui execução, nem é benchmark de FPS/RAM.** Os binários e assets originais não são publicados neste repositório.

## Objetivo e método

Investigar como jogos antigos atingiam qualidade visual e variedade de mecânicas em dispositivos limitados, e testar quais estratégias continuam úteis na criação de **jogos modernos ultraleves**. PocketForge não precisa usar Java nem reproduzir estética nostálgica.

Os arquivos foram abertos como contêineres ZIP, sem execução de classes. Foram examinados: manifestos MIDlet, arquivos internos, bytes comprimidos, PNGs por assinatura e dimensões, classfiles e referências a APIs/métodos no constant pool. Também houve desmontagem estática com `javap -c -p` do classfile de renderização de `3D-Adventure.jar`. Presença de API **não implica uso frequente em runtime**. Todos os tamanhos são dos arquivos fornecidos, não consumo de RAM.

### Inventário do lote

| JAR | KiB | Classes | PNG | BIN/outros | MIDI | Observação |
|---|---:|---:|---:|---:|---:|---|
| 1000Words | 178,9 | 5 | 1 | 5 | 0 | Recursos numerados sem extensão, lógica concentrada |
| 1XCrossingDice | 43,6 | 25 | 23 | 0 | 0 | `GameModel`, `MinimaxRobot`, regiões e controlador |
| 2020SpecialOps | 65,0 | 16 | 18 | 0 | 2 | Tiles e personagens empacotados em spritesheets |
| 2X2 | 33,1 | 4 | 4 | 0 | 0 | Jogo compacto com sheet 97×84 |
| 3D-Adventure | 19,9 | 2 | 5 | 0 | 0 | Rasterização de software e DirectGraphics |
| 3DBalloonRace | 115,1 | 11 | 5 | 9 | 0 | Recursos mistos e polígonos personalizados |
| 5Chess | 22,5 | 6 | 3 | 0 | 0 | Regras e desenho convencional |
| 5Goldminer | 46,0 | 9 | 19 | 0 | 0 | Tiles individuais 12×12 e atlas 120×64 |
| 7Zwerge | 114,9 | 10 | 15 | 27 | 8 | Mapas `lvnmNN.bin`, sets gráficos e MIDI |
| AAFlak88 | 37,6 | 7 | 21 | 6 | 0 | Animações em sheets verticais e sons OTT |

**Total:** 692.809 bytes (~676,6 KiB), 95 classes, 114 PNG, 47 binários não classificados e 10 MIDI. **107/114 PNG** são imagens indexadas por paleta; quatro RGB, duas RGBA, uma LA. Apenas um dos dez manifestos declara MIDP 2.0; os demais, MIDP 1.0.

### Observações verificáveis

- **8/10** referenciam `javax.microedition.rms.RecordStore`: persistência simples.
- **10/10** referenciam `Graphics.drawImage`: caminho de desenho com bitmap.
- **3/10** referenciam Nokia `DirectGraphics`: 1000Words, 3D-Adventure, 3DBalloonRace.
- **9/10** referenciam `Thread.sleep`; estratégia efetiva de frame pacing requer análise adicional.
- Nenhuma classe analisada referencia `javax.microedition.m3g` nem `javax.microedition.lcdui.game`. Ausência de referências **não prova** ausência de rendering 3D próprio.
- `3D-Adventure` possui um classfile principal com ~33 KiB de atributos Code. A desmontagem apresenta aritmética inteira, buffers e chamadas `DirectGraphics.drawPixels`, sem operações float/double identificadas nos métodos desmontados. **Hipótese a validar:** rasterização especializada com operações inteiras.
- `1XCrossingDice` possui `MinimaxRobot.minimaxValue` e componentes nomeados; demonstra que modularidade e código enxuto podem coexistir.
- `7Zwerge` armazena diversos níveis em binário (`lvnm*.bin`, frequentemente de tamanho descompactado idêntico), diferenciando conteúdo de código.
- `3DBalloonRace` inclui PNGs detectados pela assinatura mesmo sem extensão `.png`.

## Hipóteses para experimentar no PocketForge

| Ordem | Princípio | Técnica moderna candidata | Experimento obrigatório |
|---|---|---|---|
| P0 | Reuso gráfico | atlas + draw regions + batching | Bytes, chamadas draw e custo de textura vs arquivos soltos |
| P0 | Fases como dados | mapas RLE/delta/TypedArray, compactação | Tamanho, decode e edição vs JSON |
| P0 | Raster especializado | Canvas ImageData, raycasting, WebGL shaders pequenos | FPS/energia/memória reais vs render geral |
| P0 | Controle de paletas | PNG indexado, quantização, WebP/AVIF | Transferência vs expansão de RGBA em RAM |
| P1 | Áudio de baixa memória | síntese procedural, trilhas de eventos | Qualidade auditiva, tamanho, latência |
| P1 | IA limitada por orçamento | minimax com cutoff/nós máximos | Latência no dispositivo-alvo |
| P1 | Carregamento por ID | pacotes binários versionados + demand loading | Primeira interação, custo de parsing, cache |
| P1 | Persistência de baixo custo | snapshots versionados | Durabilidade, bytes e overhead |

**Atenção:** formatos antigos podem ser piores que soluções modernas. `fixed point`, por exemplo, deve vencer uma comparação em runtime moderno antes de entrar como regra. PNG indexado economiza transferência, mas frequentemente vira RGBA na GPU. MIDI/OTT não são formatos de saída obrigatórios. **Melhorar eficiência não significa copiar limitações.**

## Metodologia para o acervo maior

1. **Ingestão segura:** número de arquivos, tamanhos, checksums, limites contra ZIP bombs. Deduplicação por SHA-256 e fingerprints de classes.
2. **Taxonomia técnica:** MIDP, fabricante, APIs de desenho, 2D/2.5D/3D, formatos de mapas, render por tiles, som, persistência, assets.
3. **Clusterização por engine:** agrupar classes comuns e detectar reutilização entre vários jogos para evitar retrabalho.
4. **Estudos aprofundados:** selecionar representantes de famílias distintas, decompilar rotinas específicas e reconstruir seu comportamento com testes.
5. **Contraprovas modernas:** construir protótipos próprios equivalentes; medir tamanho, carregamento, frame time, memória, fidelidade e qualidade visual.
6. **Reescrever somente com evidência:** alterar as regras operacionais de `SKILL.md`, mecanismos de assets e testes, scripts, receitas e benchmarks após experimentos comparáveis.

## Status e o que ainda não foi feito

| Atividade | Estado |
|---|---|
| Abrir, classificar e inventariar 10 JARs | Feito |
| Inspecionar classfiles e símbolos Java | Feito |
| Desmontar estaticamente parte de 3D-Adventure | Feito |
| Jogar ou emular os 10 títulos | Não realizado |
| Reconstituir algoritmos completos de todos | Não realizado |
| Analisar corpus de 1.000 JARs | Não realizado — ainda não recebidos |
| Medir FPS, RAM, energia e fidelidade | Não realizado |
| Reescrever a super-skill com provas comparativas | Pendente |

**Licenças e direitos:** não redistribuir JARs, imagens, áudio ou código decompilado dos jogos comerciais. Esta pesquisa apresenta apenas metadados, estrutura e hipóteses de engenharia, a serem implementadas originalmente.

**Próxima decisão:** esperar corpus adicional e ampliar evidência antes de substituir os pilares da skill. A arquitetura v0.1 permanece funcional e não deve ser descartada sem motivo técnico.
