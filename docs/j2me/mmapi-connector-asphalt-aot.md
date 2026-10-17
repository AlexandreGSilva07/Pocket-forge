# PocketForge — MMAPI, Connector e Asphalt Nitro compilado no navegador

**Verificação experimental: 16 de outubro de 2026, Chrome no computador do usuário.**

## Resultado comprovado

O compilador AOT baseado no **TeaVM 0.16.0** agora gera um **único arquivo HTML** a partir do JAR original de Asphalt Nitro 1.1.7, sem carregar o JAR ou uma VM interpretadora Java no navegador. A compilação terminou com **zero símbolos de API ausentes**. O HTML, com JavaScript e recursos incorporados, tem aproximadamente **10,7 MB**.

O arquivo foi executado diretamente por **`file://`**, sem servidor local, CDN, rede ou Java instalado no navegador. Capturas automáticas e inspeção de pixels verificaram:

- **Menu original**: INSTANT PLAY, CAREER, FREE PLAY, MY RECORDS e OPTIONS.
- **Navegação real por teclado**: ao **segurar** ArrowDown e a tecla 5, o jogo avançou pelos menus. Uma tecla muito breve não necessariamente é observada pelo loop de atualização do JAR.
- **Fluxo seguinte**: confirmação/tutorial, instrução textual e **imagem de carro vermelho em cenário com perspectiva 3D** (gerada pelo código original compilado, não mockup).
- Canvas **240×320**, milhares de cores. Em torno de 14 s de inspeção, houve **zero exceções JavaScript de página** e **zero requisições externas**.
- O jogo criou cerca de **25 elementos de áudio**; duas tentativas emitiram `MMAPI playback failed: The element has no supported sources` no teste estendido, portanto **não se comprovou reprodução sonora completa**.

**Limite importante**: nem o movimento do carro nem uma corrida jogável até o fim foram comprovados. O tutorial ainda permaneceu sobre a cena nos testes posteriores de aceleração/direção; o motor e o suporte às APIs são **experimentais**, não uma certificação de compatibilidade completa.

O HTML final **privado** pode ser aberto com duplo clique, sem servidor, em:
`~/Downloads/PocketForge-Asphalt-Nitro-AOT-Compilado.html`.
Os screenshots e scripts de teste ficam em `~/projetos/PocketForge-Research/asphalt-aot-probe/`, **fora do GitHub** para não distribuir conteúdo protegido.

## Reimplementações genéricas da plataforma — não remendos por título

As 6 dependências de plataforma que faltavam na compilação anterior foram abordadas em componentes **compartilhados**:

### javax.microedition.media — MMAPI

`Manager.createPlayer(InputStream,String)` cria `BrowserPlayer` conectado a `HTMLAudioElement`, carregando bytes da stream como data URI, sem acesso à rede. `Player` implementa estados UNREALIZED → REALIZED → PREFETCHED → STARTED, `start`, `stop`, `close`, `setMediaTime`, `getMediaTime`, `setLoopCount`; os controles de volume, rate e tempo têm valores e métodos próprios.

- Tipos previstos: WAV, MP3, OGG e MP4 áudio **quando o navegador os decodificar**.
- Alguns formatos contidos nos JARs antigos não são suportados por Chrome. A reprodução pode depender de gesto de usuário; a falha de `audio.play()` é assíncrona e registrada, não prova de áudio tocando.
- Não há suporte a MIDI/JAM, síntese, instrumentos proprietários, e tampouco um MMAPI universal validado.

### javax.microedition.io — Generic Connection Framework

O método `Connector.open` foi implementado com despachante de protocolos **explicitamente restrito**. `resource:` abre streams somente de leitura de recursos que o compilador incorporou do JAR. `file:`, `socket:` e outros protocolos não suportados falham com `IOException` clara, em vez de simular acesso ao filesystem do PC. A API JSR-75 completa ainda falta.

### Canvas e teclado

`Canvas` reconhece setas, números de keypad e softkeys F1/F2, além de eventos `pointerdown`, `pointerup` e `pointermove` enviados ao código Java compilado. O gerador adicionou botões genéricos visíveis ao HTML, sem necessidade de editar cada jogo. O arquivo continua autocontido e offline.

## Ensaios automáticos independentes

`tests/browser_j2me_aot_compiler.py` compila **oito JARs autorais diferentes** e valida cada HTML via `file://` no Chromium:

1. Matemática/controle de fluxo (resultado numérico exato).
2. Recursos do JAR via `ClassLoader.getResourceAsStream`.
3. MIDP Canvas e texto/desenho.
4. Entrada por teclado, mouse e keypad na página.
5. Clipping/translação/ARGB/regiões verificadas por pixels.
6. PNG original embutido e lido via `Image.createImage`.
7. `Connector.open(resource:)` e erro controlado para caminhos `file:`.
8. WAV criado nos testes, MMAPI state machine, volume, velocidade, start/stop/close e objeto áudio real do Chrome.

O teste exige **zero erros de página e zero requisições externas**. Os recursos de áudio de teste são gerados durante a execução: **não são distribuídos jogos comerciais**.

## Fontes históricas e licenciamento

O trabalho foi informado pela inspeção local de phoneME e j2me.js (GPLv2), FreeJ2ME, JS2ME e TeaVM. Os repositórios históricos permanecem isolados em `~/projetos/PocketForge-Research/upstream/`; **nenhum código GPL, jogo comercial ou firmware foi adicionado ao PocketForge**. A biblioteca implementada é independente e os componentes de terceiros têm suas próprias licenças.

## Próximos bloqueios reais

1. Identificar o motivo de o tutorial continuar bloqueando aceleração/conclusão da corrida e verificar toques/softkeys sem criar condicionais para Asphalt no compilador.
2. Validar os callbacks e o ciclo de vida de áudio, codecs J2ME históricos e o erro assíncrono de reprodução.
3. Implementar conectores filesystem de modo seguro, com armazenamento virtual, sem violar políticas do navegador.
4. Adicionar `Image.createImage(byte[],offset,length)` e suporte mais fiel a formatos de recursos. Incluir testes diferenciais contra o emulador de referência.
5. Aplicar regressões a mais jogos independentes antes de reivindicar **compatibilidade universal**.

**Regra permanente:** correções de comportamento pertencem às APIs compartilhadas do PocketForge, jamais a um bloco `if jogo == Asphalt`.
