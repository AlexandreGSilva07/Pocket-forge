# 11 — Roadmap, maturidade e trabalho não implementado

## Níveis de maturidade
| Nível | Descrição | Estado |
| --- | --- | --- |
| L0 | texto de instrução isolado | superado |
| L1 | documentação modular + vertical slice + scripts básicos | **v0.1** |
| L2 | múltiplos templates/gêneros e testes de browser automatizados | planejado |
| L3 | pipeline robusto de arte, audio e cenas com manifestos validados | planejado |
| L4 | orquestração multiagente instrumentada + checkpoints automáticos | planejado |
| L5 | geração generalista avaliada por benchmarks de projetos distintos | pesquisa |

## Milestone 0.1 — Fundação
- [x] Instruções de skill e referências técnicas.
- [x] Arquitetura e protocolos de produção.
- [x] Demo Canvas e ferramentas de scaffold/auditoria/assets.
- [x] Testes de scripts em CI.
- [ ] Teste real de navegador em hardware variado.
- [ ] Medições repetidas de FPS/energia.
- [ ] Sistema automático de criação de diferentes gêneros por prompt.

## Milestone 0.2 — Robustez
- [ ] Harness Playwright em Chromium com captura e input automatizados.
- [ ] Frame snapshots e testes de UI em retrato/paisagem.
- [ ] Baselines de tamanho e orçamento no CI.
- [ ] Manifests de assets e cenas com schema JSON validado.
- [ ] Testes de input touch em dispositivos físicos.
- [ ] Regressores de estados puros com seeds/replay.

## Milestone 0.3 — Art Studio
- [ ] Pipeline consistente de conceitos → sprites/vetores → atlases.
- [ ] Arte programática para fundos, props, partículas e UI.
- [ ] Inspeção de transparência/pivot/colisão.
- [ ] Geração de animação coerente com rig/partes.
- [ ] Auditor de proveniência e licença.

## Milestone 0.4 — Genre Packs
- [ ] Arena shooter.
- [ ] Platformer.
- [ ] Corrida pseudo-3D.
- [ ] Puzzle.
- [ ] RPG isométrico compacto.
- [ ] Demo de low-poly 3D para comparar peso/recursos.

## Milestone 0.5 — Agent Harness
- [ ] Plans tipados; geração incremental e rollback.
- [ ] Revisão independente e falhas impeditivas.
- [ ] Catálogo de padrões recuperáveis.
- [ ] Métricas por custo de geração e qualidade.
- [ ] Avaliação cega de jogabilidade e comparações entre soluções.

## Definição de avanço
Um milestone não está concluído porque arquivos foram criados; exige comportamento observado, verificações relevantes, comandos de reprodução, métricas e documentação atualizada.

## Riscos
- **Goodhart**: otimizar “MB” à custa de arte e diversão.
- **Benchmark contamination**: exemplo visto pelo agente não demonstra generalização.
- **Explosão de escopo**: 8 agentes descritos não equivalem a um pipeline integrado.
- **QA superficial**: capturas não demonstram input nem progressão.
- **Licenças**: geração automática sem trilha de proveniência cria risco.

## Como priorizar
Escolher próximo incremento por: impacto em jogos reais, reutilização, capacidade de ser testado, custo de manutenção e lacunas observadas no demo. Preferir ferramenta pequena que resolve uma falha concreta a documentação extra sem uso.
