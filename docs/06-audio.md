# 06 — Música, efeitos e feedback sonoro

## Princípio
Um jogo pequeno não precisa ser silencioso. Efeitos bem escolhidos podem trazer mais percepção de qualidade do que texturas enormes.

## Fontes
- **Procedural WebAudio**: osciladores, envelopes, filtros e ruído curto; bom para UI, impactos abstratos e pickups.
- **Samples comprimidos**: sons orgânicos e ambiências impossíveis de sintetizar com qualidade suficiente.
- **Música em loops**: arquivos compactados, padrões MIDI-like ou síntese por eventos; escolher após teste de qualidade.
- **Ambiente adaptativo**: camadas ativadas por intensidade ou estado.

## Regras operacionais
- Browsers normalmente exigem **gesto do usuário** antes de iniciar áudio.
- `AudioContext` deve ser criado ou retomado após interação.
- Nunca inicializar centenas de nós sem descarte.
- Limitar vozes simultâneas e priorizar sons relevantes.
- Respeitar mute/volume persistido.
- Ao perder foco, pausar o jogo e reduzir/suspender o áudio conforme UX.
- Considerar modo silencioso e sensibilidade auditiva.

## Eventos, não chamada direta
A simulação emite `player.attack`, `enemy.hit`, `pickup.collect`, `ui.confirm`; o sistema de áudio traduz eventos em sons com variação controlada. Isso facilita testes, remasterização e troca de backend.

## Paleta sonora
Definir até 5 motivos sonoros básicos e parâmetros de variação; não usar um som aleatório para cada evento. Alinhar duração e frequência à direção de arte. Evitar sons agressivos repetidos a cada frame.

## Otimização
- Limitar polifonia (ex.: 6–12 vozes dependendo do alvo).
- Empregar envelopes curtos e geradores compartilhados.
- Reutilizar buffers decodificados.
- Pré-carregar apenas recursos do primeiro nível.
- Medir tempo até som e falhas no primeiro toque.
- Verificar se a síntese consome CPU relevante no hardware-alvo.

## Critério de aceite
Volume ajustável, mute, retomada após pausa, nenhuma exceção por bloqueio de autoplay, SFX sincronizados e nenhuma explosão de volume causada por múltiplas colisões no mesmo tick.

## Audio Core v0.2 — módulo funcional derivado dos estudos do acervo

`demo/engine/audio.js` cria áudio procedural com WebAudio e **limite configurável de vozes simultâneas** (padrão 8), inicialização condicionada à interação, controle de mute e descarte de nós após o término. A camada é independente da lógica do jogo. `demo/game.js` utiliza esse módulo para todos os efeitos sonoros do Lumen Shift, com os sinais anteriores preservados.

`tests/audio_engine.test.cjs` utiliza AudioContext falso para validar criação sob demanda, limite de vozes, liberação após `onended`, validação de parâmetros, mute, indisponibilidade e contexto suspenso. Testes lógicos não validam qualidade perceptual, latência nem consumo de bateria; essas métricas permanecem abertas.

Não há importação ou reprodução dos arquivos MIDI/OTT de terceiros do corpus: os efeitos são sintetizados originalmente. A recorrência de áudios minúsculos em J2ME orienta a comparação futura de síntese versus arquivos comprimidos.
