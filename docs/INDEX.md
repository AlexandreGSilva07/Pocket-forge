# Índice da documentação PocketForge

## Primeiro contato
- [Visão e princípios](00-visao.md)
- [Pipeline de produção](01-pipeline.md)
- [Arquitetura](02-arquitetura.md)
- [Tutorial do primeiro jogo](13-tutorial-primeiro-jogo.md)
- [Glossário](14-glossario.md)

## Implementação e criação
- [Tecnologias e renderização](03-tecnologia-renderizacao.md)
- [Componentes e gameplay](04-componentes.md)
- [Direção de arte e assets](05-artes-assets.md)
- [Áudio](06-audio.md)
- [UI e design system](17-design-system-ui.md)
- [Receitas por gênero](10-receitas.md)

## Continuidade e engenharia reversa em lotes de 100
- [Como retomar em outro chat: CONTINUITY](research/CONTINUITY.md)
- [Registro permanente (ledger) com os 1.649 hashes](research/batches/registry.json)
- [Auditoria sintética concluída: estatísticas e índices de todos os 17 lotes](research/STATIC_COMPLETE.md)
- [Fase detalhada: protocolo e rastreador](research/deep/README.md) · [registry detalhado](research/deep/registry.json)
- [Lote 001](research/batches/001.md) · [Lote 017](research/batches/017.md)

## Pesquisa empírica
- [Auditoria massiva J2ME — 2.309 JARs (1.649 hashes distintos)](research/02-auditoria-j2me-2309-jars.md) — resultados reais de download e inspeção automatizada
- [Engenharia reversa de jogos J2ME — lote 01](research/01-analise-j2me-lote01.md) — 10 JARs efetivamente inspecionados, evidências técnicas, limites e experimentos propostos

## Garantia de qualidade
- [Performance e profiling](07-performance.md)
- [Testes, gates e evidências](08-qa-testes.md)
- [Distribuição, segurança e licenças](09-distribuicao-licencas.md)
- [Benchmarks e protocolos de avaliação](16-benchmarks-avaliacao.md)

## Arquitetura futura
- [Manifesto e contratos de dados](12-manifesto.md)
- [Harness de agentes](15-harness-agentes.md)
- [Interface de ferramentas](18-protocolo-ferramentas.md)
- [Roadmap e níveis de maturidade](11-roadmap.md)
- [Limites e perguntas difíceis](19-perguntas-e-limites.md)

## Operação
- [SKILL.md](../SKILL.md) — entrada da skill e carregamento sob demanda
- [README.md](../README.md) — instalação e comandos
- [Game Brief de exemplo](../examples/game-brief.md)
- [Manifesto de exemplo](../examples/pocketforge.json)
- [Schema JSON](../schemas/pocketforge.schema.json)
- [Playbooks dos oito agentes](../agents/INDEX.md): Director, Architect, Gameplay, Visual, Audio, Profiler, Reviewer e Release

**Status:** a documentação distingue capacidades implementadas (v0.1) de projetos futuros; consulte o [roadmap](11-roadmap.md).
