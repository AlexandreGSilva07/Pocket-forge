# Continuidade entre conversas — PocketForge

## Estado canônico — 15/10/2026 (Cuiabá)

**A AUDITORIA SINTÉTICA FOI FINALIZADA. NÃO REPETIR OS 17 LOTES.**

- Corpus: 2.309 JARs processáveis no inventário inicial, contendo 1.649 SHA-256 distintos e 660 duplicatas exatas.
- Os 1.649 JARs distintos foram classificados em 17 lotes: 001–016 com 100 arquivos; 017 com 49.
- **Todos os PRs #1–#17 estão integrados à branch `main`**.
- Fonte de verdade: [registry.json](batches/registry.json), com todos os hashes SHA-256 completos, uma entrada por arquivo JAR.
- [Relatório de encerramento e índice de todos os 17 lotes](STATIC_COMPLETE.md).
- **A fase seguinte é ENGENHARIA REVERSA DETALHADA**, não gerar novas cópias da auditoria sintética. O controle de progresso fica em [deep/registry.json](deep/registry.json), inicialmente sem estudos concluídos.

## Hierarquia de fontes (não confiar na memória do chat)

1. Ler `AGENTS.md` e `SKILL.md` na raiz.
2. Ler `docs/research/STATIC_COMPLETE.md`, **`docs/research/batches/registry.json`** e relatórios por lote.
3. Verificar PRs #1–#17, evidências de execução e testes no GitHub Actions.
4. Abrir a implementação real em `demo/engine/compact.js`, `demo/engine/state.js` e `demo/engine/audio.js` e a integração em `demo/game.js`.
5. Usar documentação de arquitetura, render, áudio, QA e benchmarks em `docs/INDEX.md`.

## O que exatamente foi auditado

Para cada JAR existe `NNN.json`, `NNN.md` e `NNN.csv`: caminho/nome do JAR, título do manifesto, SHA-256 completo, caminho JAD se existir, números de classes/imagens/áudio, algumas referências e símbolos de bytecode e, quando necessário, registro de falhas parciais. **Não são dumps completos de classes nem reconstruções de algoritmos.**

O total agregado é 19.753 classes, 31.711 imagens, 27.410 PNGs indexados, 2.826 áudios e 648 JADs encontrados por correspondência de caminho/identificador. O lote 014 registra um arquivo parcialmente ilegível (Passaparola.jar). Não inferir conteúdo compreendido com a mera contagem.

## Escala de evidências

| Estado | Significado e prova mínima |
| --- | --- |
| `STATIC_INSPECTED` | JAR indexado com hash/metadata/recursos, sem execução (todos os 1.649) |
| `DECOMPILED_REVIEWED` | Métodos e lógica interpretados, pseudocódigo próprio e evidências precisas |
| `ORIGINAL_BEHAVIOR_VERIFIED` | Jogo original executado em ambiente compatível; cenas/mecânicas observadas |
| `ENGINE_IMPLEMENTED` | Módulo original da skill desenvolvido e realmente usado em demo |
| `ENGINE_TESTED` | Testes relevantes demonstrados: funções, game loop, UI, regressões no browser |
| `BENCHMARKED` | Medições reproduzíveis frente a baseline: carga, memória, FPS e tamanho |

Não mudar automaticamente o estado de nenhum jogo para as etapas detalhadas. Nomes de métodos presentes no classfile não demonstram como os métodos funcionam. Os três módulos existentes são **implementações próprias inspiradas por indícios**, e não ports reconstruídos dos 300 primeiros jogos.

## Lista de aprofundamento já escolhida

A lista de **100 jogos prioritários + 25 reservas** está em [deep/selection-100.md](deep/selection-100.md), com IDs completos, metadados e perguntas individuais em [deep/selection-100.json](deep/selection-100.json). Foi obtida dos 17 lotes, sem executar/descompilar os jogos; o benchmark JBenchmark3D é controle auxiliar, não jogo selecionado. O progresso real fica em [deep/registry.json](deep/registry.json), sem estudos concluídos ainda. O novo agente deve **começar pelas amostras prioritárias**, não repetir seleção nem inventário.

## Próxima etapa: auditoria detalhada completa

1. Reutilizar a ordem/IDs do ledger; criar rastreador adicional de análise detalhada sem apagar o registro original.
2. Analisar algoritmos reais: loops de renderização, tiles/atlases, pipeline de assets, física, controle, IA, fases, serialização, som e arquitetura.
3. Deduplicar variantes de engines por similaridade de bytecode/recursos antes de gastar análise repetida em títulos parecidos.
4. Documentar especificamente classes, funções e evidências, diferenciando inferências de observações em execução.
5. Portar **as técnicas**, não código/arte protegidos, em novos módulos originais do PocketForge. Demonstrar uso real.
6. Criar testes e benchmarks comparativos; **não alegar ganhos de velocidade/memória se não foram medidos**.
7. Organizar novos PRs por lote/tema da fase detalhada, cada um com relatório, alteração funcional do motor quando sustentada por evidência e regressões verificadas.

## Auditoria sintética reproduzível (somente se for preciso validar, não repetir)

- Fonte: `https://archive.org/download/1000_J2ME_Games_Pack/1000JavaGames.zip`
- Hash SHA-256 do ZIP: `f8e3fb19f0cb451a1eebecccc16c4cb941c68293db2990a4e82df68bfa2c10dd`
- Script: `scripts/audit_j2me_batch.py`; histórico do workflow: `.github/workflows/complete-j2me-static.yml`
- Teste da integridade do ledger: `python3 -m unittest tests.test_corpus_registry -v` (ou descoberta de testes).
- O arquivo original e os JAR/JAD não ficam versionados; apenas resultados próprios.

## Prompt para novo chat

> Continue o projeto PocketForge no repositório AlexandreGSilva07/Pocket-forge. Leia AGENTS.md, docs/research/CONTINUITY.md, docs/research/STATIC_COMPLETE.md e o registry.json. A **auditoria sintética de 1.649 JARs está concluída** em 17 PRs mesclados. Não repita essa etapa. Faça agora engenharia reversa DETALHADA, com análise real de classes e algoritmos, registre a evidência por arquivo e reconstrua progressivamente o motor do PocketForge com código original, integração, testes e benchmarks. Preserve o ledger permanentemente.

## Atualização importante — RE profunda já iniciada

**Não reiniciar a classificação dos 1.649 JARs e não reclassificar como completos os 100 escolhidos.** A primeira onda desmontou de verdade os bytecodes de 12 JARs via OpenJDK `javap`, armazenando inventários por classe e método em [deep/wave01](deep/wave01/overview.md). Houve revisão parcial de métodos reais em Xrossing Dice, 3D Adventure e 7 Zwerge; nenhuma execução dos originais em emulador foi feita. PRs #19 e #21 já integrados criaram os novos módulos AI, TilePack e Pixel Surface, testados em demos HTML/Chromium. O PR #20 é **rascunho de script para os 88 restantes; ainda não executado**. Progresso formal: [deep/registry.json](deep/registry.json).
