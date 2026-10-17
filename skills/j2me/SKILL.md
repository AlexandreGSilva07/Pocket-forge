---
name: pocketforge-j2me
description: "Use para criar jogos J2ME ou analisar, executar e converter jogos Java ME para HTML5 com ferramentas determinísticas, testes e diagnósticos."
license: MIT
metadata:
  language: "pt-BR"
  tracks: "run,port,create"
  maturity: "experimental"
---

# PocketForge J2ME — skill operacional independente de modelo/fabricante

## Objetivo

Esta skill orienta agentes de IA a construir **software e artefatos executáveis**, usando JVM Java ME e APIs CLDC/MIDP como referências. O Nokia 5320 é apenas uma amostra histórica, nunca alvo fixo. Os modos possuem contratos distintos:

| Modo | Entrada | Saída | Implementação atual |
|---|---|---|---|
| **RUN** | JAR original | Página com VM Java ME em JS; executa bytecode original | MVP com base JS2ME MIT; APIs parciais |
| **PORT** | JAR + traços | Build JS/WASM sem bytecode/JVM no runtime | **Ainda não implementado como compilador genérico** |
| **CREATE** | Brief de jogo | Fontes Java ME e manifesto para WTK/SDK CLDC-MIDP | Scaffold de fontes pronto; compilação real depende SDK e pré-verificador |

## Fluxo RUN — tarefas determinísticas

1. Ler SKILL.md da raiz e o catálogo em docs/research/plataformas-mobile-sdks-runtimes.md.
2. Executar: python3 scripts/build_j2me_runtime.py. Ele baixa uma **revisão fixada** do JS2ME MIT *durante o build*; para origem já clonada use --source /caminho/js2me.
3. **Caminho padrão SEM servidor:** executar python3 scripts/build_j2me_single_html.py; abrir dist/PocketForge-J2ME-Offline.html com duplo clique (Chrome testado via file://) e selecionar JAR. Para gerar HTML com jogo já embutido, executar python3 scripts/build_j2me_single_html.py --jar jogo.jar --output MeuJogo.html. Não publicar JAR comercial embutido. A pasta dist/j2me-web em modo HTTP é apenas alternativa de depuração.
4. Executar análise estática: python3 scripts/j2me_compat_report.py arquivo.jar --api-root dist/j2me-web/js/me --out report.json.
5. Quando disponível, executar testes de navegador com tests/browser_j2me_compat_probe.py e salvar diagnósticos. O probe é um oráculo de comportamento parcial e não garante gameplay.
6. Corrigir falhas do runtime na camada apropriada, adicionar regressão e testar **um segundo jogo**, evitando hacks exclusivos de títulos específicos.

É proibido declarar êxito apenas porque o manifesto foi lido. Escala de evidências: ZIP válido → MIDlet encontrado → bytecode executado → primeiro frame real → input funcional → loop jogável → jogo completo comparado com original.

Veja [protocolo testado de arquivo único](../../docs/j2me/html-unico-sem-servidor.md) para evidências, testes de JAR original, formatos do bundler e limitações.

## API, compatibilidade e segurança

- CLDC 1.1, MIDP 2.0, Nokia UI, MMAPI e RMS são famílias **independentes de serviços** que precisam ser implementados conforme cada jogo.
- Um arquivo de classe da API presente na pasta JS2ME não prova que seus métodos estejam completos.
- JS2ME é um projeto antigo, com JIT e suporte incompleto, especialmente M3G/JSR 184. Guardar stacks e versões exatas.
- Nosso builder aplica correções de VM determinísticas com testes, mantendo avisos MIT/BSD e origem rastreável.
- **Offline:** o bundle não usa CDN, Java instalado ou backend de execução. **HTML único via file:// foi implementado e testado no Chrome Linux.** Outros navegadores podem variar; o motor é carregado integralmente na página sem arquivos ou bibliotecas externos.
- Para JARs não confiáveis, usar perfil isolado de navegador, sem dados pessoais ou sessão autenticada. VM em JS não é sandbox garantida.
- Não commitar ROMs, JARs comerciais ou código original decompilado. Guardar testes privados em external-corpus/ e registrar hashes.

## Fluxo PORT — não inventar progresso

RUN executa bytecode pela VM escrita em JavaScript; **não é** um porte AOT independente da JVM. Para PORT verdadeiro, construir tradutor classfile→IR→JS/WASM, compatibilizar CLDC/MIDP, preservar semântica da JVM e testar equivalência por traços. Os scripts zip-jar.js/gameloft-banks.js demonstram portagem determinística de estruturas de dados, não do motor de corrida inteiro.

Só marcar PORT-TESTED quando o build resultante não carregar o JAR nem VM e reproduzir ações/regras do jogo em HTML5. TeaVM é referência AOT Apache 2.0, mas não converte MIDP/CLDC automaticamente.

## Fluxo CREATE — produção Java ME

Executar: python3 scripts/new_j2me_game.py PocketCar --title "Pocket Car".

O scaffold cria GameCanvas/MIDlet e MANIFEST.MF na pasta gerada. Compilar e pré-verificar usando Sun Wireless Toolkit 2.5.2 ou toolchain Java ME equivalente antes de chamar o JAR de compatível com celular. Testar tanto em emulador Java ME quanto no runtime web quando possível. Não incluir bibliotecas de SDK indevidamente no arquivo do jogo.

## Critérios de aceitação obrigatórios

- Testes de parser e APIs; captura de chamadas e exceções reais, com identificação de classe/método quando possível.
- CI: .github/workflows/j2me-offline-runtime.yml; teste real de JAR em Chromium; teste de instrução JVM wide; smoke do projeto principal.
- Cada avanço deve produzir **código funcional**, testes e diagnóstico, não apenas análise.
- Asphalt Nitro é teste de estresse: docs/research/deep/asphalt-nitro-1-1-7.md. Não afirmar que a corrida inteira funciona sem validar corrida, botões, render, áudio e progressão.
- Resolver bugs genéricos antes de aplicar alterações específicas de jogo.
