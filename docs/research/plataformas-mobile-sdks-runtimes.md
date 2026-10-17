# Catálogo de plataformas móveis históricas, SDKs e runtimes para engenharia de jogos ultraleves

**Pesquisa:** 16/10/2026 · **Estado:** curadoria de fontes, não execução de ferramentas, validação de arquivos nem benchmark.

> **Propósito:** apoiar engenharia reversa, observação de comportamento, identificação de formatos e estudo de restrições dos jogos móveis antigos para desenvolver **jogos HTML5 modernos, originais e ultraleves**. O PocketForge **não é um emulador, não pretende rodar necessariamente Java/Symbian e não é orientado a um Nokia específico**. A escolha inicial do Nokia 5320 XpressMusic (Symbian OS 9.3 / S60 3rd Edition FP2) foi **apenas um exemplo relativamente avançado de sua geração**, não uma restrição técnica, aparelho-alvo nem stack preferencial.

## Como ler as evidências

- **Fonte localizada** significa que a página/repositório descrito foi encontrado e inspecionado; **não** significa que o download foi baixado, que o executável abre hoje ou que toda API funciona.
- **Download listado** significa que um arquivo está mencionado em página oficial/arquivo público; integridade, hash, licença, dependências, compatibilidade e malware **não foram testados**.
- **Código-fonte disponível** não implica que se possa redistribuir componentes ou aproveitar código no motor MIT do PocketForge; examinar licença, dependências, patentes e proveniência.
- **SDK de desenvolvimento**, **runtime/VM**, **firmware/ROM**, **emulador** e **biblioteca de API** são peças diferentes. Um SDK pode conter emulador de desenvolvimento sem conseguir rodar todo JAR/SIS comercial; firmware não é uma ISO genérica; JVM de desktop **não é** runtime CLDC/MIDP.
- Nas comparações, separar **tamanho transferido do jogo**, **tamanho do runtime**, **tamanho do firmware**, **uso real de RAM**, **custo CPU/GPU**, **fidelidade visual** e **latência**. Não atribuir ao jogo economias produzidas pela VM ou pelo sistema.
- Recursos proprietários externos ficam **somente referenciados**: não adicionar SDKs, ROMs, JARs comerciais, assets, decompilações completas ou instaladores ao Git.
- O ambiente de testes de softwares antigos deve ser isolado (idealmente VM offline), sem privilégios e com hashes; executáveis sem manutenção podem ter vulnerabilidades.

## 1. Java ME/J2ME: base transversal prioritária

J2ME/Java ME foi usado em múltiplas marcas e sistemas, **não apenas Symbian**. Para jogos típicos do acervo, procurar CLDC 1.0/1.1, MIDP 1.0/2.0/2.1, JTWI (JSR 185), MSA (JSR 248) e APIs opcionais. **JSR 184** = Mobile 3D Graphics (M3G); **JSR 226** = gráficos vetoriais SVG; **JSR 239** = bindings OpenGL ES; APIs opcionais **não** são automaticamente implementadas em todo aparelho ou SDK.

| Recurso | Natureza e utilidade | Link | Estado |
| --- | --- | --- | --- |
| Sun Java Wireless Toolkit 2.5.2_01 (Windows/Linux) | SDK + emulador de dispositivos CLDC/MIDP; build, depuração, testes e exemplos de MIDlets | [Arquivo Oracle](https://www.oracle.com/java/technologies/java-archive-downloads-javame-downloads.html) · [descrição oficial](https://www.oracle.com/java/technologies/sun-java-wireless-toolkit.html) | Página e arquivos listados; **instalação não testada** |
| Sun Java ME SDK 3.0 (Windows/Mac) | Sucessor do WTK, emulação e desenvolvimento CLDC/CDC; ambiente típico Win XP/Vista | [Arquivo Oracle](https://www.oracle.com/java/technologies/java-archive-downloads-javame-downloads.html) · [guia oficial](https://www.oracle.com/java/technologies/java-me-sdk-v3.html) | Página e arquivos listados; **instalação não testada** |
| Documentação técnica Java ME | Uso de JSR 184 (3D), JSR 226 (SVG) e JSR 239 (OpenGL ES), exemplos e modos de renderização | [Guia oficial JSRs](https://docs.oracle.com/javame/dev-tools/jme-sdk-3.0-win/html-helpset/z40010bc30131.html) · [portal de documentos](https://docs.oracle.com/javame/developer/developer.html) | Páginas acessíveis |
| phoneME Feature MR2 (2007) | **Código-fonte e binários** CLDC 1.1/MIDP 2.1 para Linux ARM/x86 e Windows x86; ótima referência para VM, ciclo de MIDlet, heap, gráficos e carregamento | [Downloads históricos MR2](https://phonej2me.github.io/downloads_previous.html) · [fonte Git preservada](https://github.com/magicus/phoneME) | Fonte e downloads listados; execução não testada |
| phoneME Feature MR3/MR4 | Implementações históricas mais novas; MR3 (2008) CLDC 1.1.1/MIDP 2.1; MR4 (2009) estende APIs; plugins binários separados | [MR3 / histórico](https://phonej2me.github.io/downloads_previous.html) · [MR4 e phoneME Advanced](https://phonej2me.github.io/downloads_page.html) | Downloads listados, plugins/licenças a conferir |
| phoneME Advanced | Outra família: CDC + Foundation/Personal Profiles, **não substitui diretamente CLDC/MIDP de jogos de feature phones** | [phoneME Advanced](https://phonej2me.github.io/downloads_page.html) | Fonte histórica listada |
| FreeJ2ME | Emulador aberto com frontends AWT/SDL2/libretro; importante para observar MIDlets do corpus sob entrada/resoluções conhecidas | [Código e instruções](https://github.com/hex007/freej2me) | Repositório verificado; jogo original não testado |
| FreeJ2ME-Pro | Fork com foco em extensões Nokia DirectGraphics, JSR 184 e Mascot Capsule; verificar diferença real por teste | [Código](https://github.com/digitalgust/freej2mePro) | Repositório verificado; compatibilidade não aferida |
| J2ME Loader | Emulador Android aberto; documenta compatibilidade 2D/3D, controles, perfis e suporte a Mascot Capsule | [Código](https://github.com/nikita36078/J2ME-Loader) | Repositório verificado; execução não testada |
| SquirrelJME | Implementação independente com alvo Java ME 8 e preservação de software antigo; **incompleta e não equivalente a um runtime MIDP 2.1 de produção** | [Código e limitações](https://github.com/SquirrelJME/SquirrelJME) | Repositório verificado |

**Precisão histórica:** a página oficial do WTK 2.5.2 explicita **MIDP 2.0 (JSR 118)** nas APIs implementadas; não presumir que seu emulador equivale ao ambiente **MIDP 2.1** do phoneME MR2 nem ao runtime proprietário do Nokia. SDK e implementação de Java ME podem fornecer diferentes JSRs.

### Arquivos phoneME MR2 concretos (índice histórico, não downloads validados)

Na [página de versões anteriores](https://phonej2me.github.io/downloads_previous.html), a versão MR2 b23 de 08/05/2007 lista:
- `phoneme_feature-mr2-rel-src-b23-08_may-2007.zip` — código-fonte, **17.419.455 bytes**.
- `phoneme_feature-mr2-rel-bin-b23-win-08_may_2007.zip` — Windows/x86, **5.342.365 bytes**.
- `phoneme_feature-mr2-rel-bin-b23-linuxarm-08_may_2007.zip` — Linux/ARM, **5.379.672 bytes**.
- `phoneme_feature-mr2-rel-bin-b23-linuxx86-08_may_2007.zip` — Linux/x86, **5.283.505 bytes**.

Esses tamanhos são **dos ZIPs**, não tamanhos da VM em RAM, do firmware ou de um MIDlet. O repositório Git [magicus/phoneME](https://github.com/magicus/phoneME) informa requisitos antigos de build (incluindo toolchain capaz de gerar binários i686 e Java bytecode antigo).

## 2. Symbian, S60, UIQ, N-Gage, Series 80/90: família de SDKs, não um só modelo

| Família | Exemplos localizados | Fonte | Possível aplicação |
| --- | --- | --- | --- |
| S60 1st/2nd Edition | S60 0.9/1.2 (Symbian 6.1), 2.0/2.1 FP1 (7.x), 2nd FP2 (8.0) | [S60 / S80 / S90 SDKs](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Series.md) | Estudar gráficos, áudio e limites pré-Symbian 9 |
| S60 3rd Edition | SDK v3 1.0 (Symbian 9.1), v3 1.0.1 (9.2), **v3.2 1.11 (9.3, jul/2008)** | [Arquivo histórico](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Series.md) | C++ nativo, ferramentas EPOC e APIs S60; **não** confundir com SDK Java ME universal |
| S60 5th | SDK v5 1.0.1 (Symbian 9.4, mar/2009) | [Arquivo histórico](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Series.md) | Comparar evolução de UI, gráficos e touch |
| Symbian^3 / Belle | SDKs 2011/2012 com C++, Qt, Java ME, Web Runtime | [Symbian^3 e UIQ](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-UIQ%26S3.md) | Mais atual da família para comparar stack híbrida |
| UIQ 2.1/3.0/3.1/3.3 | SDKs de celulares de diferentes fabricantes | [Arquivo UIQ](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-UIQ%26S3.md) | Separar evolução do OS da camada de interface |
| Series 80 e Series 90 | SDKs Java MIDP e C++ (S80 DP 2.0; S90 Concept) | [Arquivo de séries](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Series.md) | Investigar resoluções, UI e plataformas alternativas |
| SDKs por aparelho | N7210, 3510i, 5100, 3300, N6230, N7600, N7710 e N97 | [Arquivo de dispositivos](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Phone.md) | **Perfis e APIs por dispositivo**, sem torná-los alvo do motor |
| Extensões | Plug-in OpenGL ES 1.1 para S60 3rd, sensores, energia, Eseries FP2, Open C | [Plug-ins](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Plugins.md) | Entender aceleração, limites de energia, API e instrumentação |
| Ferramentas criativas | Nokia Audio Suite, Multimedia Converter, Content Authoring e Testing Suite | [Outros SDKs/ferramentas](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Various.md) | Explorar pipeline de áudio, conversão e assets históricos |
| SDKs Qt / Python para S60 | Qt SDK, PyS60 1.4.5–2.0.0 | [Arquivo de linguagens](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Langs.md) | Comparar abstração, tamanho de runtime e overhead |
| Bibliotecas técnicas | S60 3rd Ed FP2 C++ Developer Library, documentação Symbian^3/Belle | [Arquivo de docs](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Docs.md) | Consultar contratos e APIs antigas |
| Códigos abertos do OS | Repositórios preservados do Symbian Foundation, inclusive kernel | [SymbianSource](https://github.com/SymbianSource) · [arquivo e links históricos](https://github.com/mrRosset/Symbian-Archive/blob/master/Links.md) | Estudo arquitetural de OS; versões abertas não equivalem automaticamente ao binário de 2008 |
| EKA2L1 | Emulador open-source de Symbian/N-Gage (C++), kernel e serviços reimplementados | [Repositório](https://github.com/EKA2L1/EKA2L1) · [instalação de dispositivos](https://eka2l1.github.io/quickstart/basic/installdevice/) | Validar comportamento de apps nativos compatíveis, **não assumir suporte integral a Java ME** |

**Advertência:** o arquivo Symbian-Archive reúne espelhos de terceiros (às vezes MEGA), com direitos/licenças próprios e disponibilidade não garantida. Não houve inspeção binária de SDKs, instalação, execução de `epoc.exe`, verificação de checksum ou extração das APIs. Plugins e docs às vezes exigem Windows XP/JRE antigos.

### O Nokia 5320 é **somente uma amostra de referência**

- **Modelo:** Nokia 5320 XpressMusic, identificador de firmware **RM-409**; **sistema:** Symbian OS **9.3**, **S60 3rd Edition Feature Pack 2**.
- **Firmware encontrado em catálogo externo:** `RM-409 v.03.26 5320.rar` (**132.638 KB** listados) e `RM-409 v.04.13 5320.rar` (**134.484 KB** listados).
- **Link de referência:** [catálogo de versões RM-409](https://www.tile-os.com/Firmwares/Nokia/5320/) · [espelho por família](https://firmware.center/firmware/Nokia/5320%20%28RM-409%29/).
- O tamanho acima é do **pacote de firmware comprimido**, **não** do kernel, tamanho de imagem do OS residente nem memória consumida durante o jogo.
- A escolha histórica busca representar uma plataforma relativamente sofisticada do fim da era Java ME/S60. **Não priorizar patches específicos desse aparelho** sobre padrões transversais.

## 3. Outras plataformas móveis: ampliar a comparação além do Java/Symbian

| Ecossistema | Fonte/documentação localizada | O que investigar | Cautela |
| --- | --- | --- | --- |
| **Windows Mobile 6 / Windows CE** | [SDKs Microsoft oficiais: Standard e Professional](https://www.microsoft.com/en-us/download/details.aspx?id=6135) (emuladores, headers, bibliotecas, exemplos) | C/C++, .NET Compact Framework, renderização, input, recursos, consumo de runtime | São instaladores históricos para Visual Studio/Windows; **não instalar sem isolamento** |
| **BlackBerry Java OS** | [Exemplos JDE oficiais liberados sob Apache 2.0](https://github.com/blackberry/JDE-Samples) · [guia histórico de desenvolvimento](https://www.blackberry.com/emailers/developers/javaone/DevZoneWelcomePDF_Final.pdf) | APIs Java de fabricante, ciclo de vida, organização de UI e recursos | **Amostras**, não um runtime/SDK JDE completo confirmado para download |
| **Palm OS Garnet/Cobalt** | [SDKs históricos listados](https://palmdb.net/app/palm-os-sdk) · [documentação técnica](https://palm.wiki/development/docs/601/PalmOSCompanion/PalmOS5ARM_Chapter.html) · [docs preservados](https://github.com/pmastrosimone/palm-dev-docs) | ARMlets, render 2D, recursos, 68K↔ARM, estruturas e transição de arquitetura | Dependências e licenças históricas a inspecionar |
| **Nokia N-Gage (nativo)** | [EKA2L1](https://github.com/EKA2L1/EKA2L1) · [anúncio histórico SDK N-Gage 1.0](https://www.sec.gov/Archives/edgar/data/924613/000110465907024010/a07-7067_16k.htm) | Jogos nativos e capacidades de engine, gráficos e multimídia além de MIDP | Não foi localizado pacote oficial N-Gage SDK íntegro para download neste levantamento |
| **Mophun** (SDK em C para jogos) | [Referência histórica](https://emulation.gametechwiki.com/index.php/Mophun) | Runtime específico para jogos e custos de abstração distintos de Java ME | Histórico secundário; **nenhum SDK validado** |
| **Mascot Capsule 3D** (API japonesa) | [Implementação aberta discutida em J2ME Loader](https://github.com/nikita36078/J2ME-Loader) · [FreeJ2ME-Pro](https://github.com/digitalgust/freej2mePro) | APIs 3D proprietárias, formato de modelos, comportamento em jogos reais | Várias revisões e extensões incompatíveis; não inferir padronização |
| **BREW / Qualcomm** | [Anúncio Qualcomm: BREW 2.0 com SDK](https://www.qualcomm.com/news/releases/2002/06/qualcomm-unveils-new-release-brew-client-software-and-brew-sdk-maximize) · [guia de instalação histórico](https://www.devmedia.com.br/introducao-ao-brew/7803) | Plataforma de execução C/C++ focada em serviços e jogos para celulares; comparar pipeline e API nativa | Existência do SDK **documentada**, porém download executável atual **não validado** |
| **DoJa / i-mode (NTT DoCoMo)** | [Guia técnico oficial DoJa-5.x, PDF](https://www.docomo.ne.jp/english/binary/pdf/service/developer/make/content/iappli/technical_data/doja/jguidefordoja5_x_en_080527.pdf) · [Guia de plataforma J2ME Polish](https://github.com/Enough-Software/j2mepolish/blob/master/enough-polish-website/site/source/docs/platform-doja.html) | Perfil Java CLDC proprietário distinto de MIDP, APIs e ferramentas de jogos japoneses | Documentação localizada; SDK/emulador original **não instalado** |
| **Sony Ericsson Java ME** | [Readme preservado do SDK Java ME 2.5.0.3](https://j2me-docs.narod.ru/sdk/README.html) | Extensões e APIs de fabricante, ferramentas de teste e diferenças para Nokia | Documento técnico localizado, **arquivo de SDK não validado** |
| **Nokia Series 40 / outras Java ME** | [SDKs por aparelho no Symbian-Archive](https://github.com/mrRosset/Symbian-Archive/blob/master/SDKs-Phone.md) | Celulares Java ME sem depender de Symbian; comparar resolução, perfis e custos de runtime | Perfil a confirmar individualmente; **Series 40 não é Symbian** |

A pesquisa em BREW, DoJa e Sony Ericsson foi ampliada com documentação de época; isso comprova a existência histórica de ferramentas, mas não que seus instaladores originais estejam disponíveis ou executem hoje. O DoJa é um perfil Java específico do i-mode, **não** sinônimo de MIDP 2.1.

A documentação Microsoft lista instaladores de 454,7 MB (Professional) e 210,6 MB (Standard); novamente, **tamanho de SDK não é tamanho do OS**. A documentação Palm inclui exemplos de código ARM nativo chamado a partir de aplicativos 68K; é uma ótima comparação de trade-offs, mas os aparelhos não usavam necessariamente Java ME como plataforma principal.

## 4. Priorização conforme o problema de engenharia (não por fabricante)

| Pergunta concreta | Ferramentas candidatas | Evidência que falta produzir |
| --- | --- | --- |
| Como roda um MIDlet real sem celular? | FreeJ2ME / FreeJ2ME-Pro / J2ME Loader + WTK | Inicialização, input, menus, resolução, save, áudio, 3D; screenshots/logs reproduzíveis |
| Como Java ME aloca/gerencia recursos? | phoneME Feature MR2/MR3, SDK Oracle, especificações | Mapear heap, GC, desenho, carga de assets e diferença runtime×jogo |
| Como funcionavam renderizadores 3D compactos? | Jogos do corpus com JSR 184, JSR 239, Mascot + exemplos Java ME | Reconstruir algoritmo concreto, testar imagem e performance |
| Como engines economizavam bytes e RAM? | 100 JARs prioritários + exemplos SDK + código de runtime | Bytecode real, formatos, cena equivalente, memória real e tamanho compactado |
| Era eficiente por API, hardware ou game design? | Amostras Java ME, Palm, WinMobile, Symbian nativo e benchmarks | Separar variáveis e executar uma baseline controlada |
| Vale portar uma técnica para HTML5 atual? | Implementação PocketForge Canvas 2D/WebGL comparada a baseline simples | Frame p50/p95, memória, tempo até jogar, tamanho e qualidade no mesmo dispositivo |

**Sequência proposta**, sem reiniciar auditorias concluídas:
1. Reutilizar [registro de 1.649 hashes](../batches/registry.json), [seleção dos 100](../deep/selection-100.md) e [estado detalhado](../deep/registry.json). **Não repetir os 17 lotes nem fingir reconstrução dos 100.**
2. Montar **ambiente reproduzível de observação** para um pequeno subconjunto de 2D, 3D e áudio em emuladores abertos. Registrar JAR original apenas temporariamente, hash, runtime, versão, perfil, comandos, input e telas.
3. Cruzar com `javap`, parsing de manifestos e APIs JSR; usar SDK como **documentação/comportamento de referência**, não como motor HTML5 final.
4. Reconstruir **técnica geral em código próprio** (por exemplo, decodificação de sprites, cache, batching, framebuffer, IA) e integrá-la em uma demo jogável.
5. Medir contra baseline moderna nos **mesmos dispositivos e cenas**. Registrar negativos e overheads: um truque que poupava RAM num Nokia pode ser mais lento em Canvas/WebGL.
6. Versionar resultados em [registry da fase detalhada](../deep/registry.json) somente após evidência e testes; respeitar [gates](../../08-qa-testes.md) e políticas de licença.

### Modelo mínimo de ficha por ferramenta

```yaml
nome: "..."
categoria: runtime | sdk | emulador | os-firmware | documentacao
fonte_url: "..."
plataforma: "..."
versao: "..."
licenca_confirmada: false
download_localizado: true
bytes_baixados_e_hash_verificados: false
instalacao_testada: false
jogo_original_executado: false
apis_confirmadas: []
limites: "..."
aplicacao_no_pocketforge: "..."
```

## 5. Fontes principais e observações finais

- [Oracle, Java ME Archive Downloads](https://www.oracle.com/java/technologies/java-archive-downloads-javame-downloads.html) — origem oficial para WTK e SDK 3.0; pode exigir aceite/login e não oferece atualizações de segurança.
- [Oracle, referência de APIs 3D/SVG](https://docs.oracle.com/javame/dev-tools/jme-sdk-3.0-win/html-helpset/z40010bc30131.html) — especificações de capacidades, **não** compatibilidade automática de cada celular.
- [phoneME Project, versões históricas](https://phonej2me.github.io/downloads_previous.html) — código e binários CLDC/MIDP.
- [Symbian-Archive](https://github.com/mrRosset/Symbian-Archive) — diretório histórico amplo de ferramentas, não fornecedor oficial atual.
- [SymbianSource](https://github.com/SymbianSource) — componentes abertos preservados do Symbian Foundation.
- [EKA2L1](https://github.com/EKA2L1/EKA2L1), [FreeJ2ME](https://github.com/hex007/freej2me), [J2ME Loader](https://github.com/nikita36078/J2ME-Loader) — referências de emulação, não equivalentes umas às outras.
- [Microsoft Windows Mobile 6 SDKs](https://www.microsoft.com/en-us/download/details.aspx?id=6135), [BlackBerry JDE Samples](https://github.com/blackberry/JDE-Samples), [Palm OS SDK](https://palmdb.net/app/palm-os-sdk) — comparação de ecossistemas independentes.

**Aquisição efetivamente realizada:** [relatório de 12 arquivos com hashes e três pendências](aquisicao-fontes-mobile-2026-10-16.md). Os arquivos de terceiros não foram commitados.

**Este catálogo é um inventário de referências e hipóteses de pesquisa.** Não houve download, instalação, descompactação, emulação de jogos ou avaliação de desempenho desses SDKs/firmwares nesta atualização. A pesquisa pode ser expandida para novos sistemas sem alterar a missão da skill.
