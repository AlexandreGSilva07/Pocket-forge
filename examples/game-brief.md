# Exemplo de Game Brief — Lumen Shift

**Pitch:** sobreviva em uma arena abstrata, desvie dos perseguidores, colete energia e use uma arrancada para escapar.  
**Gênero:** ação/arcade de arena 2D.  
**Plataforma:** navegador moderno; teclado e toque.  
**Pilar 1:** resposta imediata ao controle.  
**Pilar 2:** contraste entre perigo e recompensa.  
**Pilar 3:** visual luminoso geométrico de baixo custo.

## Loop
Iniciar → navegar → coletar orbes/evitar inimigos → aumentar pontuação e dificuldade → receber dano → perder vidas → derrota → reiniciar.

## Ponto de partida técnico
Canvas 2D e WebAudio sintetizado, nenhum pacote externo. Alvo aspiracional de até 1 MB transferido e 60 FPS. Esses valores precisam ser medidos no dispositivo-alvo, não presumidos.

## Controles
WASD/setas e apontador touch para mover; Space e botão Dash para impulso; P para pausar; M para silenciar. O teclado pode comportar-se diferente do touch devido à distância; avaliar separadamente.

## Critérios de aceite
- Menu renderiza e botão inicia.
- Jogador move em duas plataformas de input.
- Colisão provoca feedback e reduz vida.
- Score avança com tempo/colecionáveis.
- Derrota aparece e reiniciar limpa o estado.
- Sons não tocam antes da autorização de áudio.
- Auditor lista peso e ausência de dependências remotas.

## Não está incluído
Campanha, fases múltiplas, backend, multiplayer, app store, PWA, testes com aparelho físico e benchmark automatizado de FPS.
