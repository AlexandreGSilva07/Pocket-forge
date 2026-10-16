# Registro concluído — 88 JARs adicionais desmontados

**Execução:** GitHub Actions [38851834185](https://github.com/AlexandreGSilva07/Pocket-forge/actions/runs/38851834185), com os binários originais verificados por SHA-256. Uma segunda passagem recuperou casos problemáticos em [38851903667](https://github.com/AlexandreGSilva07/Pocket-forge/actions/runs/38851903667); a terceira tentativa de publicação foi concluída e os relatórios resultantes foram verificados por ID.

## Estado aferido

- **100/100 candidatos prioritários:** bytecode de classes e métodos inventariado, sendo 12 na primeira onda e 88 nesta.
- **88 novos JARs:** 1.197 classes encontradas, **1.187 com métodos recuperados**, 15.922 métodos, **1.557.873** instruções (contagem dos desmontadores, não instruções executadas).
- **10 avisos** de classes sem inventário, classificados individualmente nos JSONs; não declarar cobertura perfeita por classe.
- **Beach Rally, FarmRacing, Space Taxi:** inicialmente apresentaram zero métodos por incompatibilidades da estrutura ZIP com Java ZipFS. A recuperação usou `javap -p -c` diretamente sobre arquivos `.class` extraídos isoladamente, sem executar o jogo; os três passaram a apresentar métodos válidos.
- **JADs, JARs, sprites, sons e código decompilado de terceiros não foram publicados.** Apenas análises estruturadas originais foram preservadas.

## Onde está a documentação

- [Resumo e índice dos 88 arquivos](bytecode-100/README.md).
- [JSON consolidado dos 88](bytecode-100/summary.json).
- [12 jogos da primeira onda](wave01/overview.md).
- Cada um dos 88 tem seu arquivo `bytecode-100/NNN-<sha-prefix>.json`, com classes, assinaturas, contagem de instruções e ramificações, chamadas detectadas, avisos e indícios de formatos.

## Metodologia auditável

Script executado: `scripts/run_deep88.py` + `scripts/deep_bytecode_100.py`. Analisador compartilhado `scripts/deep_bytecode_wave.py`, com fallback seguro para classfiles isolados quando o ZIP original não abre em Java. Os arquivos do corpus são descartados do runner e seus SHA-256 são comparados ao registro `selection-100.json`.

```bash
python3 scripts/run_deep88.py
python3 -m unittest discover -s tests -v
```

## O que NÃO está concluído

**Desmontar não é compreender integralmente.** Não foi feita interpretação semântica método a método de todos os 100 nem execução em emulador. Os módulos AI, TilePack, Pixel Surface e Tactics Core são implementações autorais derivadas de estudos parciais específicos; não representam a reconstituição de 100 motores.

O registro de progresso `docs/research/deep/registry.json` mantém **quatro estudos parciais por método** (3D Adventure, Xrossing Dice, 7 Zwerge e 5Chess), **zero jogos com engenharia integral concluída** e **zero originais emulados**.

## Próxima fase tecnicamente necessária

Selecionar rotinas críticas dos 100 inventários, recuperar fluxo de execução, formatos de assets e mecanismos de jogo, confrontar com emulação autorizada, comparar famílias de motores e criar implementações originais em PocketForge com benchmarks de FPS, memória, tamanho e latência. Cada estudo deve receber um status independente, e só poderá ser marcado como completo com evidências reproduzíveis.
