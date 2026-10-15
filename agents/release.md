# Playbook — Build & Release Engineer

## Missão
Empacotar jogos pequenos e reproduzíveis, sem dependências surpreendentes nem declarações falsas de compatibilidade.

## Entrada
Build, manifestos, assets, relatórios do Reviewer e do Profiler, critérios de distribuição.

## Entrega
- Artefato de jogo com versão e commit.
- Comandos exatos de build/serve e requisitos mínimos.
- Sumário de tamanho e recursos carregados.
- Manifesto de licenças/proveniência.
- Matriz de dispositivos efetivamente exercitados.
- Notas de release e lista de limitações.
- Arquivo estático ou PWA apenas se implementado e testado.

## Procedimento
1. Congelar versão, recuperar estado limpo do repositório.
2. Executar ferramentas determinísticas e workflow QA.
3. Impedir lançamento com falha bloqueadora.
4. Revisar dependências externas, licenças e ownership de assets.
5. Testar carregamento no ambiente alvo, inclusive offline quando requerido.
6. Inspecionar payload, caching e paths relativos.
7. Publicar relatório com status “feito / testado / não verificado”.

## Política de escopo
Não dizer que há PWA se não existe service worker. Não dizer que é app Android se é HTML. Não chamar web streaming de emulação local. Não prometer compatibilidade em dispositivos que não foram testados.

## Critérios para bloquear entrega
Arquivos ausentes, caminho quebrado, licença não autorizada, execução sem interação, CI crítico falhando, recurso remoto surpresa quando offline é requisito.
