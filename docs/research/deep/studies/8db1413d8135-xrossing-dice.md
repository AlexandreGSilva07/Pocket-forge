# Estudo dirigido de bytecode — Xrossing Dice

**JAR SHA-256:** `8db1413d8135bfc300525375ae0ff398548707d0d8f824cb610d797130e67c9d`

**Status:** `METHOD_REVIEW_PARTIAL` — métodos reais desmontados/interpretados, **não** jogo inteiro plenamente compreendido, portado ou executado. Ferramenta: OpenJDK 21 `javap -c -p` sobre binários originais enviados em conversa; recursos ZIP lidos sem executar MIDlets. Data: 15/10/2026.

### Evidência de bytecode real

- JAR enviado previamente pelo usuário e reidentificado pelo SHA-256 `8db1413d8135bfc300525375ae0ff398548707d0d8f824cb610d797130e67c9d`.
- `javap -classpath 1XCrossingDice.jar -c -p com.ixisoft.gxdice.nokia40.MinimaxRobot`: 25 classes no JAR.
- `MinimaxRobot.minimaxMove(GameController)`: percorre colunas quando `colRobot=true` e linhas caso contrário, chamando `minimaxValue` em alternativas selecionáveis. Começa a melhor avaliação em `Integer.MIN_VALUE` e escolhe o melhor índice.
- O método `minimaxMove` reduz temporariamente o horizonte `depthLimit` em **2 níveis** sob condição específica de início da partida (comparação entre turnos jogados e dimensão do tabuleiro), retornando ao limite quando o valor ficaria menor que **3**. Isso é um ajuste de custo da busca, não uma prova de tempo de resposta.
- `minimaxValue(GameController,int,boolean,int,int,int)`: ramificação recursiva **min/max** com limites alfa/beta. Operações de teste equivalentes a `alpha >= beta` provocam retorno antecipado. Métodos usam pontuação dos dois jogadores e detectam ausência de jogadas.
- O método preserva o valor anterior da célula, seleciona linha ou coluna, zera célula usada, atualiza pontuação e chama `undoMove(...)` em retorno normal e ao podar; `undoMove` restaura célula, seleção e pontuações originais. Esta é uma **estratégia mutação/desfazer**, diferente de copiar toda a posição em cada nó.
- Folhas e finais são avaliados por diferenças de pontuação; há **multiplicação por 1.000** em estados finais selecionados pelo bytecode. Não foi reconstruído o conjunto completo das regras de vitória ou as heurísticas de inicialização.

### Contribuição ao PocketForge

Implementado **código original** em `demo/engine/ai.js`: busca alfa-beta genérica com `applyMove`/`undoMove`, orçamentos de nós e profundidade e restauração do estado mesmo quando há erro. É uma adaptação arquitetural, **não um port das regras de Xrossing Dice**.

`demo/ai-lab.html` é um jogo original de tomada de peças para exercitar a API. Testes em `tests/ai_engine.test.cjs` validam melhor jogada, reversibilidade, teto de nós, poda e manejo de erro.

### Próximo estudo necessário

Investigar `GameController` e todos os caminhos terminais, comparar poda vs busca exaustiva, medir tempos em dispositivos reais e execução do jogo original em emulador. **Não houve emulação no presente estudo.**
