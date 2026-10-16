# 04 — Componentes reutilizáveis e lógica de gameplay

## Filosofia
Componentes expressam comportamentos isolados; entidades compõem sistemas. Para jogos pequenos, objetos JS bem separados são suficientes. Não impor ECS formal quando aumenta complexidade sem ganho.

## Catálogo mínimo

| Componente | Estado | Interface esperada |
| --- | --- | --- |
| Transform | posição, rotação, escala | `setPosition`, `translate`, `snapshot` |
| Motion | velocidade, aceleração, drag | `update(dt, input)` |
| Collider | shape, layers, máscara | `overlap(other)`, `resolve(other)` |
| Health | atual, máximo, invulnerabilidade | `damage(amount)`, `heal(amount)` |
| StateMachine | estado, transições | `send(event)`, `can(event)` |
| Sprite/Shape | visual, z-order | `render(ctx, camera)` |
| Lifetime | duração, expiração | `tick(dt)`, `expired` |
| Projectile | direção, dono, tipo | `spawn(config)`, `hit(target)` |
| Camera | posição, zoom, shake | `worldToScreen`, `follow` |
| InputActions | ação, fonte, pressed/released | `snapshot()`, `consume(action)` |
| AudioCue | identificador, prioridade | `emit(event)` |
| Progression | experiência, desbloqueios | `apply(event)` |

## Regras de contratos
- **Sem side effects ocultos**: dano não inicia automaticamente uma mudança de tela.
- **IDs explícitos**: entidade e recurso são referenciados por chaves estáveis.
- **Delta em segundos**: `dt` não é número de frames.
- **Eventos tipados**: `enemy.hit`, `player.dead`, `level.cleared`.
- **Renderização não decide regras**: partículas cosméticas não podem alterar vida.
- **Cada componente possui teardown** quando registra input, timers ou áudio.
- **Configuração é dado**: preferir tabelas de balanceamento a valores mágicos dispersos.

## Colisões
AABB primeiro, círculos para objetos arredondados. Hitboxes não devem obrigatoriamente acompanhar cada detalhe visual. Adotar camadas (jogador, inimigo, projétil, parede, pickup) e filtrar colisões desnecessárias antes da geometria. Broad phase por grade uniforme se a contagem justificar; medir primeiro.

## Movimento e sensação
Priorizar resposta de input: aceleração previsível, velocidade máxima e desaceleração. Para plataforma, considerar coyote time e jump buffering. Para ação, hit stop curto, windup legível e invulnerabilidade pós-dano. Testar touch e teclado sem transferir cegamente sensibilidade entre ambos.

## Progresso e persistência
Regras de score e progressão pertencem ao `world`, não ao HUD. Salvar apenas estado mínimo versionado; validar dados recuperados. Para web offline, `localStorage` é aceitável para configurações e recordes pequenos, com tratamento de falhas/ambiente restrito.

## Dificuldade
Construir curvas limitadas: diminuir janelas, aumentar velocidade/frequência ou ampliar padrões de inimigo. Evitar modificar todos os parâmetros simultaneamente; isso impede explicar o que melhorou. Testar se é possível vencer/perder de forma compreensível.

## Exemplo: dano puro
```js
function applyDamage(health, amount) {
  const next = Math.max(0, health.current - Math.max(0, amount));
  return { ...health, current: next, dead: next === 0 };
}
```

A função retorna novo estado; o sistema que a chama decide quando criar partículas, áudio, knockback e transição para derrota.

## Critérios de aceite de um componente
1. Interface/contrato público documentado.
2. Estado inicial e casos de borda definidos.
3. Testes para transições/critérios fundamentais.
4. Custo por frame aceitável na cena de referência.
5. Nenhuma dependência de assets externos surpresa.
6. Exemplo reproduzível no projeto de demonstração quando apropriado.

## Implementado na pesquisa J2ME — renderer compacto v0.2

`demo/engine/compact.js` fornece componentes **originais, reutilizáveis e executados no Lumen Shift**: atlas horizontal com regiões de desenho, gerador de mapas tipados (`Uint8Array`), codificador/decodificador RLE com validação rígida e renderer Canvas 2D com culling de tiles. `demo/game.js` usa o atlas/mapa de fato para desenhar o fundo. Testes determinísticos estão em `tests/compact_engine.test.cjs`.

**Evidência e limite:** o desenho via atlas, a representação compacta e a persistência simplificada são padrões observados nos JARs, mas os detalhes concretos deste módulo são **implementações próprias**. Ainda não foi provado que a nova implementação melhora FPS, RAM ou tamanho sobre a anterior; o desempenho deve ser medido. A decoração do fundo não é uma engine de plataforma/RPG completa.

## Storage Core v0.2 — reconstrução incremental por evidência do corpus

Em `demo/engine/state.js`, `PocketForgeState.createStore` implementa registros identificados, namespace, versão, persistência via `localStorage`, fallback de sessão e migração não destrutiva. O Lumen Shift migra o recorde do formato anterior e persiste através da API do motor. Testes em `tests/state_engine.test.cjs` cobrem roundtrip, versionamento, dados corrompidos, bloqueio de armazenamento e isolamento entre jogos.

**Origem e diferença técnica:** o inventário do corpus J2ME encontrou numerosas referências a `javax.microedition.rms.RecordStore`. Isso motiva uma API moderna mínima de snapshots; **não é port de RecordStore nem prova de que a implementação seja equivalente**. Ainda faltam benchmarks de latência/durabilidade em aparelhos reais.
