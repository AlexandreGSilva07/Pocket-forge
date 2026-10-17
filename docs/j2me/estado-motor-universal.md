# PocketForge J2ME — estado verificável do motor universal

**Data:** 16/10/2026. **Escopo implementado:** RUN experimental + diagnóstico determinístico + scaffold de jogo J2ME. **Não** existe compilador PORT AOT genérico nem compatibilidade total com qualquer JAR.

## O que roda no navegador

O builder scripts/build_j2me_runtime.py monta, a partir de um commit fixo do [JS2ME](https://github.com/szatkus/js2me) MIT, uma pasta dist/j2me-web/ com HTML, CSS e runtime JS. O pacote final não contém JARs comerciais, não usa CDNs e não exige Java instalado. O download do JS2ME ocorre apenas **na preparação**; o bundle final pode ser hospedado ou servido em localhost **sem rede externa**.

O runtime usa bytecode Java original dentro de um interpretador/JIT escrito em JavaScript; portanto isto é **EXECUÇÃO VIA VM**, não código de jogo convertido integralmente em JavaScript. O código-fonte também inclui originais do Zip.js com licenças BSD preservadas. Nenhum firmware Symbian é necessário para a execução dos JARs que usam APIs suportadas.

### Reprodução

1. Execute: python3 scripts/build_j2me_runtime.py
2. Execute: python3 -m http.server 8000 --directory dist/j2me-web
3. Abra http://localhost:8000 e importe seu JAR legitimamente obtido (até 64 MiB).
4. Observe o status e use **Exportar diagnóstico**.
5. Para relatório estático: python3 scripts/j2me_compat_report.py arquivo.jar --api-root dist/j2me-web/js/me --out relatorio.json

Se a fonte já estiver disponível localmente, o builder aceita --source para evitar qualquer download durante o build. O conteúdo do JAR importado não é enviado a um servidor externo; o interpretador lê o arquivo no navegador. Por segurança, trate JARs desconhecidos como código não confiável, executando-os em perfil/ambiente separado.

## Resultados experimentais

- Um MIDlet de referência de 2.219 bytes do próprio projeto upstream teve manifesto lido, 2 recursos carregados e **17 entradas reais no executor de bytecode**, evidenciadas por teste Chromium. A execução **ainda reportava erros System.out** nesse estado inicial; não se tratava de um jogo completo.
- O arquivo de pesquisa AsphaltNitro.jar tem SHA-256 `a96827c5c6539bcaff2d7d23f8bad0cf1dafd8d421af38f97664a25c49fcd9cf`, 2.136.505 bytes, 21 classes Java, versão de classfile 45 e 3.014 referências simbólicas a campos/métodos.
- Mapeamento estático na fonte JS2ME: **32 classes de API com arquivo JS correspondente; 2 sem arquivo**: javax/microedition/media/control/RateControl e TempoControl. Isso **não prova** que 32 APIs funcionam; outras classes presentes tinham métodos ausentes.
- O JAR original do Asphalt foi executado **temporariamente no GitHub Actions** sem ser commitado, via conjunto de dados público. O JIT zazu atingiu 62.337 entradas de método com Canvas criado antes de um bug da instrução JVM wide; depois da correção, observou-se mais de 100 mil entradas antes de outra falha de compatibilidade.
- Comparação de backends: pumba (interpretador), zazu (JIT) e timon (compilador experimental) produzem resultados distintos; timon ainda falha mais cedo com inicialização do Canvas. Todas essas observações são **probes de inicialização**, não prova de corrida/render fiel.
- Corrigimos deterministicamente o opcode JVM wide: endereçamento local u16 para loads/stores e incremento iinc com limite int32. Adicionamos regressão Node.
- Instrumentação de invocações revelou falhas concretas de Java ME: StringBuffer.append(char[],int,int) e Player.getMediaTime()J. O builder agora inclui implementações genéricas e testes para ambos. A resposta do jogo a esses patches é reavaliada por CI.
- **Situação da corrida original:** nenhum teste provou controle, colisões, progresso ou conclusão de corrida; não anunciar Asphalt como portado ou plenamente emulado.

As referências de execução e logs ficam no [PR #27](https://github.com/AlexandreGSilva07/Pocket-forge/pull/27), no [workflow de runtime](../../.github/workflows/j2me-offline-runtime.yml) e nos seus artefatos de curta duração.

## O que a engenharia determinística poupa

O analisador de classfiles lê magic/versão/constant pool, referências externas e grupos de APIs, sem IA. O runtime já executa muitas instruções bytecode e invoca APIs existentes, sem a IA precisar entender semanticamente métodos proprietários ofuscados. Os defeitos restantes viram exceções precisas, correções de VM/APIs e testes reutilizáveis.

A meta é minimizar exceções: usar um pequeno corpus para identificar e implementar lacunas genéricas por *assinatura*; só acionar análises manuais em formatos proprietários, desvios de render e performance.

## O que falta para universalizar e para o modo PORT

- **RUN:** suporte abrangente CLDC/MIDP, MMAPI, RecordStore, canvas, tempos/threads, JSR184 M3G, Mascot, Nokia UI, diferentes resoluções, controle touch/teclas. Testar dezenas de jogos independentes.
- **PORT:** compilador de bytecode para IR e JS/WASM, mantendo semântica da JVM e substituindo chamadas de API por adaptadores sem VM embutida no bundle final. Este item **não está feito** e não deve ser vendido como tradução automática atual.
- **CREATE:** script new_j2me_game.py gera fonte MIDP 2.0 e manifesto; é preciso WTK/SDK genuíno, pré-verificação e teste em aparelhos/emuladores de referência antes de chamar o JAR de compatível.
- **Validação:** capturas e traços do original em emulador + comparação funcional/visual e benchmarks. Canvas criado ou dezenas de milhares de entradas bytecode não equivalem a gameplay completo.

A pesquisa continua **transversal**, não vinculada ao Nokia 5320 ou Symbian. O PocketForge permanece voltado à criação de jogos modernos ultraleves; RUN/PORT/CREATE J2ME são capacidades adicionais formalizadas na [subskill](../../skills/j2me/SKILL.md).
