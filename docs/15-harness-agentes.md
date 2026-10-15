# 15 — Projeto do harness de agentes (alvo arquitetural)

> **Status:** referência de arquitetura. A v0.1 possui playbooks e ferramentas, mas **não** executa automaticamente agentes autônomos nem um ciclo de revisão multiagente.

## Por que um harness
Uma skill longa sem controle de estado tende a gerar muitos arquivos, confundir hipóteses com resultados e produzir retrabalho. O harness proposto adiciona **planejamento explícito, execução isolada, observação, revisão e decisões reproduzíveis**.

## Componentes do harness
```text
Pedido
  │
  ▼
Spec Compiler ───► Game Brief + acceptance.json + budget.json
  │
  ▼
Planner ─────────► DAG de tarefas pequenas, responsáveis e dependências
  │
  ├──► Art Worker ───────► assets + proveniência + revisão visual
  ├──► Gameplay Worker ──► módulos + unit tests
  ├──► Audio Worker ─────► eventos + assets + smoke
  └──► Build Worker ─────► bundle + manifest + verificações estáticas
  │
  ▼
Runtime Test Harness ──► evidências: logs, screenshots, inputs, métricas
  │
  ▼
Independent Reviewer ──► PASS / FAIL / NOT TESTED
  │
  ├── FAIL corrigível ► novo incremento limitado
  └── PASS ───────────► release report
```

## Artefatos compartilhados
- `game-brief.json`: problema e restrições.
- `acceptance.json`: critérios automatizáveis e manuais.
- `budget.json`: metas com device/profile/método.
- `tasks.json`: dependências, escopo, caminhos permitidos, owner e estado.
- `assets/manifest.json`: IDs, tamanhos, pivôs e licenças.
- `reports/evidence.json`: comandos, resultados, hashes, hardware e lacunas.
- `reports/review.json`: bloqueadores, severidade, reproduções.

## Autômato de tarefas
`proposed → ready → running → artifact_ready → verified → accepted`; alternativos `blocked`, `failed`, `cancelled`. Uma tarefa em `artifact_ready` **não pode virar `accepted` apenas por declaração do agente que a executou**. Exigir revisão por critérios objetivos ou revisor separado.

## Regras de concorrência
- Dependências e contratos congelados antes de paralelismo.
- Workers não editam simultaneamente o mesmo arquivo.
- Uma fonte de verdade para Game Brief, manifestos e budgets.
- Merge apenas com testes pertinentes e resolução de conflitos de design.
- Limite de tentativas e orçamento de tokens por tarefa.
- Falha de build ou P0 interrompe expansão de conteúdo.

## Hierarquia de revisão
**Nível 1**: scripts determinísticos (parse, JSON, tamanho, paths).  
**Nível 2**: integração browser (interações, console, load).  
**Nível 3**: performance real (traço, percentis, aparelhos).  
**Nível 4**: avaliação humana/visual (coerência, diversão, comunicação, acessibilidade).  
Não usar parecer de LLM como substituto de execução.

## Contrato de evidência
```json
{
  "taskId": "player-movement",
  "status": "verified",
  "commit": "abcdef",
  "checks": [
    {"name": "keyboard-left", "result": "pass", "method": "browser-input"}
  ],
  "notTested": ["touch-android"],
  "artifacts": ["demo/game.js"]
}
```
O contrato acima é **proposto**. Não há ainda parser/orquestrador na v0.1.

## Anti-loop
Após três tentativas repetindo a mesma falha sem nova evidência, interromper, documentar hipótese de raiz e propor experimento menor; não continuar gerando código sem diagnóstico.

## Critério de maturidade
O harness só poderá ser chamado de “operacional” quando possuir pelo menos um fluxo completo em CI, do brief até execução de browser com screenshot e revisão independente rastreáveis, e comparar resultados entre jogos diferentes.
