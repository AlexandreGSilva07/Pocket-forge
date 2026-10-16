# Fase 2 — engenharia reversa detalhada de J2ME

**Estado:** não iniciada. A fase 1 de inventário foi concluída para 1.649 SHA-256 de JAR. O objetivo desta fase não é varrer novamente nomes e classes, mas **investigar arquitetura e comportamento de programas reais** e reconstruir progressivamente as melhores técnicas em componentes originais do PocketForge.

## Fluxo por jogo

1. Selecionar o arquivo pelo SHA-256 e nome já existentes em [../batches/registry.json](../batches/registry.json) e no arquivo JSON do lote correspondente.
2. Obter o binário original em ambiente temporário. Revalidar SHA-256. Não commitar JAR/JAD/recursos proprietários.
3. Descompilar bytecode de modo adequado a Java ME. Guardar somente informação necessária de classe, assinaturas e trechos pequenos de evidência técnica, não publicar decompilação integral proprietária.
4. Investigar render loop, gerenciamento de telas, atlas, animações, tilemaps, áudio, IA, física, carregamento e persistência, conforme aplicável.
5. Quando viável, **executar o jogo original em emulador** e comparar com a arquitetura inferida. Anotar tela/controles/eventos e grau de fidelidade; sem execução, manter esse campo como não verificado.
6. Produzir um estudo por jogo, com métodos/caminhos reconhecidos, invariantes, pseudocódigo próprio, técnicas e limitações. Não inventar classes ou algoritmos ausentes.
7. Identificar a família de motor/variante e evitar reestudar implementações idênticas.
8. Selecionar técnicas úteis à Web moderna, implementar código autoral no PocketForge, integrar em jogo de referência, executar testes e fazer comparações instrumentadas com baseline.
9. Registrar progresso em `registry.json` deste diretório, apontando para relatórios versionados.

## Estados independentes

- `not_started`: ainda não houve análise detalhada.
- `decompiled_reviewed`: lógica real estudada com evidências.
- `original_behavior_verified`: foi realmente executado o jogo original.
- `engine_implemented`: existe implementação nova e integrada do PocketForge.
- `engine_tested`: teste executável e de navegador verificado.
- `benchmarked`: números de latência/RAM/FPS/tamanho mensurados sob baseline comparável.

Estes estados não são necessariamente lineares — um jogo pode ter descompilação estudada sem execução ou sem módulo implementado. Não confundir falhas de uma etapa com sucesso de outra.

## Estrutura prevista por estudo

```text
docs/research/deep/
  registry.json                 # Estado global da fase detalhada
  README.md                     # Este contrato
  studies/
    <sha256-prefixo>-analise.md # Evidências e métodos descobertos
```

Cada estudo documentará SHA-256 completo, nome/caminho do jogo, origem, classes relevantes, comportamento confirmado versus inferido, diagramas ou pseudocódigo próprios, família de motor, pontos reutilizáveis, componentes PocketForge associados, testes, métricas, grau de confiança e limites.

## Critérios para PR completo na fase detalhada

- Evidências técnicas por arquivo, código e método real, além do inventário já existente.
- Módulo(s) novos ou aperfeiçoados integrados em jogo de referência quando uma técnica for validada. **Não implementar arbitrariamente** se os resultados contradisserem uma hipótese.
- Testes unitários, de integração e navegador conforme aplicabilidade; métricas comparativas sempre que alegar vantagem.
- Atualizar `registry.json` da fase detalhada; nunca sobrescrever os 1.649 registros sintéticos.
- Direitos e licenças: publicações apenas de documentação original e código próprio.

Veja também [../STATIC_COMPLETE.md](../STATIC_COMPLETE.md) e [../CONTINUITY.md](../CONTINUITY.md).
