# 10 — Receitas de gêneros, algoritmos e padrões visuais

Estas receitas são **estratégias de implementação**, não jogos completos. A escolha deve partir do Game Brief e da prova de diversão, não da facilidade de gerar código.

## Receita A: shooter de arena (micro/compact)
**Core loop:** navegar → esquivar → eliminar ameaça → coletar melhoria → sobreviver.  
**Sistemas:** input 8 direções; colisores círculo; inimigos por steering; spawn budget; projéteis poolados; HUD; score/combo; pausa; game over.  
**Arte:** silhueta clara, glow barato, trilhas, feedback de impacto e pequenos shake (opcional).  
**Balanceamento:** tempo médio até primeiro acerto, taxa de projéteis em tela e distância mínima para telegraph.  
**Gates:** invulnerabilidade após hit, colisão reproduzível, reinício sem vazamento de estado.

## Receita B: platformer de precisão
**Core loop:** mover → ler obstáculos → saltar → alcançar checkpoint.  
**Sistemas:** AABB e resolução por eixo, plataformas, coyote time, jump buffer, câmera, checkpoints, inimigos opcionais.  
**Armadilhas:** velocidade dependente de FPS; atravessar plataformas em dt alto; entrada touch imprecisa.  
**Gates:** testar 30/60/120Hz, parede, teto, duplo input e retomada após pausa.

## Receita C: corrida pseudo-3D
**Core loop:** conduzir → ultrapassar → desviar → concluir setor/volta.  
**Visual:** projeção em perspectiva de faixas de pista, sprites escalados por profundidade, skyline paralaxe, motion blur estilizado opcional.  
**Sistemas:** curvas por segmentos, posição lateral, velocidade, spawn de tráfego, colisão aproximada, HUD de tempo/velocidade.  
**Otimização:** desenhar apenas segmentos visíveis, distância de visão adaptativa, cache do fundo.  
**Gates:** pista sem descontinuidade, controles consistentes, 60 FPS no alvo, UI legível em alta velocidade.

## Receita D: RPG isométrico leve
**Core loop:** explorar → enfrentar desafio → ganhar recurso → melhorar equipamento.  
**Sistemas:** grade/waypoints, ordenação por coordenada de profundidade, hitboxes independentes, inventário orientado a dados, diálogos curtos, save versionado.  
**Arte:** tiles/reutilização de props, sombras simples e paleta por bioma.  
**Armadilhas:** escala de conteúdo cresce mais rápido que o motor; limitar vertical slice a uma sala, um inimigo e um objetivo.

## Receita E: puzzle minimalista
**Core loop:** compreender regra → experimentar → receber feedback → aprender variação.  
**Sistemas:** estado puro e testável, undo/restart, animações curtas, input claro.  
**Arte:** identidade de cor e forma; evitar depender apenas de cor para sinalizar estado.  
**Gates:** possibilidade de vencer testada por solver ou rota manual reproduzível.

## Receita F: micro-3D/low-poly
**Core loop:** navegação e interação em arena reduzida.  
**Tecnologia:** WebGL/Three.js só se benchmark justificar.  
**Assets:** malhas simples, atlas de materiais, luz baked/vertex colors.  
**Gates:** draw calls, shader compilation, memória de texturas, perda/restauração de contexto GPU.

## Padrões reutilizáveis
- **Object pooling** para partículas/projéteis.
- **Spatial grid** para colisões amplas.
- **Behavior trees pequenos ou FSMs** para IA de inimigos.
- **Data-driven waves** para dificuldade.
- **Tweak panel de desenvolvimento** para ajustar parâmetros sem rebuild.
- **State snapshot** para replay, depuração e testes.
- **Event bus restrito** para SFX/HUD; não espalhar eventos globais arbitrários.
- **LOD estético**: reduzir brilho, partículas e resolução interna sem remover pistas de gameplay.

## Teste de seleção da receita
Fazer um protótipo jogável de 30 segundos com um inimigo/obstáculo; abandonar a receita se a fantasia central não aparecer nesse intervalo. Não expandir fases para mascarar um loop pouco interessante.
