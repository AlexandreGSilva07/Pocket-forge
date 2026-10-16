---
name: pocketforge
description: "Engenharia completa de jogos modernos ultraleves para Web, do conceito ao build validado: arte, mecânicas, áudio, performance, QA e entrega. Use quando o usuário pedir para criar, prototipar, ampliar, revisar, portar ou otimizar jogos HTML5."
license: MIT
metadata:
  version: "0.1.0"
  language: "pt-BR"
  platforms: "web,desktop,mobile"
---

# PocketForge — skill de engenharia de jogos ultraleves

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

Os 100 alvos foram selecionados, mas **apenas 12 JARs passaram por desmontagem do bytecode** (metadados por classe e método em `docs/research/deep/wave01/`) e **3 têm revisão técnica parcial de métodos**, sem execução dos originais: 3D Adventure, Xrossing Dice e 7 Zwerge. Nenhum dos 100 foi declarado totalmente reconstruído. O estado canônico está em [deep/registry.json](docs/research/deep/registry.json).

Código original do motor, documentado e testado: [AI Core](demo/engine/ai.js) (alfa-beta, mutate/undo e limites), [TilePack](demo/engine/tilepack.js) (formatos de mapas e PFL v1) e [Pixel Surface](demo/engine/pixels.js) (framebuffer RGBA4444). Exemplos [AI Lab](demo/ai-lab.html) e [Pixel Lab](demo/pixel-lab.html). Metas de FPS e RAM ainda exigem benchmarks; 12 desmontagens automáticas não são 12 estudos semânticos completos.
