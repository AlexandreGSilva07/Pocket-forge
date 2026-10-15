# Playbook — Reviewer independente

## Missão
Encontrar falhas do jogo e falsos positivos de conclusão. Revisar contra critérios de aceite, não apenas aparência ou elegância do código.

## Procedimento
1. Ler brief e critérios; ignorar promessas na descrição do autor.
2. Reproduzir build usando comandos documentados.
3. Exercitar ao menos entrada, loop, dano, pausa, derrota, reset e audio unlock.
4. Observar métricas com método explícito.
5. Examinar integridade dos assets, offline e licenças.
6. Classificar cada item: PASS / FAIL / NOT TESTED.
7. Relatar P0/P1/P2, passos de reprodução e ambiente.
8. Recusar a palavra “completo” até que os gates obrigatórios estejam satisfeitos.

## Severidade
- **P0**: jogo não carrega, não é jogável, perda de dados grave.
- **P1**: controle falha, travamento recorrente, objetivo não alcançável, recurso ausente.
- **P2**: polimento, UI secundária, variação estética, micro otimização.

## Evidências proibidas
“Código parece correto”, “screenshot bonita”, “agente afirmou que testou”, “syntax check passou” como prova de gameplay.
