# 18 — Interface recomendada para ferramentas futuras

> **Status:** contrato de interoperabilidade proposto para ferramentas novas. Os scripts v0.1 usam CLI humana e não implementam ainda este protocolo JSON completo.

## Objetivo
Permitir que agentes chamem ferramentas sem depender de parsing de texto livre. A futura interface padrão seria `pocketforge tool <name> --input request.json --output result.json`, mantendo ferramentas pequenas e reprodutíveis.

## Envelope de pedido
```json
{
  "version": "0.1",
  "taskId": "atlas-17",
  "action": "atlas.pack",
  "input": {"assetsManifest": "assets/manifest.json"},
  "constraints": {"maxSizePx": 2048, "paddingPx": 2},
  "outputDir": "build/assets"
}
```

## Envelope de retorno
```json
{
  "version": "0.1",
  "taskId": "atlas-17",
  "status": "ok",
  "artifacts": [
    {"path": "build/assets/atlas.webp", "sha256": "HASH", "bytes": 12345}
  ],
  "metrics": {"durationMs": 900, "count": 54},
  "warnings": [],
  "errors": []
}
```
`HASH` é placeholder, não um hash real.

## Taxonomia de erros
- `INVALID_INPUT`: schema ou parâmetro rejeitado.
- `MISSING_ASSET`: referência não encontrada.
- `LICENSE_UNKNOWN`: recurso sem proveniência suficiente.
- `BUDGET_EXCEEDED`: limite excedido.
- `UNSUPPORTED_FEATURE`: motor/codec não implementado.
- `RUNTIME_TEST_FAILED`: execução observou falha.
- `UNVERIFIED`: não foi possível executar prova exigida.

## Invariantes
- Saída determinística com seed/versão quando apropriado.
- Sem modificar arquivos fora dos paths autorizados.
- Sem download oculto de assets.
- Erros estruturados; não salvar sucesso parcial como `ok`.
- Artefatos contendo provenance e checksums reais.
- Limites explícitos de tempo, memória e tamanho.
- Logs separados da resposta JSON da ferramenta.

## Ferramentas candidatas
`game.scaffold`, `assets.vector_generate`, `assets.atlas_pack`, `scene.validate`, `qa.browser_smoke`, `qa.visual_diff`, `perf.benchmark`, `bundle.audit`, `release.package`.

Não afirmar que essas ações já existem só porque estão documentadas. Na v0.1 existem apenas os scripts listados em `SKILL.md`.

## Ordem de implantação
1. Padronizar saída JSON de ferramentas atuais.
2. Definir schemas e testes contratuais.
3. Implementar runner isolado com sandbox de paths.
4. Integrar browser/testes de runtime.
5. Expor integração MCP opcional sem obrigar o jogo a usar MCP.
