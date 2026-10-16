# Continuidade PocketForge: 100 jogos por PR

Este documento é o ponto de partida de qualquer conversa futura. O estado **não depende da memória do chat**: deve ser reconstituído dos arquivos versionados, PRs e CI.

## Fontes de verdade

- Corpus fixo: https://archive.org/download/1000_J2ME_Games_Pack/1000JavaGames.zip. Seu SHA-256 é guardado no registro.
- Registro mestre permanente: docs/research/batches/registry.json. Contém cada lote e os **SHA-256 completos** dos JARs.
- Por lote: docs/research/batches/NNN.json (classes, APIs, símbolos, JAR e JAD, IDs), NNN.csv (tabular) e NNN.md (leitura humana).
- Configuração de seleção: config/j2me-batch.json; processamento: scripts/audit_j2me_batch.py; CI: .github/workflows/j2me-batch.yml.
- Motor funcional e uso real: demo/engine/compact.js e demo/game.js. Testes: tests/compact_engine.test.cjs, tests/browser_smoke.py e workflows.

## Níveis de conclusão — não misturar

1. STATIC_INSPECTED: inspecionado como ZIP/classfiles sem executar.
2. DECOMPILED_REVIEWED: rotinas de comportamento reconstruídas com evidências específicas.
3. ORIGINAL_BEHAVIOR_VERIFIED: executado e observado o jogo original.
4. ENGINE_IMPLEMENTED: componente original codificado e usado por um jogo PocketForge.
5. ENGINE_TESTED: testes unitários e em navegador aprovados.
6. BENCHMARKED: tamanhos/tempo de carregamento/frame-time/memória medidos em condições declaradas.

Referência de API presente não prova que ela seja usada em runtime. 100 JARs inspecionados estaticamente não são 100 jogos estudados profundamente.

## Como criar cada PR

1. Ler este guia, batches/registry.json, o lote mais recente e todos os PRs abertos.
2. Confirmar que o PR anterior foi mesclado; se não, criar branch a partir de uma base que CONTE o registro anterior, evitando perder o histórico.
3. Usar uma branch distinta (audit/j2me-batch-002 etc.), configurar batch N em config/j2me-batch.json e submeter. GitHub Actions seleciona 100 JARs com SHA distintos, por ordem determinística dos caminhos no ZIP.
4. Conferir se o CI realmente publicou os registros NNN.md/NNN.csv/NNN.json e atualizou registry.json. O CI aborta se detectar IDs repetidos no registro.
5. Cada PR deve identificar **TODOS** os 100 arquivos pelo nome/caminho JAR e hash SHA-256. Preencher campo JAD somente se houver um arquivo JAD real com nome correspondente; caso contrário, registrar 'não encontrado'. Não confundir JAR com JAD.
6. Inspecionar de modo mais profundo representantes diversos do lote: recursos, render, lógica, dados de nível, IA ou áudio. Explicar o método e as evidências.
7. Codificar e integrar uma melhoria verificável ao MOTOR — não só documentação — com testes. Caso não exista evidência suficiente, registrar essa limitação e manter PR como pesquisa, não como reconstrução concluída.
8. Medir diferenças reais sempre que alegar ganho de FPS, memória, tamanho ou latência. Incluir baseline, dispositivos, amostragem e testes.
9. Criar um PR exclusivo para o lote, título 'J2ME Batch NNN — 100 JARs + módulo do motor'. Anexar link de CI, documento de todos os arquivos e changelog de código/testes.
10. Nunca publicar conteúdo binário, imagens, músicas ou código decompilado de terceiros no repositório. Manter só metadados e implementações originais.

## Retomada em outro chat

Pedido recomendado:

> Continue PocketForge no repo AlexandreGSilva07/Pocket-forge. Leia docs/research/CONTINUITY.md, docs/research/batches/registry.json e verifique os PRs abertos. Processe o próximo lote de 100 JARs não repetidos e produza PR separado com todos os nomes e hashes. Reconstrua de fato um componente funcional do motor, integre ao jogo de demonstração, teste e reporte diferenças medidas. Não confunda inspeção estática com reconstrução de código.

## Estado da primeira execução

- Corpus original: 2.309 JARs analisados em inventário amplo; 1.649 hashes diferentes.
- Lote 001: 100 hashes distintos, docs/research/batches/001.md, .csv, .json e registry.json.
- PR inicial: https://github.com/AlexandreGSilva07/Pocket-forge/pull/1
- Motor original incorporado: compact.js, atlas Canvas de quatro regiões, tiles tipados, RLE, render de mapa com culling; usado em Lumen Shift.
- Sempre conferir CI antes de afirmar sucesso; testes e auditoria estrutural não comprovam superioridade de desempenho.

## Indicadores de qualidade a registrar por lote

| Qualidade | Evidência exigida |
|---|---|
| Identidade | SHA completo e nome/caminho original |
| Cobertura | 100 IDs únicos por PR, exceto lote final |
| Pesquisa | APIs, símbolos, recursos e representantes analisados em profundidade |
| Implementação | Arquivos de código alterados e usados no projeto |
| Testes | Comandos, saídas e link de CI |
| Performance | Medições reais versus baseline ou campo 'não medido' |
| Persistência | Arquivos versionados e somados ao ledger global |
