# 19 — Perguntas difíceis, limites e critérios de honestidade

## PocketForge consegue criar qualquer jogo?
**Não na versão 0.1.** Há uma demonstração e ferramentas fundacionais. A arquitetura é projetada para expansão; a autonomia de gerar jogos arbitrários ainda deve ser implementada e avaliada.

## É igual ao REA?
Não. O REA organiza ferramentas para investigação/engenharia reversa; PocketForge organiza **produção de jogos originais**. As semelhanças desejadas são documentação, especialização, contratos, instrumentação e validação.

## Precisa programar em Java?
Não. A inspiração vem de design compacto de jogos antigos. A implementação de referência usa HTML/CSS/JavaScript Canvas, sem JVM ou emulador J2ME.

## A estética precisa ser pixelada?
Não. O alvo é jogo **moderno ultraleve**; a arte pode ser vetorial, ilustrada, isométrica, low-poly, 2.5D ou híbrida.

## Canvas é sempre a melhor escolha?
Não. WebGL/WebGPU ou motores podem ser superiores para muitos sprites, shaders ou 3D real. Decidir por protótipo e medição.

## 1 MB é garantia?
Não. É uma meta inicial para microgames, não limite universal, benchmark nem qualidade garantida. Arte e mecânica definem o orçamento viável.

## O script de assets faz arte completa?
Não. Gera SVGs abstratos com seed; personagens animados, coerência visual e atlas complexos exigem etapas adicionais.

## Posso usar 1.000 jogos J2ME como corpus?
Sim, para estudar padrões, se houver acesso legítimo e uso conforme licenças. Evitar distribuição não autorizada de assets/código de terceiros. O corpus não é necessário para executar o PocketForge.

## Como sei se está realmente funcionando?
Verifique os gates G0–G5 em `08-qa-testes.md`. Sintaxe Python/JS no CI não equivale a teste interativo em navegador. Exigir relatório de evidências e testes manuais/futuros testes automatizados.

## E se o agente inventar resultados?
O relatório deve separar “concluído”, “testado”, “medido” e “não verificado”. A palavra **otimizado** requer baseline comparável; **jogável** requer entrada e loop exercitados.

## Uma única skill enorme ou subskills?
Começar com skill raiz enxuta + referências especializadas. Subskills independentes podem surgir quando possuírem ferramentas e testes próprios, não apenas nomes.
