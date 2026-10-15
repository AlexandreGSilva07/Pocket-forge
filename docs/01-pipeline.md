# 01 — Pipeline operacional da super-skill

## Estados
`DISCOVERY → DESIGN → SLICE → CONTENT → HARDENING → RELEASE`. Uma etapa só é concluída quando suas saídas e evidências existem. Reabrir etapas é permitido e esperado.

### A. Discovery
**Entradas:** pedido do usuário, restrições de plataforma, referências legítimas.  
**Saídas:** Game Brief, registro de hipóteses, 3–5 riscos, dispositivo alvo, orçamento preliminar.  
**Gate:** fantasia e loop descritos em termos observáveis.

### B. Design
**Saídas:** modelo de estados, contrato de inputs, decisão tecnológica, mapa de entidades, moodboard sem copiar ativos, métricas de experiência.  
**Gate:** tudo que é essencial pode ser construído com recursos disponíveis; risco crítico tem experimento previsto.

### C. Vertical Slice
**Saídas:** build executável com início, controle, conflito, feedback, derrota/vitória e reinício; telemetria mínima.  
**Gate:** testado pelo menos uma vez em runtime real, com comandos/ambiente anotados. `node --check` não vale como runtime.

### D. Content
**Saídas:** assets aprovados, níveis, progressão, trilha, UI, metas de download atualizadas.  
**Gate:** consistência visual, ausência de placeholders indevidos, caminhos de assets válidos, navegação completa.

### E. Hardening
**Saídas:** relatório de bugs, testes automatizados, testes manuais, p50/p95 de frame em hardware de referência, orçamento de assets.  
**Gate:** sem bugs bloqueadores; metas atendidas ou explicitamente renegociadas.

### F. Release
**Saídas:** build, modo de servir, README de operação, licenças e relatório de evidências.  
**Gate:** build reproduzível; demonstrativo abre em ambiente documentado; conteúdo original/licenciado.

## Rotina sugerida para agente único
1. Inspecionar o repositório antes de tocar nos arquivos.
2. Registrar hipóteses e critérios de aceite.
3. Criar um incremento pequeno e executável.
4. Executar testes objetivos e capturar falhas reais.
5. Corrigir primeiro bloqueadores, depois visual/performance.
6. Fazer revisão independente (ou passe separado com checklist) antes de encerrar.
7. Relatar em três colunas: **feito / medido / não verificado**.

## Papéis especializados
- **Director**: interpreta intenção e mantém visão do projeto.
- **Architect**: define boundaries, game loop e contratos.
- **Visual**: direção de arte, legibilidade e assets.
- **Gameplay**: sensação de controles, inimigos, progressão e equilíbrio.
- **Sound**: design sonoro e políticas de desbloqueio de áudio.
- **Profiler**: custos reais e alternativas.
- **Reviewer**: testes e evidências; não confunde estilo com correção.
- **Release**: empacota, audita proveniência e limitações de distribuição.

Esses papéis podem ser executados pelo mesmo agente em etapas distintas. Sua presença no texto não significa que subagentes estejam em execução.

## Protocolo de transferência entre papéis
Cada entrega deve conter:
- **Contexto**: versão/commit, brief relevante.
- **Artefatos**: paths exatos.
- **Decisões**: trade-offs e motivos.
- **Evidências**: comandos usados, resultados e ambiente.
- **Dívida e riscos**: o que ficou de fora.
- **Próximo contrato**: o que o consumidor precisa garantir.

## Como não desperdiçar tokens
Carregar documentação conforme a fase; usar manifestos estáveis; evitar colar milhares de linhas quando um diff basta; resumir observações com referências a arquivos/commits; não pedir ao LLM para fazer matemática, empacotamento, hashing ou análise determinística já coberta por scripts.

## Matriz de falhas
| Falha | Diagnóstico verificável | Mitigação |
| --- | --- | --- |
| Tela branca | console, exceções, HTTP dos assets | corrigir imports/caminhos/boot |
| Jogo sem resposta | eventos, focus, ponteiro, estados | inspeção de input e pointer capture |
| FPS variável | profiler e frame histogram | reduzir draw calls, alocações e efeitos |
| Assets incoerentes | atlas/paleta/escala comparativa | style guide e revisão de conjunto |
| Peso inflado | auditor de arquivos e bundle | atlas, compressão, retirar dependências |
| Offline não funciona | teste com rede bloqueada | assets locais e cache versionado |
| “Funciona aqui” | matriz de dispositivos | testes em touch/teclado e diferentes DPI |
