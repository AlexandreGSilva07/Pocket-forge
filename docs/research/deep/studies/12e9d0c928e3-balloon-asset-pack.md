# Engenharia reversa dirigida — 3D Balloon Race: contêiner de sprites PNG

**JAR original:** `828 Java Games/3DBalloonRace.jar`  
**SHA-256:** `12e9d0c928e3887efec1e44a467ab592fc4d42194fb95540ef8f8c680d51ba93`  
**Tamanho:** 117.888 bytes · **Status:** `METHOD_REVIEW_PARTIAL`.

Este estudo utilizou **bytes reais do JAR**, `zipfile`, `Pillow` apenas para identificar cabeçalhos/formatos de imagens e `javap -p -c` em classes reais. Não foi executado em emulador e não representa compreensão do motor gráfico completo.

## Descoberta #1 — vários PNGs independentes no mesmo recurso

Os arquivos dentro do JAR chamados `m`, `q` e `l0`–`l3` **não são PNGs isolados**. Eles começam com dois bytes big-endian que informam o tamanho da próxima imagem PNG, seguidos pela assinatura padrão de PNG. A sequência se repete para imagens consecutivas.

Exemplos comprovados:

| Recurso | Bytes | Estrutura observada | PNGs identificados |
|---|---:|---|---:|
| `m` | 6.072 | Sequência exclusiva de imagens com prefixo de 2 bytes | **3** |
| `q` | 28.192 | Sequência exclusiva de imagens com prefixo de 2 bytes | **53** |
| `l0` | 21.309 | Três PNGs seguidos de outros dados | 3 inicialmente |
| `l1` | 19.752 | Três PNGs seguidos de outros dados | 3 inicialmente |
| `l2` | 22.240 | Três PNGs seguidos de outros dados | 3 inicialmente |
| `l3` | 23.271 | Três PNGs seguidos de outros dados | 3 inicialmente |

O arquivo `m` contém PNGs indexados por paleta com dimensões **158×49, 158×49 e 90×18**. O arquivo `q` começa por PNG paletizado **81×384** e contém outros 52 PNGs, encerrando precisamente ao fim dos 28.192 bytes.

Em `l0`, o primeiro comprimento é `01 AE` (430), seguido de PNG de exatos 430 bytes; o segundo é `05 83` (1.411), seguido de PNG de 1.411 bytes; o terceiro tem 2.768 bytes. Há dados não PNG depois: **não se deve afirmar que todo `l0` é uma sequência PNG homogênea** sem entender as outras seções.

### Verificação da implementação no bytecode

O método `a.a(DataInputStream,boolean)`, identificado por `javap -classpath 3DBalloonRace.jar -c -p a`, executa:

- Condicional `boolean` que chama `DataInputStream.readShort()` para obter o comprimento (ou usa o padrão 4096);
- Aloca `byte[]` desse tamanho e faz `read(byte[])`;
- Chama `Image.createImage(byte[],0,len)`.

Essa cadeia confirma diretamente **comprimento + bytes da imagem + decodificação**, além da evidência de alinhamento encontrada em `m` e `q`. O código usa `read`, não `readFully`; portanto a rotina original pode não lidar robustamente com leituras parciais. Um leitor moderno deve validar truncamento estritamente.

## Descoberta #2 — leitor separado de dados compactados

`a.a(DataInputStream)` (retorno `byte[]`) lê um `readShort()`, aloca o bloco de entrada e depois cria buffer de **7.500 bytes**. No laço observa o bit alto (`AND 128`) e emprega o valor `AND 127` para um contador de repetição, avançando o índice de saída. É **um candidato forte a formato RLE de contagem com sentinela**, mas seu significado completo depende do campo de configuração `c.l`, que ainda precisa ser reconstruído. Não anunciar equivalência do novo codec sem vetores originais de teste.

## Consequências para o motor PocketForge

Novo arquivo `demo/engine/assets.js`:

1. `legacyEntries` lê sequências históricas `[u16 BE tamanho][bytes]` com limites e verificação de formato opcional, útil em futuros testes de compatibilidade.
2. `encode/decode` especificam um formato **novo, independente e versionado** `PFB1`, com nome mágico, quantidade de registros, tipo e comprimento uint32 BE, aceitando PNG e dados binários.
3. `demo/assets-lab.html` gera três sprites próprios, comprime como PNG, empacota, recupera e desenha no Canvas. Nenhum sprite ou áudio do jogo comercial foi reutilizado.
4. Testes cobrem recuperação exata, mistura PNG/binário, corrupção de tamanhos, limite de entradas e integridade do pacote.

A concatenação não necessariamente comprime os bytes dos PNGs; sua principal vantagem é **organizar múltiplos recursos em um único blob, com índices e leitura sob demanda**. Há custos de download e decodificação de imagens no navegador que precisam ser medidos.

## Reprodução local do achado, sem redistribuir arte

```bash
sha256sum 3DBalloonRace.jar
javap -classpath 3DBalloonRace.jar -c -p a
```

Para verificar a sequência de PNGs, ler cada comprimento com `int.from_bytes(data[offset:offset+2], "big")`, validar o cabeçalho `89 50 4E 47 0D 0A 1A 0A` imediatamente depois e avançar `2+comprimento`. Para imagens paletizadas, abrir apenas a fatia validada com Pillow e inspecionar `Image.mode == "P"`.

**Limites:** sem execução do jogo original, sem instrumentação de RAM/FPS, sem identificação integral dos blocos mistos `l0-l3` e sem reconstrução do RLE `a(DataInputStream)`. Este é um estudo parcial de métodos e formatos, com implementação independente.
