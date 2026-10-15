# 12 — Contratos de dados e manifesto de projeto

## Por que ter manifesto
Permitir que designer, gerador de arte, lógica, QA e release compartilhem **uma representação auditável** dos requisitos. Sem contrato, nomes de assets, controles e estados divergem.

## Estrutura proposta
Arquivo `pocketforge.json`. O esquema descrito abaixo é a especificação de referência inicial; **o scaffold v0.1 não lê esse arquivo para gerar a mecânica**. O `examples/pocketforge.json` mostra um exemplo.

```json
{
  "schemaVersion": "0.1",
  "id": "lumen-shift",
  "title": "Lumen Shift",
  "target": { "platform": "web", "orientation": "responsive" },
  "genre": "arena-action",
  "input": ["keyboard", "touch"],
  "visual": { "style": "neon-vector", "motion": "reduced-supported" },
  "budgets": { "transferBytes": 1048576, "targetFps": 60 },
  "states": ["menu", "playing", "paused", "defeat"],
  "assets": [],
  "acceptance": ["player-moves", "player-can-lose", "game-restarts"]
}
```

## Convenções
- `id`: minúsculo com hífens, estável e sem espaços.
- `title`: rótulo humano.
- `schemaVersion`: versão de formato independente da versão do jogo.
- `target`: orientações e plataformas realmente testadas.
- `budgets`: metas; `evidence` contém as medições reais separadamente.
- `assets`: IDs estáveis com tipo, caminho, dimensões, licença/proveniência.
- `states`: estados possíveis e transições válidas.
- `acceptance`: critérios testáveis, não slogans como “bonito e rápido”.

## Evolução de schema
1. Modificações compatíveis adicionam campos opcionais.
2. Incompatibilidades exigem novo `schemaVersion` e migração.
3. Não sobrescrever evidências de métricas anteriores sem preservar ambiente.
4. Todo campo que influencia jogo deve ter valor padrão explícito ou ser obrigatório.

## Manifesto de asset (modelo)
```json
{
  "id": "player.main",
  "kind": "svg",
  "path": "assets/player.svg",
  "source": "procedural",
  "license": "MIT",
  "pivot": [0.5, 0.5],
  "logicalSize": [48, 48]
}
```

## Trilha de auditoria
Separar `brief`, `implementation`, `measurements` e `evidence`. Uma meta de 60 FPS não é a mesma coisa que uma amostra medida no celular. Guardar commit, ambiente, caminho dos relatórios e data.
