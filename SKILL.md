---
name: pocketforge
description: "Engenharia de jogos ultraleves HTML5 e Java ME: criação, engenharia reversa de JAR/JAD, execução offline em navegador, adaptação e validação de gameplay. Use para criar, prototipar, analisar, portar ou testar jogos."
license: MIT
metadata:
  version: "0.1.0"
  language: "pt-BR"
  platforms: "web,desktop,mobile"
---

# PocketForge — skill de engenharia de jogos ultraleves

## Novos modos Java ME — decisão obrigatória

Se a tarefa envolve JAR/JAD, CLDC, MIDP, engenharia reversa Java ME ou criação de jogos J2ME, leia imediatamente **[skills/j2me/SKILL.md](skills/j2me/SKILL.md)**. Operações separadas: **RUN** (executar bytecode pela VM escrita em JS, experimental); **PORT** (exportar código JS/WASM sem VM, compilador genérico ainda não pronto); **CREATE** (gerar fontes J2ME, build com SDK e pré-verificador). Não confundir a execução via VM JS com a conversão AOT nem declarar que qualquer JAR é suportado.


## Persistência do conhecimento entre chats (obrigatório)

Antes de alterar o motor, ler [CONTINUITY.md](docs/research/CONTINUITY.md), o [relatório final da auditoria sintética](docs/research/STATIC_COMPLETE.md) e o [ledger dos 1.649 JARs](docs/research/batches/registry.json). **A etapa sintética está encerrada: todos os 17 PRs foram mesclados na main. Não reexecutar os lotes.** A próxima etapa é engenharia reversa detalhada de classes, métodos e algoritmos com evidências por jogo, seguida de construção e avaliação de componentes originais e testados do PocketForge. As análises sintéticas anteriores não são reconstruções completas e não provam melhoria de FPS/RAM.

O motor funcional utiliza três módulos em `demo/engine/`: `compact.js` (atlas/RLE/tilemap), `state.js` (persistência versionada) e `audio.js` (síntese WebAudio limitada), carregados no Lumen Shift. Ler testes correspondentes antes de evoluir.


Você é o engenheiro principal de um estúdio de jogos. Seu produto final é um **jogo executável**, não uma imagem, apresentação ou página de marketing. Use arte, arquitetura e tecnologia adequadas ao projeto; o objetivo é alto valor visual por byte e por milissegundo, **não** estética obrigatoriamente retrô.

## Invariantes
1. **Jogo primeiro**: entregar um loop jogável com entrada → atualização → renderização → feedback → resultado.
2. **Não confundir artefatos**: mockup ≠ protótipo; build ≠ jogo testado; testes sintáticos ≠ testes de jogabilidade.
3. **Escopo progressivo**: vertical slice funcional antes de expandir conteúdo.
4. **Orçamentos explícitos**: estabelecer metas de peso, FPS, memória, tempo de carregamento e dispositivos-alvo antes de escolher stack.
5. **Sem dependências arbitrárias**: avaliar custo total da biblioteca, runtime, licença, manutenção e compatibilidade offline.
6. **Direção de arte consistente**: paleta, iluminação, formas, tipografia, animações e feedback devem parecer parte do mesmo jogo.
7. **QA independente**: reproduzir falhas, testar controles, estados e regressões; separar observação de suposição.
8. **Integridade**: jamais alegar que screenshots provam jogabilidade ou que uma ferramenta foi executada quando não foi.
9. **Direitos autorais**: usar ativos originais, licenciados ou fornecidos legitimamente; não copiar automaticamente recursos de jogos de terceiros.
10. **Acessibilidade**: oferecer input alternativo, redução de movimento e interface legível sempre que cabível.

## Ordem de execução
1. Ler [visão e critérios](docs/00-visao.md), [pipeline](docs/01-pipeline.md) e [arquitetura](docs/02-arquitetura.md).
2. Produzir o **Game Brief**: gênero, fantasia central, plataforma, orientação, controles, público, duração de sessão, metas de performance, arte, áudio, riscos, critérios de aceite.
3. Criar o **vertical slice** sem telas falsas: menu → gameplay → feedback → game over/restart; testar antes de expandir.
4. Escolher mecanismos de renderização e tecnologia conforme [decisão técnica](docs/03-tecnologia-renderizacao.md), documentando trade-offs.
5. Construir os sistemas reutilizáveis com contratos em [componentes](docs/04-componentes.md).
6. Produzir a arte segundo [assets](docs/05-artes-assets.md); o áudio segundo [áudio](docs/06-audio.md).
7. Executar [testes e gates](docs/08-qa-testes.md), seguir [otimização](docs/07-performance.md).
8. Auditar licenças e conteúdo com [distribuição](docs/09-distribuicao-licencas.md).
9. Entregar build e **Evidence Report**: o que existe, o que foi verificado, comandos, métricas, falhas conhecidas e próximos passos.

## Carregamento sob demanda

| Necessidade | Documento |
| --- | --- |
| Pipeline e checkpoints | [01](docs/01-pipeline.md) |
| Estrutura e arquitetura | [02](docs/02-arquitetura.md) |
| Stack e renderização | [03](docs/03-tecnologia-renderizacao.md) |
| Componentes e mecânicas | [04](docs/04-componentes.md) |
| Sprites, vetores, 2D/2.5D e UI | [05](docs/05-artes-assets.md) |
| Música e SFX | [06](docs/06-audio.md) |
| Otimização e budgets | [07](docs/07-performance.md) |
| Testes de gameplay e QA visual | [08](docs/08-qa-testes.md) |
| Distribuição, segurança e licença | [09](docs/09-distribuicao-licencas.md) |
| Receitas e exemplos | [10](docs/10-receitas.md) |
| Tarefas e marcos futuros | [11](docs/11-roadmap.md) |
| Contratos do manifesto | [12](docs/12-manifesto.md) |

## Ferramentas incluídas na v0.1
- `python3 scripts/new_game.py slug --title "Título"`: deriva um projeto HTML5 standalone a partir do vertical slice.
- `python3 scripts/make_assets.py pasta/assets --seed 42`: cria um pequeno conjunto **original** de SVGs procedurais.
- `python3 scripts/audit.py caminho`: auditora de peso estático; não mede FPS/RAM reais.
- `python3 -m unittest discover -s tests -v`: regressões unitárias Python.
- `node --check demo/game.js`: valida apenas sintaxe JS, não gameplay.
- `python3 tests/browser_smoke.py`: smoke Chromium/Playwright após instalar dependências de desenvolvimento; prova limitada de interações desktop/touch.
- `demo/`: vertical slice de ação arcade com Canvas 2D e áudio procedural.

## Capacidade atual vs. visão
**Implementado:** documentação modular, scaffold, assets vetoriais simples, auditor de tamanho, demonstração jogável, testes automatizados estruturais.  
**Planejado, não implementado:** geração generalista de jogos por prompt, agentes em execução paralela, inspeção visual por IA, port automático, benchmark FPS em vários dispositivos, pipeline 3D completo. Nunca afirme o contrário.

## Critérios de pronto
Veja [gates](docs/08-qa-testes.md). Se não foi executado e observado, marque como **não verificado**. Se o usuário pedir apenas uma parte do escopo, não fabrique as demais como concluídas.

## Pesquisa detalhada — situação verificada em 16/10/2026

Os **100 alvos prioritários passaram por desmontagem real de bytecode** e possuem inventários de classes/métodos: [primeira onda de 12](docs/research/deep/wave01/overview.md) e [88 seguintes](docs/research/deep/bytecode-100/README.md). Há **5 estudos de métodos parciais** (3D Adventure, Xrossing Dice, 7 Zwerge, 5Chess, 3D Balloon Race), mas **zero jogos integralmente reconstituídos e zero originais executados em emulador**. Estado canônico: [deep/registry.json](docs/research/deep/registry.json).

Módulos autorais implementados e testados a partir de evidências: [AI Core](demo/engine/ai.js), [TilePack](demo/engine/tilepack.js), [Pixel Surface](demo/engine/pixels.js), [Tactics](demo/engine/tactics.js) e [Asset Pack](demo/engine/assets.js). Demos [AI Lab](demo/ai-lab.html), [Pixel Lab](demo/pixel-lab.html), [Tactics Lab](demo/tactics-lab.html) e [Asset Lab](demo/assets-lab.html). Não afirmar ganhos de FPS/RAM nem equivalência aos originais sem testes medidos.
