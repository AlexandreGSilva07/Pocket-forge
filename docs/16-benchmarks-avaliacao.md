# 16 — Benchmarks e metodologia de avaliação

> Status: **protocolo proposto**, não números já medidos pelo PocketForge.

## Questão central
Como demonstrar que a super-skill **cria jogos melhores e mais eficientes**, e não apenas texto mais elaborado?

## Conjunto de avaliação
Criar no mínimo cinco briefs cegos, cobrindo:
1. Puzzle visual com undo e solução comprovável.
2. Arena shooter com inimigos, score e touch.
3. Platformer com controle de salto, colisões e checkpoint.
4. Corrida pseudo-3D com sprites escalados, curva e controles.
5. Micro-3D ou 2.5D com arte e cena coerentes.

Usar tarefas **não vistas durante a produção dos exemplos**. Manter sementes, conteúdo solicitado e orçamento iguais em comparações.

## Baselines
- **B0**: agente sem a skill.
- **B1**: agente com somente prompt curto de “jogo leve”.
- **B2**: agente com PocketForge, sem scripts.
- **B3**: agente com skill + scripts + QA.
Controlar modelo, hardware, limite de tokens, tempo e disponibilidade de ferramentas. Relatar versões.

## Métricas de resultado
| Métrica | Interpretação | Direção |
| --- | --- | --- |
| Critical acceptance pass rate | % de requisitos essenciais observados | maior |
| Playability score | % de casos exercitados de input/objetivo/fim | maior |
| Package bytes | tamanho transferido do build | menor, mantendo qualidade |
| Cold start p50/p95 | tempo até interatividade sem cache | menor |
| Frame time p50/p95/p99 | distribuição de duração por frame | menor |
| Crash/error rate | exceções por minuto / cenário | menor |
| Visual coherence | avaliação cega com rubrica | maior |
| Fix efficiency | bugs corrigidos por ciclo e custo | maior |
| Reuse score | módulos efetivamente reutilizados | maior |

## Rubrica de arte (0–4 por eixo)
- Linguagem de formas consistente.
- Hierarquia focal e leitura de gameplay.
- Animações/feedback perceptivelmente polidos.
- Paleta, efeitos e iluminação coerentes.
- Elementos são legíveis em viewport pequeno.

Avaliadores devem olhar **o jogo em movimento**, não só um screenshot.

## Teste de performance
Configuração fixada: dispositivo e browser exatos, bateria/energia, resolução, DPR, conteúdo da cena, duração, cache e número de repetições. Aquecer, depois medir pelo menos três janelas em cargas baixa/média/alta. Reportar p50/p95/p99 e variância.

## Instrumentação sugerida
- Trace do Performance panel/Playwright.
- `performance.now()` para intervalos controlados.
- Long Tasks API quando aplicável.
- Auditores de bytes brutos e transferidos.
- Logs de posição/estado e replay determinístico.
- Comparação por screenshots com tolerância ao render do dispositivo.

## Teste de confiabilidade
Induzir: `blur`, aba em background, redimensionamento, refresh, rapid-fire input, teclado + touch simultâneo, áudio bloqueado, localStorage indisponível. Cada recuperação esperada deve ser especificada.

## Publicação
Cada benchmark precisa incluir comando de reprodução, brief, modelo usado, versões, commit, dados brutos, relatórios e falhas. Não publicar apenas “atingiu 60 FPS” sem evidência.
