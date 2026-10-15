# 17 — Design system de jogos compactos

## A interface também é gameplay
UI não é só decoração. Ela transmite regras, risco, progresso e as próximas ações. Uma interface leve deve reduzir ambiguidade, não minimizar pixels indiscriminadamente.

## Tokens de design
Definir: cores por função (`surface`, `primary`, `danger`, `reward`), escalas de tipografia, bordas, espaçamentos, curvas, contraste e tempo de animação. Tokens devem viver em um único arquivo por jogo. Para Canvas puro, espelhar tokens sem duplicação incoerente em JS e CSS.

## Hierarquia
1. **Ameaça imediata** (inimigo, hazard, telegraph).
2. **Jogador e espaço navegável**.
3. **Objetivo e recompensa**.
4. **HUD prioritário** (vida, munição, tempo).
5. **HUD secundário** (score, combo, recorde).
6. **Ambiente/decorativos**.

O que importa mais para a decisão precisa vencer o fundo em contraste, tamanho e movimento. Beleza não justifica esconder interação.

## Layout responsivo
- Safe areas `env(safe-area-inset-*)`.
- Touch targets grandes, sem colocar ação perto da navegação do sistema.
- HUD em DOM quando acessibilidade/seleção/navegação compensam; Canvas para mundo.
- Testar viewport estreito e paisagem, inclusive teclado aberto quando há input textual.
- Não assumir que `100vh` equivale à área visível em celulares; testar `100dvh`.

## Movimento e conforto
- Preferir animação de transform e opacidade.
- Respeitar `prefers-reduced-motion`.
- Evitar flashes fortes e tremores contínuos.
- Oferecer controles configuráveis se o gênero exigir timing preciso.
- Garantir pausa e áudio silenciado.

## Estados de interação
Todo botão precisa de: normal, foco, ativo, desabilitado, loading quando necessário e feedback de acionamento. Um clique sem resposta pode parecer bug mesmo que o estado tenha mudado internamente.

## Acessibilidade prática
Contraste suficiente, sinais redundantes além da cor, elementos interativos rotulados, controles via teclado, escala tipográfica e opção de reduzir movimento. Jogos muito rápidos podem demandar modo de dificuldade/assistência.

## Checklist
- O jogador sabe onde está?
- O objetivo atual é perceptível sem ler um manual extenso?
- O dano é distinguível do pickup?
- O estado pausa/derrota é inequívoco?
- Nenhuma camada tapa controles?
- Os padrões visuais permanecem legíveis após compressão/escala?
