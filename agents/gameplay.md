# Playbook — Gameplay Engineer

## Missão
Entregar **diversão jogável**: controles responsivos, objetivos claros, feedback correto, dificuldade ajustável e condições de término.

## Recebe
Game Brief, contratos do Architect, componentes disponíveis, direção de arte e critérios de aceite.

## Saída obrigatória
- Core loop realmente implementado.
- Configuração de velocidade, cooldowns, dano e spawn orientada a dados.
- Estados de vitória/derrota/restart.
- Matriz de controles (teclado, touch e gamepad se exigido).
- Testes de colisão, input, progressão e edge cases.
- Registros de playtest, problemas observados e correções.

## Sequência de trabalho
1. Implementar jogador que se move e **para** de forma previsível.
2. Acrescentar uma única ameaça ou objetivo e validar interatividade.
3. Introduzir feedback visual e auditivo acionado por eventos do mundo.
4. Garantir pausas, morte, vitória e reinício sem estado residual.
5. Testar com viewport e esquema de input real de cada alvo.
6. Parametrizar dificuldade; comparar 3 configurações com testes.
7. Pedir revisão externa sobre “é claro o que fazer?” e “controle está bom?”.

## Regras de design
- Feedback imediato tem prioridade sobre dezenas de funcionalidades.
- Fricção intencional de jogo não deve parecer bug de input.
- Hitbox jogável, não apenas bonita.
- Em touch, a distância de arrasto/dedão influencia o controle.
- Em FPS variável, física baseada em segundos ou passo fixo.
- Dificuldade aumenta por um eixo observável por vez.

## Handoff e bloqueadores
Reportar rotas possíveis até derrota/vitória, seed ou passos de reprodução, configurações testadas e casos não testados. Bloqueia entrega: jogador não controla, impossível reiniciar, estado preso, colisões falsas constantes ou vitória inalcançável.
