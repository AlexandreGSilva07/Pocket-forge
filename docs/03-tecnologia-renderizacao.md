# 03 — Tecnologia, renderização e matriz de decisão

## Princípio
O melhor motor é o que entrega a experiência pretendida dentro do orçamento real de bytes, memória, CPU/GPU e manutenção. Nunca escolher tecnologia apenas pelo nome ou fama.

## Rotas suportadas conceitualmente

| Rota | Quando usar | Custo/risco |
| --- | --- | --- |
| Canvas 2D puro | arcade 2D, puzzle, shooters simples, efeitos customizados | portátil, pequeno; disciplina manual de cena/input |
| Canvas 2D + ferramentas de conteúdo | sprite-driven, animação rica, mapas tileados | atlas e streaming precisam de cuidado |
| WebGL2 direto | grande quantidade de partículas, shaders, 2.5D | contexto GPU, fallback e depuração mais complexos |
| LittleJS | jogo arcade rápido com utilitários de física/áudio/entrada | examinar tamanho e licença da versão escolhida |
| KAPLAY | mecânicas e composição declarativa | abstração maior, dependência adicional |
| Phaser | jogos 2D de maior escopo e ecossistema grande | bundle inicial geralmente mais pesado |
| Three.js | 3D verdadeiro e cena moderada | assets 3D, memória de GPU e shader compile dominam |

Essas são **candidatas**, não dependências incluídas. Verificar versão, licença, distribuição e tamanho no projeto concreto.

## Critérios de decisão pontuados
Pontuar cada alternativa de 0–5:
- Qualidade visual exigida (peso 3).
- Volume previsto de sprites/geometria e draw calls (peso 3).
- Payload total gzip/Brotli (peso 2).
- Maturidade, manutenção e facilidade de depuração (peso 2).
- Tempo de implementação do vertical slice (peso 2).
- Compatibilidade target/touch/offline (peso 3).
- Capacidade de testes automatizados (peso 2).

Multiplicar nota × peso e registrar a decisão. **Pontuação não substitui benchmark**.

## Escolha de resolução
1. Fixar coordenadas lógicas em pixels/unidades do mundo.
2. Definir política: `contain`, `cover` ou layout responsivo por HUD.
3. Ajustar backing size ao DPR, com teto configurável.
4. Testar paisagem e retrato somente se ambos forem alvo.
5. Medir custo do fill-rate; canvas 4K pode custar muito mais que 720p.

## Renderização de alto valor por baixo custo
- **Iluminação falsa**: gradientes, overlays e pontos de brilho sem shadow maps.
- **Paralaxe**: camadas deslocadas, pouca CPU.
- **Procedural**: gradientes, formas, padrões, ruído pré-computado.
- **Tween e easing**: grande sensação de polimento com poucos bytes.
- **Partículas pooladas**: emissões curtas e feedback audiovisual.
- **Screen shake breve**: acessibilidade exige opção reduzir movimento.
- **Shaders compactos**: somente quando custo GPU e portabilidade compensam.
- **Animação baseada em curvas**: interpolação e transforms podem substituir muitos frames raster.

## Anti-padrões
- Canvas com todo o conteúdo recriado em DOM a cada frame.
- Texturas enormes para arte pequena.
- Dependência apenas para um helper trivial.
- Geração procedural cara sem cache.
- Sombras gaussianas e blur em todas as entidades móveis.
- Renderização e lógica acopladas que inviabilizam testes.

## Teste de decisão
Comparar pelo menos duas rotas com a **mesma cena** se a decisão for crítica. Medir tempo de startup, JS transferido, draw time p50/p95, memória e compatibilidade. Documentar dispositivo, navegador, DPR, FPS alvo, contagem de objetos e limite de variância.
