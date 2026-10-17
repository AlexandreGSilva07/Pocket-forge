# PocketForge — Núcleo de Compilação Java ME → HTML5

**Marco experimental: 16/10/2026, ampliado com referências phoneME.** Um compilador antecipado (AOT), **diferente do emulador JS2ME**. A mesma ferramenta recebe JARs independentes e produz HTML único, que abre por dois cliques no Chrome, sem Java instalado e sem interpretador de bytecode no navegador.

## Arquitetura implementada

`JAR/JAD (manifesto + .class)` → **PocketForge Compiler** (TeaVM 0.16.0, Apache-2.0, versão fixa no POM) → adaptação geral CLDC/MIDP → **`Jogo.html`**.

TeaVM é utilizado como núcleo de compilação industrial existente: decodifica classfiles, compila métodos e gera JavaScript. Não reescrevemos métodos dos jogos com IA, não dependemos de nomes de classes ofuscadas, e não recompilamos o motor para cada título. A adaptação que o script gera é somente o lançador derivado do manifesto `MIDlet-1` ou `Main-Class`; não contém lógica ou heurísticas exclusivas de jogos. Classes no pacote padrão (como `GloftASGM`) também são suportadas.

As implementações Java de APIs Java ME estão em `compiler/teavm-aot/src/main/java/javax/microedition/` e são compartilhadas com **todos** os jogos. A interface gráfica utiliza Canvas 2D, eventos de teclado do navegador e superfícies offscreen, via TeaVM JSBody. Projetos de referência baixados **fora do Git**: JS2ME (MIT), FreeJ2ME, TeaVM (Apache-2.0), SquirrelJME. Nem o código GPL eventualmente encontrado nem ROMs/JARs comerciais foram incorporados.

### Compilar

**Requer no computador de desenvolvimento:** Python 3, JDK 21 (ou toolchain equivalente) e Maven 3.9+. A primeira compilação baixa dependências do TeaVM pela rede. O arquivo **HTML resultante** não requer nenhuma dessas ferramentas, servidor, CDN ou conexão externa.

```bash
python3 scripts/compile_j2me_aot.py caminho/Jogo.jar --out dist/aot/Jogo.html
# Abrir dist/aot/Jogo.html com dois cliques.
```

O programa não executa o JAR durante a compilação. O executável de entrada é referenciado como dependência pelo Maven em uma pasta de trabalho temporária; somente JavaScript gerado e adaptadores efetivamente utilizados são integrados ao HTML. O JAR original não está no HTML. Os limites de tamanho impedem expansão indiscriminada de arquivos ZIP/JAR.

**Se uma API faltar**, o compilador encerra com erro e produz `Jogo.compile.json`, contendo as classes/métodos ausentes. Isso é um diagnóstico de compatibilidade, não pedido para escrever adaptação específica para aquele jogo.

## Evidências reais — Google Chrome do computador do usuário

| Programa JAR | Classes originais | Resultado do compilador / browser |
| --- | ---: | --- |
| `Calculator.jar`, fonte autoral | 1 | HTML 47 KB; calcula arrays/condições/loops, imprime `CALCULATOR=57`. |
| `PocketDemo.jar`, fonte autoral MIDP | 2 | HTML 59 KB; cria Canvas de 240×320 com desenho e texto colorido. |
| `Interactive.jar`, fonte autoral MIDP | 2 | HTML 59 KB; pressionar seta chama `keyPressed` **Java compilado** e altera pixels. |
| `asteroids.jar`, jogo independente de 2002 | 11 | HTML ~246 KB; **tela original Asteroid Zone renderizada e animada no Chrome**, sem JVM/JAR no HTML; não há demonstração de gameplay completo. |
| `AsphaltNitro.jar`, jogo Gameloft | 21 | **Ainda não compila.** O diagnóstico enumerou 19 símbolos de API ausentes (MMAPI, `Graphics.drawRGB`, `drawRegion`, clipping e outras). Não declarar suporte até corrigir APIs e executar uma corrida. |

O teste [`tests/browser_j2me_aot_compiler.py`](../../tests/browser_j2me_aot_compiler.py) **constrói três JARs diferentes a partir de fontes próprias**, compila os três sem modificar o compilador e abre os HTMLs via `file://` no Chrome/Chromium. Exige saída matemática exata, Canvas 240×320, conteúdo gráfico, resposta real ao teclado, zero erros JavaScript e zero requisições externas. A compilação do Asteroids foi testada manualmente com código real na máquina; não distribui seus bytes no Git.

## Distinção obrigatória RUN × PORT

- **RUN**: o JS2ME abre um JAR original com uma VM escrita em JavaScript. Continua útil como oráculo de comparação e para compatibilidade incremental.
- **PORT/COMPILE (este trabalho)**: TeaVM traduz métodos Java para JavaScript **na construção**. No navegador, não existe JAR ou VM interpretando bytecode. É o caminho prioritário para exportar um arquivo autônomo, com compilação determinística.
- **CREATE**: gerador de código-fonte Java ME; as mesmas APIs e testes servem para os jogos criados.

## Limitações e critérios de conclusão

O processo é **genérico**; a **cobertura da plataforma ainda é parcial**. Nenhum compilador pode compilar corretamente todas as chamadas desconhecidas sem implementar suas especificações. Nesta primeira versão ainda faltam: recursos de imagem/áudio embutidos, MMAPI, M3G/JSR 184, Mascot Capsule, Nokia APIs opcionais, conectores/file IO, maior fidelidade de clipping/texto, persistência real do RMS, testes de multithreading e menus. Alguns adaptadores são apenas aproximações ou simplificações explícitas; não representam compatibilidade certificada com MIDP.

Não chamar compilação bem-sucedida de jogo completo. A régua é: classfiles reconhecidos → compilação concluída → primeiras funções em HTML → imagem real → input → jogo jogável → comparação com original → testes de regressão em títulos independentes.

Tentou-se minificar o JS do TeaVM: o HTML de Asteroids caiu para ~70 KB, **mas houve uma regressão gráfica**; portanto foi mantida a configuração NÃO minificada, que passou nos testes. Otimização só entra após equivalência comprovada. O PocketForge não deve receber hacks específicos de títulos para mascarar defeitos de plataforma.

## Fontes e licenças

- [TeaVM, documentação oficial de compilação com Maven](https://teavm.org/docs/tooling/maven.html) — compilador AOT Apache-2.0, usado na versão 0.16.0.
- [TeaVM, comunicação Java/JavaScript](https://teavm.org/docs/runtime/jso.html) — interfaces nativas e `@JSBody`.
- [JS2ME](https://github.com/szatkus/js2me) — motor RUN antigo, MIT; **não** é o motor de compilação AOT.
- [FreeJ2ME](https://github.com/hex007/freej2me) e [SquirrelJME](https://github.com/SquirrelJME/SquirrelJME) — referências de comportamento e implementação, sem copiar código nem assets.

**Resultado:** existe agora um compilador real, testado, extensível e independente de nomes de jogos. A meta de compatibilidade com *qualquer* JAR, inclusive Asphalt Nitro completo, **ainda não foi alcançada**.

## Referência phoneME e compatibilidade ampliada

Veja [levantamento executável de phoneME/j2me.js](phoneme-compatibilidade-referencia.md): o compilador recebeu suporte geral a clipping, translação, ARGB, regiões gráficas e leitura de pixels. Inclui recursos não Java via TeaVM ResourceSupplier e pré-decodifica imagens comuns no HTML. Os testes de regressão agora são **seis JARs independentes**. No Asphalt Nitro, símbolos faltantes caíram de **19 para 6** (MMAPI e Connector), mas o jogo **ainda não compila nem está jogável**. As fontes phoneME/j2me.js GPLv2 foram mantidas fora do repositório.
