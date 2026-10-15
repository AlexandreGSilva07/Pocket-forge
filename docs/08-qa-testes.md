# 08 — QA, testes automatizados e evidências

## Modelo de qualidade
Separar cinco tipos:
- **Static**: sintaxe, imports, recursos e licenças.
- **Unit**: regras puras, estados, RNG, colisão, progressão.
- **Integration**: componentes e assets reais no runtime.
- **Functional gameplay**: entrada, pausa, objetivo, derrota, reset, sound unlock.
- **Visual & performance**: viewport, pixels relevantes, FPS e travamentos.

Nenhuma categoria substitui outra. Um workflow verde apenas com `node --check` valida sintaxe, não jogabilidade.

## Gates (G0–G5)
| Gate | Evidência mínima | Bloqueia entrega se falhar? |
| --- | --- | --- |
| G0: Build | arquivos, comandos, dependências resolvidas | sim |
| G1: Input | teclado/touch previstos controlam jogador | sim |
| G2: Gameplay | possível jogar, perder/ganhar, reiniciar | sim |
| G3: Visual | tela legível e sem arte faltando | sim |
| G4: Perfil | métricas definidas e medições no alvo | conforme escopo |
| G5: Licença/Offline | atribuições e teste sem CDN surpreendente | sim, se offline/licença exigir |

## Matriz mínima manual
| Caso | Passos | Esperado |
| --- | --- | --- |
| Primeiro load | iniciar HTTP local | menu inicial visível sem erro |
| Começar | clicar/tocar Começar | simulação inicia e HUD aparece |
| Movimento | setas/WASD e touch | avatar responde previsivelmente |
| Ação | Space/Enter ou botão touch | feedback observável |
| Colisão | atingir perigo | vida reduz, feedback ocorre |
| Falha | perder vidas | estado derrota |
| Reinício | clicar/tocar Reiniciar | score/vida/entidades reiniciados |
| Pausa | tecla/botão e voltar | tempo lógico congela corretamente |
| Áudio | iniciar com/sem mute | sem erro de autoplay, áudio respeita configuração |
| Offline | desabilitar rede após carregar | nenhuma dependência inesperada |

## Protocolo de QA visual
- 360×640, 390×844, 768×1024, 1366×768, tela retangular ampla.
- Viewport CSS ≠ resolução real: verificar DPR 1 e 2.
- Fazer screenshots **após** fontes/assets/estado estabilizados.
- Comparar imagens com baseline e diferenças relevantes, não apenas pontuação total.
- Testar contraste, orientação e botões que fiquem atrás de safe areas.
- Com redução de movimento ativada, remover shake/flashes excessivos.

## Reproduzibilidade
Registrar commit SHA, navegador, versão, sistema, devicePixelRatio, viewport, seed, número de ticks, ação e esperado. Arquivar logs, screenshots e vídeos quando necessário. Falhas intermitentes precisam de reprodução repetida.

## Modelo de Evidence Report
```md
# Evidence Report — <projeto>
Commit:
Build/run:
Testes executados e resultados:
Dispositivos/navegadores:
Controles testados:
Estados jogáveis observados:
Tamanho (bruto/gzip):
FPS p50/p95/p99 e método:
Memória e método:
Licença dos recursos:
Falhas reproduzidas:
Não verificado:
```

## Política de afirmações
- “**Compila**”: ferramenta de build ou parser executada.
- “**Roda**”: aplicação iniciada e observada em runtime.
- “**Jogável**”: entrada e gameplay exercitados com estados.
- “**Otimizado**”: comparado com baseline usando métrica.
- “**Completo**”: critérios de aceite cobertos por evidência.

## Suite v0.1
`tests/test_tools.py` cobre geração/auditoria; `node --check` valida sintaxe. `tests/browser_smoke.py` usa Playwright/Chromium no CI para iniciar, mover, pausar, retomar e acionar dash em desktop/touch; salva screenshots como artefatos de evidência. **Ainda não existe comparação automática de pixels com baseline**, avaliação humana/IA de imagens, teste em telefone físico ou medição de FPS. Essas lacunas permanecem no roadmap.
