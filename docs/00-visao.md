# 00 — Visão, princípios e definição do produto

## Missão
PocketForge é um conjunto de instruções, ferramentas, contratos e exemplos para agentes que criam **jogos modernos ultraleves**. A identidade estética é livre: formas geométricas, arte pintada, low-poly, vetor, voxel, isométrico, motion design, 2D estilizado ou 2.5D. O objetivo é obter **qualidade percebida elevada** com download pequeno, funcionamento fluido e arquitetura clara.

**Referência histórica:** a engenharia de celulares J2ME mostrou como equipes extraíam muito de plataformas limitadas. Isso é inspiração metodológica, não exigência de linguagem Java, resolução 240×320, pixel art ou aparência antiga.

## O que a skill é
- **Conhecimento executável**: referências especializadas, scripts verificáveis, modelos de decisão, exemplos e padrões.
- **Fluxo de produção**: brief → protótipo → conteúdo → instrumentação → QA → build.
- **Disciplina de evidência**: comparação entre objetivo, implementação e resultado medido.

## O que a skill não é
- Não é um motor de jogos proprietário completo.
- Não garante criar um jogo original de qualquer gênero sem intervenção.
- Não converte magicamente imagens em animações ou projetos em jogos prontos.
- Não mede hardware apenas lendo CSS ou contando linhas de código.
- Não autoriza reutilizar código, imagens, marcas ou músicas de terceiros.

## Hierarquia de prioridades
1. **Jogabilidade compreensível**: aprender rápido, responder rápido, dar feedback claro.
2. **Correção observada**: estados, controles, colisão, progressão, pausas e reinício.
3. **Coesão visual**: arte consistente, hierarquia de interface, leitura em telas pequenas.
4. **Performance**: frames estáveis, carregamento rápido, baixa memória e poucos bytes.
5. **Manutenção**: código modular, assets rastreáveis e testes.
6. **Distribuição**: offline, acessibilidade, licenças e robustez.

Se houver conflito, não otimizar peso destruindo a jogabilidade. Registrar exceções aprovadas.

## Definição de moderno
“Moderno” é **polimento e liberdade visual**, não dependência de WebGL pesado: antialiasing quando adequado, iluminação estilizada, animações coerentes, composição, partículas, camadas de profundidade, gradientes, áudio contextual, UX responsiva e feedback. Nenhum recurso visual deve existir apenas para aumentar complexidade técnica.

## Perfis de projeto
| Perfil | Cenário | Referência de orçamento inicial (ajustar ao dispositivo) |
| --- | --- | --- |
| Micro | puzzle/arcade offline | alvo < 1 MB transferido, 60 FPS de referência |
| Compact | ação, roguelite, corrida pseudo-3D | alvo < 5 MB, 60 FPS de referência |
| Expanded | 2.5D, mundo maior, arte sofisticada | budget negociado; faseamento obrigatório |

São **metas de projeto**, não medições nem garantias. O dispositivo-alvo, a latência de rede e as definições de medição fazem parte do brief.

## Template de Game Brief
Preencher antes de codificar:
- Nome, pitch de uma frase, fantasia central, mecânica principal e público.
- Plataforma, orientação, viewport lógico, controles e metas de acessibilidade.
- Pilares: até três sensações que o jogo deve causar.
- Loop de 15–60 segundos; condição de perder, vencer, evoluir ou reiniciar.
- Referências visuais (sem copiar assets), estilo, paleta e iluminação.
- Meta de download, FPS p50/p95, memória, tempo até jogar e dispositivos.
- Conteúdo mínimo do vertical slice, hipóteses a testar, riscos.
- Critérios de aceite mensuráveis e responsável por validar.

## Antipadrões
- Interface bonita sem controles funcionais.
- 12 efeitos antes de existir colisão ou loop principal.
- Dependência de CDN silenciosa em projeto supostamente offline.
- Regenerar todos os sprites para alterar uma cor.
- Gerar código sem executar e declarar “100% funcional”.
- Usar inúmeras bibliotecas para demonstrar uma única cena simples.
- Pixel art por padrão mesmo quando o usuário pede outra linguagem visual.
