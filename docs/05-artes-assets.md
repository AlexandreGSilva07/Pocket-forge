# 05 — Direção de arte e pipeline de assets

## Objetivo
Visual moderno e autoral com desempenho previsível. Pixel art é **uma opção**, nunca padrão obrigatório. Criar arte que pareça feita pelo mesmo estúdio, independentemente de ser vetorial, raster, low-poly ou híbrida.

## Art Bible mínimo
- **Pilares visuais**: por exemplo “neon sereno”, “formas orgânicas”, “contraste de ação”.
- **Paleta**: primária, neutros, acentos, alertas e estados de dano.
- **Formas**: silhueta de personagens e linguagem de cantos/arestas.
- **Profundidade**: regras de sombra, luz, paralaxe, desfoque e escala.
- **Tipografia**: família e fallback, contraste, tamanho mínimo responsivo.
- **Animação**: overshoot, duração, easing e limites de movimento.
- **Asset sheet**: personagem, inimigo, terreno e HUD lado a lado para medir consistência.

## Três fontes
### A. Procedural
SVGs, Canvas, geometria, ruído, gradientes, partículas, shaders e animações paramétricas. Ideal para ícones, efeitos, fundos, UI, efeitos luminosos e jogos abstratos. **Ferramenta v0.1:** `scripts/make_assets.py` gera alguns SVGs simples e originais, não produz automaticamente personagens complexos.

### B. Assistida por modelos generativos
Gerar conceitos e variações; depois revisar silhueta, consistência, recorte, resolução, transparência, direitos de uso e repetibilidade. Uma imagem bonita não equivale a spritesheet. Para animar: key poses → intervenções → alinhamento → frames → atlas → inspeção em movimento.

### C. Híbrida
Base procedural + pintura/IA + finalização vetorial/raster. Permite identidade rica sem assets gigantes. Manter arquivo-fonte e derivar versões otimizadas.

## Formatos e escolha
| Formato | Uso | Atenção |
| --- | --- | --- |
| SVG | ícones, UI, formas escaláveis | filtros caros; rasterizar quando necessário |
| WebP/AVIF | fundos e arte raster com compressão | validar suporte, custo de decode e transparência |
| PNG | sprites com arestas exigentes/alpha | frequentemente maior |
| JSON de atlas | coordenadas, pivôs e estados | versão e validação de paths |
| glTF/GLB | malha 3D comprimida | materiais, texturas e GPU ainda custam memória |

Não assumir que o menor arquivo tem o menor custo final de processamento.

## Convenção de nomes
`kind/name/variant/state`, por exemplo `character/runner/blue/idle`. Persistir atribuição de licença, fonte, prompt ou procedimento, versão, dimensões, escala base e autor em manifesto. Evitar nomes como `final_final_2.png`.

## Spritesheets
- Remover pixels transparentes e preservar `pivot` por frame.
- Empacotar por fase/tema, não um atlas único de 16K.
- Evitar bleeding por padding e sampler apropriado.
- Conferir frames, ordem, FPS de animação e transições.
- Testar em DPR 1, 2 e escalas fracionárias.

## Animação econômica
Em vez de 60 quadros completos:
- rig simples e interpolação de partes;
- squash/stretch em escala;
- particle trails procedurais;
- sombras elípticas;
- emissões pequenas e contextuais;
- reposicionamento e inclinação coerentes com física.

## Checklist visual
1. Jogador identificável em menos de um segundo.
2. Inimigos distinguíveis por silhueta e comportamento, não apenas cor.
3. Contraste suficiente em fundos dinâmicos.
4. Efeitos não escondem hitboxes.
5. UI funciona em viewport pequeno e alto DPI.
6. Transições preservam consistência de luz/paleta.
7. Redução de movimento disponível quando efeitos intensos.
8. Imagens originadas/licenciadas são documentadas.
