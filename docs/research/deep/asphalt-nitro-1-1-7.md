# Asphalt Nitro 1.1.7 — engenharia reversa dirigida com validação real (fase A)

**Data:** 16/10/2026 · **Estado: leitor de bancos e ciclo de teclas portados parcialmente; jogo completo NÃO portado.**

## Entrada real e identidade

O usuário forneceu na Biblioteca o arquivo **AsphaltNitro.jar**:

- SHA-256: `a96827c5c6539bcaff2d7d23f8bad0cf1dafd8d421af38f97664a25c49fcd9cf`.
- 2.136.505 bytes; 56 entradas no ZIP/JAR, 21 arquivos `.class`.
- Manifest: Gameloft, `MIDlet-1: Asphalt Nitro, /icon.png, GloftASGM`, versão `1.1.7`, `CLDC-1.1`, `MIDP-2.0`, `SEMC-Screen-Size: 240,320`.
- A análise prévia particular do usuário havia catalogado 16 bancos, 1.310 registros, 348 sprites privados com marcador `DF 05` (após tag 2) e 928 registros binários não classificados. Também produziu um visualizador de sprites em HTML **não equivalente à lógica do jogo**.

## Trabalho 1 — reconstrução exata do contêiner Gameloft em JavaScript

Novo código original: [demo/engine/gameloft-banks.js](../../../demo/engine/gameloft-banks.js).

Os arquivos compactados dentro do JAR têm nomes `6`, `6.1`, `12`, `12.1` etc. O cabeçalho do arquivo-base é `uint16LE total`, `uint8 partes`, um byte reservado e uma tabela de `uint16LE inicio_de_cada_parte`. Cada parte tem uma tabela de `uint32LE` contendo **um offset adicional** para delimitar o último recurso. O arquivo-base começa sua tabela depois do cabeçalho; cada parte subsequente a inicia no primeiro byte. Os payloads preservam a tag original.

O leitor foi **testado contra os bytes reais do JAR** na sandbox, sem JVM: extraí todas as partes diretamente do ZIP/JAR, reconstruí cada registro pelo código JS e comparei contra o catálogo previamente gerado, exigindo **mesmo ID, tamanho, tipo e SHA-256 do payload**.

**Resultado:** 16 bancos, **1.310/1.310 registros equivalentes**, **zero divergências**. Exemplos: banco `6` = 810 registros e duas partes; banco `12` = 71 em cinco partes; banco `13` = 209 em sete partes.

Isso é equivalência de **extração de bytes**, não de renderização ou mecânica. Ainda não sabemos interpretar os 928 recursos binários nem converter `DF 05` em pixels diretamente via JS. O procedimento prévio usava a classe Java original `f.class` apenas na etapa offline de geração de sprites.

## Trabalho 1.5 — importar diretamente o JAR no navegador, sem Java

O módulo [demo/engine/zip-jar.js](../../../demo/engine/zip-jar.js) implementa leitura do diretório central ZIP, descompressão `stored`/`deflate-raw` via APIs nativas do navegador, limites de entrada e validação CRC32. Foi **testado com o próprio AsphaltNitro.jar na sandbox**: 56 entradas abertas, 16 bancos reconhecidos e 1.310 registros recuperados pelo pipeline JavaScript completo — **zero bytecode Java executado**. Testes públicos cobrem arquivos sintéticos (stored/deflate) e CRC corrompido. Importação de JAR é leitura/inspeção, **não emulação nem execução de corrida**.

## Trabalho 2 — semântica de entrada derivada de bytecode real

Em `j.class` inspecionado com `javap -c -p j`, observou-se:

- `j.run()` invoca `Canvas.repaint()` e `Canvas.serviceRepaints()`, além de controlar o ciclo com `Thread.sleep`/`yield`.
- `j.paint(Graphics)` usa `System.currentTimeMillis` para computar intervalo entre frames, limitado a 1000 ms, atualiza contadores de teclas, e invoca `f()` do jogo.
- `keyPressed`: ignora repetição de um contador positivo; incrementa até limite 126.
- `keyReleased`: converte contador positivo em negativo; etapa de paint observa negativo e retorna a zero; índices >= 18 recebem transição de pulso.

Portamos **apenas esse pequeno subsistema**, em [demo/engine/gameloft-input.js](../../../demo/engine/gameloft-input.js), com testes específicos. Não há evidência ainda para rotular aceleração, nitro ou IA como portados.

## Experimento Java-free executável

[demo/gameloft-bank-lab.html](../../../demo/gameloft-bank-lab.html) interpreta bancos locais, lista IDs, tipos, offsets, dump HEX, prévia PNG padrão e exportação de registros. Não usa Java/MIDP. Para testar com a cópia que o usuário possui:

```sh
unzip AsphaltNitro.jar 6 6.1
python3 -m http.server 8000 --directory demo
# Abrir http://localhost:8000/gameloft-bank-lab.html e selecionar 6 e 6.1
node --test tests/gameloft_*.test.cjs
```

**Esse laboratório não é jogo nem emulador**. O botão de arquivo espera **bancos já descompactados do JAR**, não o próprio arquivo `.jar`. Os testes versionados usam **fixtures sintéticas**; os checks com o JAR original são evidência particular desta investigação (não colocaremos binários comerciais na CI pública).

## Próximo marco técnico obrigatório

1. Reimplementar a decodificação de sprites Gameloft `DF 05` inteiramente em JavaScript, a partir do comportamento de `f.class`, e comparar os pixels resultantes (incluindo paleta e transparência) com capturas locais de referência.
2. Interpretar bancos binários de pistas/cenas e identificar, pelo fluxo de uso em `a`, `s` e auxiliares, os formatos que realmente governam perspectiva, terreno e objetos.
3. Portar a simulação real, física, efeitos, menus, IA, renderização e progressão; testar com traces determinísticos e jogo original observado em emulador (somente como oráculo).
4. Entregar o executável HTML/JS quando comportamento e imagens tiverem sido verificados; **não** reapresentar um clone aproximado ou uma visualização de assets como porte original.

## Dataset maior, sem importar ROMset comercial ao Git

O [M5-Dev/j2me-vault](https://huggingface.co/datasets/M5-Dev/j2me-vault) lista mais de 7,5 mil jogos, incluindo `Games/AsphaltNitro.jar` (**2.136.505 bytes**) e `Games/AsphaltNitro-1.jar` (**995.750 bytes**). Também há o [j2me-full-romset](https://huggingface.co/datasets/M5-Dev/j2me-full-romset) com 456 JARs e capturas. **Tamanho igual não prova hash igual** entre versões da mesma aplicação.

O script [scripts/fetch_j2me_sample.py](../../../scripts/fetch_j2me_sample.py) possibilita obter **amostras sob demanda** no diretório ignorado `external-corpus/`, com validação ZIP e hash. Este download não foi executado nesta fase; o JAR analisado veio da Biblioteca do usuário. É desnecessário e inadequado colocar 3,4 GB de jogos comerciais no repositório público. Licença do dataset não implica direitos sobre os próprios jogos.

**Integridade:** sem redistribuição de executáveis, arquivos comerciais, sprites ou decompilação integral. Não houve execução do JAR original nem testes de FPS, RAM, fidelidade de menus ou corrida. Continuamos comprometidos com o objetivo de criação de jogos HTML5 modernos originais, sem VM Java no runtime final.
