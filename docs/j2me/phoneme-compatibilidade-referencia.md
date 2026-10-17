# Referência real Java ME — phoneME, j2me.js e compilador PocketForge

**Investigação executada no computador do usuário em 16/10/2026.** O objetivo permanece geral: **receber JARs Java ME e gerar HTML autônomo**, independentemente do fabricante, modelo Nokia ou nome do jogo. Não existem patches específicos de Asphalt Nitro neste trabalho.

## Fontes reais obtidas para análise, fora do repositório

Os códigos ficaram em `~/projetos/PocketForge-Research/upstream/`. Não foram incluídos como código-vendorizado no Git público.

| Código-fonte | Revisão observada | O que fornece | Distribuição |
|---|---|---|---|
| [phoneME](https://github.com/magicus/phoneME) | `5a13f65` | Implementações originais de CLDC, MIDP, RMS, MMAPI, bibliotecas JavaCall e componentes nativos de referência | GPLv2 nos arquivos examinados; não integrado ao PocketForge |
| [j2me.js / PluotSorbet](https://github.com/andreasgal/j2me.js) | `46ee3e7` | Máquina virtual JavaScript de Mozilla com integração com classes phoneME e trabalho AOT histórico | GPLv2 no repositório examinado; não integrado |
| [JS2ME](https://github.com/szatkus/js2me) | `828b81b` | Interpretador/JIT JavaScript MIT usado pelo modo **RUN** anterior | MIT |
| [FreeJ2ME](https://github.com/hex007/freej2me) | `eb4ac87` | Emulador de referência de API Java ME em Java | Referência separada; verificar licença de cada componente |
| [SquirrelJME](https://github.com/SquirrelJME/SquirrelJME) | `877513f` | Implementação alternativa de VM e bibliotecas Java ME | Referência separada |
| [TeaVM](https://github.com/konsoletyper/teavm) | `cfc0ce2` | Compilação antecipada de classfiles Java para JavaScript | Apache-2.0; já integra o núcleo AOT |

**Limite técnico:** phoneME foi projetado historicamente para arquiteturas e camadas de portabilidade próprias (JavaCall/PCSL, Linux ARM/i386, Windows i386). Baixar sua árvore e firmware Symbian **não equivale a executar os binários ARM/Symbian em um navegador**. Portar integralmente essa pilha para WebAssembly envolveria VM, bindings nativos, gráficos, multimídia, armazenamento e serviços de plataforma. O código de referência prova como as APIs são definidas e implementadas, mas a compatibilidade precisa ser exercitada por testes.

**Limite jurídico:** as fontes originais GPL foram mantidas isoladas para estudo, sem copiar implementação GPL para as classes independentes do PocketForge. Se algum dia for decidido distribuir phoneME/j2me.js integrados no runtime, será necessária uma estratégia de licenciamento explícita.

## Implementação geral — não específica de jogos

No compilador AOT [`scripts/compile_j2me_aot.py`](../../scripts/compile_j2me_aot.py) e na biblioteca [`compiler/teavm-aot/src/main/java/javax/microedition/`](../../compiler/teavm-aot/src/main/java/javax/microedition/lcdui/Graphics.java):

- **MIDP Graphics:** operações `setClip`, `clipRect`, consulta de clip, `translate`, `getTranslateX/Y`, `fillTriangle`, `drawRGB` com ARGB e `drawRegion`, integradas a Canvas e superfícies offscreen. A semântica de translação e clip foi testada com coordenadas/pixels exatos. Alguns recursos ainda são simplificados, por exemplo arcos e todos os tipos de transformação.
- **MIDP Image:** `createRGBImage`, `getRGB`, superfícies e cópia de pixels. O compilador pré-decodifica PNG/JPEG/GIF/BMP reconhecidos, possibilitando `Image.createImage("/caminho.png")` **síncrono** no Java compilado, com PNG de teste validado por bytes/pixels no Chrome. Imagens inválidas e formatos proprietários ainda precisam de tratamento.
- **Recursos genéricos dentro do JAR:** `GameResourceSupplier` registrado como serviço do TeaVM inclui os arquivos de recurso na compilação; `ClassLoader.getResourceAsStream()` leu um arquivo original do JAR durante um teste em Chrome `file://` sem conexão. O JAR completo não é embutido; os **recursos utilizados podem ser incluídos**, e sua licença deve ser respeitada.
- **Validação automática:** seis pequenos JARs autorais compilados a HTML, sem bytecode/JVM/servidor em runtime: algoritmo numérico, Canvas, teclado, desenho ARGB/clip, carregamento de arquivo binário, imagem PNG. A bateria de Chromium afirma pixels, tamanhos, texto e zero requisições de rede.

Os testes ficam em `tests/browser_j2me_aot_compiler.py` e são executados pelo workflow `.github/workflows/j2me-aot-compiler.yml`. Nenhum firmware, ROM comercial, JAR de jogo comercial nem código GPL é colocado no Git.

## Medição real de cobertura — Asphalt Nitro 1.1.7

O JAR original fornecido/estudado tem SHA-256 `a96827c5c6539bcaff2d7d23f8bad0cf1dafd8d421af38f97664a25c49fcd9cf`. O compilador produzia **19 símbolos ausentes** antes deste estudo. Após implementar 13 símbolos gráficos gerais, uma nova tentativa real encontrou **6 símbolos ausentes**:

- `javax.microedition.io.Connector`
- `javax.microedition.media.Controllable`
- `javax.microedition.media.Manager`
- `javax.microedition.media.Player`
- `javax.microedition.media.control.RateControl`
- `javax.microedition.media.control.TempoControl`

São requisitos da plataforma (MMAPI/IO), não nomes de métodos internos do Asphalt. Ter apenas uma definição vazia desses tipos poderia satisfazer a compilação, mas **não seria suporte funcional**; implementar comportamentos completos e testá-los é o próximo marco.

**Situação comprovada:** o núcleo AOT continua compilando JARs independentes e verificando comportamento em Chrome. **Asphalt Nitro ainda não compila na modalidade AOT e não existe corrida jogável**, nem prova de compatibilidade com todos os aparelhos ou extensões JSR.

## Próximas entregas verificáveis

1. Implementar MMAPI de forma independente com contratos de `Player` e `Manager`, testes reais de áudio, clock, estados e controles, e falhas explícitas para codecs não suportados.
2. Resolver armazenamento RMS persistente e I/O conforme APIs CLDC, JSR 75 e políticas de segurança do navegador; padronizar perfis de aparelhos sem perfis específicos por título.
3. Implementar imagem binária `Image.createImage(byte[],...)`, clipping e transformações plenamente aderentes e imagens/pistas proprietárias por seus decodificadores gerais, sem hacks para Asphalt.
4. Incluir conjunto diversificado de jogos e testes diferenciais contra uma implementação Java ME de referência, usando capturas e interações reproduzíveis.
5. Só considerar o compilador universal dentro de um **perfil de APIs declarado e testado**. Nenhuma máquina pode garantir compatibilidade com extensões desconhecidas apenas por conhecer o formato do bytecode.

## Fontes verificadas

- [Oracle — Graphics MIDP 2.0](https://docs.oracle.com/javame/config/cldc/ref-impl/midp2.0/jsr118/javax/microedition/lcdui/Graphics.html)
- [TeaVM — extensão ResourceSupplier](https://teavm.org/docs/runtime/compiler-extensions.html)
- [TeaVM — arrays em JavaScript, JSByRef](https://teavm.org/docs/runtime/jso.html)
- [phoneME — documentação de build Linux i386 / ARM](https://phonej2me.github.io/content/mr2/index_feature.html)
