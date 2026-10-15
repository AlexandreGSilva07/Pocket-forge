# PocketForge

**Super-skill de engenharia de jogos modernos ultraleves, com liberdade estética e validação real.**  
Construída para agentes que precisam entregar jogos jogáveis — não apenas protótipos ou mockups.

## O que existe nesta versão (v0.1)

- `SKILL.md` compatível com o formato aberto Agent Skills, com referências sob demanda.
- Guias especializados de arquitetura, direção de arte, design, áudio, componentes, testes e otimização.
- Ferramentas Python sem dependências para criar um novo projeto, produzir assets vetoriais e auditar o peso do pacote.
- **Lumen Shift**: vertical slice jogável em HTML5 Canvas, sem framework nem CDN, com partículas, controles touch/teclado, colisão, vida, pontuação, dash, áudio sintetizado e dificuldade progressiva.
- Testes locais e integração contínua via GitHub Actions.

## Executar o demo

```bash
python3 -m http.server 8000 --directory demo
# abrir http://localhost:8000
```

Ou abra `demo/index.html` (utiliza módulos ES; prefira servidor HTTP).

## Criar um jogo derivado

```bash
python3 scripts/new_game.py meu-jogo --title "Meu Jogo"
python3 -m http.server 8000 --directory meu-jogo
python3 scripts/audit.py meu-jogo
python3 scripts/make_assets.py meu-jogo/assets --seed 42
```

O scaffold é uma **base de referência**, não um gerador de jogos arbitrários: o agente deve redesenhar a mecânica, a arte e os componentes de acordo com o pedido, depois testar a entrega.

## Usar como skill

Copie o repositório para o diretório de skills do seu agente e aponte o agente ao arquivo `SKILL.md`. O formato usa frontmatter `name: pocketforge` e documentação carregada sob demanda; a localização de instalação varia conforme o agente.

Leia `SKILL.md` e `references/pipeline.md`. Os arquivos `agents/*.md` representam **papéis operacionais**, não processos de IA automaticamente executados.

## Critérios de qualidade

1. O jogo precisa executar, responder aos controles e ter condições de vitória/derrota.
2. O desenho visual é livre, desde que consistente e legível.
3. O projeto deve manter um orçamento definido de tamanho, memória, FPS e inicialização.
4. O agente deve apresentar evidências observáveis de testes e declarar lacunas.
5. É proibido tratar mockups, código compilável ou screenshots como comprovação de jogabilidade.

## Status

**v0.1: fundação funcional**, não um conversor automático de 1.000 jogos nem um sistema autônomo de produção. O próximo passo é ampliar gêneros, geradores de assets e harness de QA visual.

MIT License (ver `LICENSE`).
