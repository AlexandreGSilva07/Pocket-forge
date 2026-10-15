# 13 — Tutorial operacional: primeiro jogo executável

## Pré-requisitos
Python 3.9+ para scripts, navegador moderno para demo, Node.js apenas para validação sintática opcional. Não há instalação npm para rodar Lumen Shift.

## 1. Executar a referência
```bash
git clone https://github.com/AlexandreGSilva07/Pocket-forge.git
cd Pocket-forge
python3 -m http.server 8000 --directory demo
```
Abrir `http://localhost:8000`. Clicar em **Jogar**, mover com WASD/setas ou toque e usar Space/dash. O jogo deve apresentar feedback ao atingir inimigos ou coletar orbes, terminar quando a vida chegar a zero e permitir reiniciar.

## 2. Derivar scaffold
```bash
python3 scripts/new_game.py ./meu-jogo --title "Aurora Runner"
python3 -m http.server 8001 --directory meu-jogo
```
O scaffold copia a demo e personaliza título. Ele **não cria automaticamente mecânicas diferentes**; o agente precisa implementar o design.

## 3. Gerar primeiros assets
```bash
python3 scripts/make_assets.py meu-jogo/assets --seed 42
```
Verificar SVGs em um visualizador/navegador. Esta ferramenta gera ícones abstratos e um fundo geométrico; não produz sprites de personagem animados.

## 4. Modificar a mecânica
- Escrever Game Brief antes de mudar tudo.
- Alterar parâmetros de velocidade, frequência e dano para aprender a estrutura.
- Implementar um novo objetivo (ex.: resistir 45 segundos) e atualizar HUD.
- Adicionar uma entidade e uma condição de colisão.
- Rodar e medir; não apenas olhar o diff do JavaScript.

## 5. Auditoria
```bash
python3 scripts/audit.py meu-jogo --json
python3 -m unittest discover -s tests -v
node --check meu-jogo/game.js
```
A saída lista bytes e gzip teórico. FPS e memória não são medidos por esses comandos.

## 6. Entregar com evidências
Produzir Evidence Report em `docs/08-qa-testes.md`. Abrir em desktop e telefone quando for alvo. Capturar erros reais e comunicar o que não foi possível testar.

## Erros frequentes
- **Tela vazia**: console JS, caminho `game.js`, CSS bloqueando Canvas ou erro de load.
- **Sem som**: o navegador pode bloquear áudio até primeira interação; verificar mute/volume.
- **Controles não respondem**: foco do navegador, pause state, viewport e `touch-action`.
- **Falhas em `file://`**: servir por HTTP local como no comando acima.
- **Pior FPS no celular**: DPR alto e demasiados efeitos; limitar resolução interna e reduzir partículas primeiro.
