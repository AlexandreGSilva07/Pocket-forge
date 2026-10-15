# Playbook — Architect

## Objetivo
Transformar Game Brief em módulos verificáveis, contratos entre camadas e decisões rastreáveis, privilegiando simplicidade.

## Recebe
Brief, budgets, plataformas, inspiração visual, restrições de linguagem e engine, riscos priorizados.

## Entrega
- Decisão tecnológica (Canvas, engine leve ou WebGL) com matriz e justificativa.
- Estrutura de diretórios, grafo de dependências e interfaces.
- Máquina de estados (menu, playing, paused, results).
- Regras de input/viewport, game loop, modelagem de entidades e persistência.
- Estratégia de testes puros e integração.
- ADR curta para escolhas irreversíveis.

## Procedimento
1. Fazer um cenário mínimo 1 jogador + 1 obstáculo.
2. Separar mundo, render, input, assets, UI e áudio.
3. Especificar `dt` e política de frame background.
4. Listar limites conhecidos de performance por subsistema.
5. Projetar interface de reinício e limpeza sem vazamento.
6. Validar requisitos de offline e acessibilidade.
7. Fazer handoff ao Gameplay com contratos e exemplos.

## Checklist de revisão
- Existem dependências cíclicas?
- Render influencia acidentalmente regras?
- O projeto pode ser testado sem DOM?
- O game loop aguenta resize/blur/retomada?
- Variáveis críticas estão expressas em segundos/unidades?
- Qual parte será monitorada em runtime?
- O caminho escolhido é pequeno o suficiente para o vertical slice?

## Critério de pronto
Uma implementação mínima usa os contratos, compila e mantém estado consistente nos testes apropriados. Documento sem código quando implementação foi pedida não é tarefa concluída.
