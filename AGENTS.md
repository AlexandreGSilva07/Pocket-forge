# AGENTS.md — PocketForge

Este repositório é uma super-skill para criar jogos modernos ultraleves. Nenhum agente deve depender do histórico da conversa.

## Leia antes de agir
1. [SKILL.md](SKILL.md) — contrato de criação de jogos e critérios de qualidade.
2. [docs/research/CONTINUITY.md](docs/research/CONTINUITY.md) — protocolo de auditorias de 100 JARs por PR.
3. [docs/research/batches/registry.json](docs/research/batches/registry.json) — fonte de verdade dos SHA-256 já investigados.
4. [docs/INDEX.md](docs/INDEX.md) — referência completa de arquitetura, assets, arte, QA, harness e benchmarks.

## Estado de auditorias
A **auditoria sintética dos 1.649 JARs com hashes distintos está concluída**, em 17 PRs mesclados na main. Ver [relatório final](docs/research/STATIC_COMPLETE.md). Não repetir os 17 lotes: começar a engenharia reversa detalhada com análise real de código/algoritmos. 1.649 SHA-256 distintos não significam 1.649 títulos únicos.

## Para os PRs da fase DETALHADA (a próxima etapa)
- Aproveitar os IDs e metadados já existentes em registry.json, sem reauditar o inventário. Manter um registro adicional do avanço detalhado por hash e classe/função.
- Descrever análise estática versus análise profunda; não afirmar que o programa foi executado se apenas leu bytecode.
- Alterar **código funcional do motor** com testes; jamais só gerar relatórios.
- Integrar o componente em uma demonstração ou teste executável, avaliar regressões e medir benefícios antes de alegar ganho de desempenho.
- Atualizar o ledger, os relatórios por jogo e a documentação de engenharia.
- Executar a suite Node, Python e smoke de navegador no GitHub Actions.
- Não publicar jogos originais, recursos gráficos, áudio nem código decompilado de terceiros.

## Motor atual
- demo/engine/compact.js — atlas Canvas, mapa de tiles tipado, RLE e culling.
- demo/engine/state.js — armazenamento versionado, tratamento de corrupção, migração de saves e fallback.
- demo/engine/audio.js — síntese procedural WebAudio com limite de vozes.
- demo/game.js — jogo Lumen Shift usa estes módulos na execução real.

## Comandos
~~~bash
node --test tests/*.test.cjs
python3 -m unittest discover -s tests -v
node --check demo/game.js
python3 tests/browser_smoke.py
~~~

Use a branch nova, produzindo um PR por lote. Antes de abrir PR, verifique CI, documentação, ID único e demonstração. Não marque DONE sem evidência.
