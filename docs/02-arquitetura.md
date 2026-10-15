# 02 — Arquitetura recomendada de jogo compacto

## Topologia lógica
```text
bootstrap
 ├─ asset loader + manifest
 ├─ input (teclado/touch/gamepad)
 ├─ clock (delta fixo)
 ├─ world + entidades + colisão
 ├─ regras/estado/progressão
 ├─ renderer + camera + efeitos
 ├─ mixer de áudio
 └─ HUD + menus + acessibilidade
```

## Loop
Separar **simulação com passo fixo** da renderização com interpolação. Exemplo: passo físico `1/60 s`, `requestAnimationFrame` para desenhar. A simulação recebe `dt` limitado; quando a aba volta de background, descartar atrasos excessivos em vez de tentar simular minutos acumulados.

Pseudocódigo:
```text
onFrame(now):
  frameDt = clamp((now - last)/1000, 0, 0.10)
  accumulator += frameDt
  while accumulator >= fixedDt and steps < maxSteps:
      input.snapshot()
      world.update(fixedDt)
      accumulator -= fixedDt
  renderer.draw(world, accumulator/fixedDt)
```

A implementação v0.1 do demo usa um loop simplificado e limita o delta; o modelo com accumulator é a evolução recomendada.

## Estados explícitos
`boot, menu, playing, paused, victory, defeat`. Toda transição deve definir: ações de entrada, saída, áudio, congelamento de simulação, efeitos pendentes e botões disponíveis. Nunca condicionar estado a texto desenhado no Canvas.

## Contratos de módulo
- `input`: devolve intenção sem saber como entidades são desenhadas.
- `world`: regras determinísticas sem manipular DOM.
- `renderer`: lê um snapshot e não altera regras.
- `assets`: mapeia IDs estáveis para recursos decodificados.
- `audio`: recebe eventos sem bloquear o loop.
- `ui`: acessível por DOM quando apropriado e sincronizada ao estado.

## Memória
- Preferir pools em partículas e projéteis frequentes.
- Evitar criar centenas de arrays/objetos a cada frame.
- Libertar listeners, áudio e timers ao destruir cenas.
- Usar atlases pequenos e específicos por cena.
- Pensar em **pico de memória**, não apenas tamanho comprimido no download.

## DPI e escala
Separar **resolução lógica** de **backing resolution**; limitar DPR para dispositivos lentos. Viewport responsivo, manter aspecto ou definir política de crop; converter coordenadas de ponteiro do CSS para o espaço lógico antes da colisão.

## Determinismo para teste
Separar RNG de simulação e RNG cosmético; seed controlável; ticks explícitos; logs de eventos importantes. Replays com input gravado são ferramenta de QA, não devem depender de tempo de parede.

## Performance por projeto
**Micro**: Canvas 2D, assets vetoriais/raster locais, efeitos limitados.  
**Compact**: Canvas 2D/ WebGL conforme volume de sprites e efeitos.  
**Expanded**: WebGL2 ou motor externo se um benchmark do caso justificar o custo.

Evitar dependência de motor por moda. Quando migrar de motor, preservar contratos de gameplay e dados.
