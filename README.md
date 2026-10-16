# PocketForge

**Super-skill de engenharia de jogos modernos ultraleves.** Crie jogos HTML5 com liberdade estética, alto acabamento visual e foco em **qualidade percebida por byte, milissegundo e linha de código** — do Game Brief ao build revisado.

> [!IMPORTANT]
> **v0.1 = fundação operacional**, não criação autônoma de qualquer jogo. Existem documentação, scripts, demo, testes estruturais e smoke interativo de navegador. Agentes autônomos de criação e QA visual em navegador ainda constam no roadmap. J2ME é uma referência de engenharia enxuta; PocketForge **não usa Java, não é emulador e não obriga pixel art**.

## Pesquisa reproduzível: 100 jogos por PR

**Status: 1.649/1.649 JARs distintos auditados sinteticamente e versionados**, em 17 PRs mesclados (16 lotes de 100 + um de 49). A fase estática está encerrada; a **próxima fase é engenharia reversa detalhada e evolução do motor**.

- [Contrato de continuidade para qualquer agente/chat](docs/research/CONTINUITY.md)
- [Ledger com hashes completos, sem duplicação](docs/research/batches/registry.json)
- [Relatório final, estatísticas e índice dos 17 PRs](docs/research/STATIC_COMPLETE.md) · [Lote 001](docs/research/batches/001.md) · [Lote 017](docs/research/batches/017.md)
- Motor operacional já integrado ao demo: [compact](demo/engine/compact.js), [estado](demo/engine/state.js) e [áudio](demo/engine/audio.js), com testes e CI.

**Não colocar JARs/JADs originais no repositório.** O processamento sintético terminou: cada PR contém os metadados dos arquivos, sem executar ou descompilar integralmente os jogos. Os próximos PRs, da fase detalhada, deverão estudar algoritmos de verdade e incorporar melhorias funcionais do motor com testes e benchmarks.

## Comece aqui

| Recurso | O que contém |
| --- | --- |
| **[SKILL.md](SKILL.md)** | Entrypoint de agente, invariantes, fluxo, gates, referência sob demanda |
| **[Índice técnico](docs/INDEX.md)** | 20 capítulos organizados por engenharia, arte, QA e operações |
| **[Tutorial](docs/13-tutorial-primeiro-jogo.md)** | Instruções de execução e derivação do demo |
| **[Lumen Shift](demo/)** | Vertical slice de arena/ação Canvas, sem CDN, motor ou dependências de runtime |
| **[Padrões por gênero](docs/10-receitas.md)** | Arena, plataforma, pseudo-3D, RPG isométrico, puzzle e micro-3D |
| **[Harness de agentes](docs/15-harness-agentes.md)** | Arquitetura proposta de papéis, tarefas, gates e evidências |
| **[Roadmap](docs/11-roadmap.md)** | O que está concluído, planejado e pendente de teste |

## A primeira demonstração: Lumen Shift

Um jogo compacto construído com Canvas 2D, CSS e JavaScript puros. Possui menu, controle por teclado e ponteiro, botão de dash, perseguidores, orbes colecionáveis, colisão, vida, score, recorde local, aumento de dificuldade, pausa, reinício, partículas e áudio sintetizado. É **código de vertical slice**, não um benchmark de desempenho validado em múltiplos aparelhos.

### Executar

```bash
git clone https://github.com/AlexandreGSilva07/Pocket-forge.git
cd Pocket-forge
python3 -m http.server 8000 --directory demo
```

Abra **http://localhost:8000** em um navegador. Em desktop use WASD/setas, Space (dash), P (pausa) e M (áudio). Em touch, aponte a direção na arena e toque no botão Impulso. Para servir ao celular na mesma rede, configure o endereço/porta do servidor apropriadamente.

## Toolchain local

Não é necessário npm para executar o jogo ou os scripts Python.

```bash
# Gerar scaffold de um novo projeto a partir da referência
python3 scripts/new_game.py meu-jogo --title "Meu Jogo"

# Gerar SVGs procedurais originais (ícones e cenário abstrato)
python3 scripts/make_assets.py meu-jogo/assets --seed 42

# Auditar tamanho local bruto e gzip aproximado
python3 scripts/audit.py meu-jogo --json

# Testes determinísticos Python e sintaxe JS
python3 -m unittest discover -s tests -v
node --check demo/game.js
```

**Os limites das ferramentas são explícitos:** `new_game.py` copia/customiza um ponto de partida, não inventa novas mecânicas por prompt; `make_assets.py` cria quatro SVGs abstratos, não um sprite studio generalista; `audit.py` não mede FPS, memória ou tráfego HTTP real.

## Organização

```text
Pocket-forge/
├── SKILL.md
├── README.md
├── docs/             # 20 capítulos técnicos e índice
├── agents/           # 8 playbooks especializados + índice
├── examples/         # Game Brief e manifesto de requisitos
├── schemas/          # contrato JSON Schema do projeto
├── scripts/          # new_game, make_assets, audit
├── demo/             # Lumen Shift (HTML, CSS, JS)
├── tests/            # regressões determinísticas + browser smoke Playwright
├── .github/workflows # CI: sintaxe, testes e orçamento de bundle
├── CONTRIBUTING.md
└── LICENSE
```

## Pesquisa baseada em jogos reais

O [relatório da coleção Nokia64](docs/research/02-auditoria-j2me-2309-jars.md) registra a análise estática de **2.309 JARs, sendo 1.649 binariamente distintos**, obtidos de um ZIP de ~154 MiB pelo GitHub Actions. O jogo original não foi executado nem integrado ao repositório.

O [primeiro relatório J2ME](docs/research/01-analise-j2me-lote01.md) documenta **análise estática de dez arquivos JAR**, com padrões de assets e renderização e experimentos para orientar a futura revisão da skill. **Não** foram analisados 1.000 jogos, executados jogos em emulador ou medidos FPS/RAM nesse estudo.

## Índice temático

**Começar:** [Visão](docs/00-visao.md) · [Pipeline](docs/01-pipeline.md) · [Arquitetura](docs/02-arquitetura.md) · [Tutorial](docs/13-tutorial-primeiro-jogo.md)

**Produzir:** [Tecnologia/render](docs/03-tecnologia-renderizacao.md) · [Componentes](docs/04-componentes.md) · [Arte/assets](docs/05-artes-assets.md) · [Áudio](docs/06-audio.md) · [Design system](docs/17-design-system-ui.md) · [Receitas](docs/10-receitas.md)

**Verificar:** [Performance](docs/07-performance.md) · [QA e gates](docs/08-qa-testes.md) · [Benchmarks](docs/16-benchmarks-avaliacao.md) · [Distribuição/licenças](docs/09-distribuicao-licencas.md)

**Evoluir:** [Manifesto](docs/12-manifesto.md) · [Harness](docs/15-harness-agentes.md) · [Contrato de ferramentas](docs/18-protocolo-ferramentas.md) · [Roadmap](docs/11-roadmap.md) · [Limites](docs/19-perguntas-e-limites.md)

## Como instalar como skill

O arquivo `SKILL.md` segue o formato de skills para agentes (frontmatter YAML + instruções). Adicione o diretório ao local de skills do agente escolhido; cada ferramenta/cliente tem seu próprio caminho de instalação. Referências técnicas são carregadas sob demanda.

A presença dos oito playbooks em `agents/` **não** configura um sistema de agentes em execução; são playbooks para um agente coordenador ou pessoas. O harness real está especificado em [15](docs/15-harness-agentes.md).

## Qualidade e evidências

Os workflows GitHub Actions executam testes Python, verificação de sintaxe JavaScript, orçamento estático, validade sintática JSON e um **smoke real via Playwright/Chromium**: iniciar, mover, pausar, retomar, usar dash e acionar touch no perfil mobile, salvando screenshots como artefatos de CI. Isso comprova esses caminhos no ambiente do runner, mas **não** equivale a teste em celular físico, revisão visual por IA/humano, benchmark FPS ou avaliação de diversão. A documentação [G0–G5](docs/08-qa-testes.md) separa build, gameplay, visual, perfil e licença; use o [Evidence Report](docs/08-qa-testes.md#modelo-de-evidence-report) para declarar o que foi testado.

O objetivo é evoluir do vertical slice para ferramentas reutilizáveis e benchmarks de múltiplos gêneros, preservando fidelidade de relatório: **feito ≠ testado ≠ medido**.

## Licença e contribuições

Código e documentação sob [MIT](LICENSE); o uso de assets externos exige rastreio de proveniência e licença. Veja [CONTRIBUTING.md](CONTRIBUTING.md).
