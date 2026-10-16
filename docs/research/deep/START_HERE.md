# Primeira onda de pesquisa profunda — 12 jogos

Plano sugerido, **não** estudos concluídos. Intercalar gêneros e técnicas evita estudar apenas 3D no começo.

| # | Nome/caminho JAR | SHA-256 completo | Questão principal |
|---:|---|---|---|
| 1 | `828 Java Games/3D-Adventure.jar` | `f2667dd8ee20f37d323d16a705ef9e26ed4e61f704af185e1dbb187cf7cf5761` | Rasterização de software e orçamentos de pixels |
| 2 | `All Java Mobile Phone Games/D/Doom RPG (motorola)/doom_rpg_kr.jar` | `6925de2ce810de09f989fdcc2ead3afeed5ebb287cb55ea0d237936d2f32a370` | Perspectiva, navegação e regras de RPG |
| 3 | `All Java Mobile Phone Games/G/GeopodDC 3D/GeopodDC3D.jar` | `595a04f90efc3ab0ea705116b59ea7cff4fd06281b34f121be8231b1a25fe02c` | Modelos M3G, formatos e pipeline 3D |
| 4 | `All Java Mobile Phone Games/P/Prince Of Persia 3 Portugal (teclas)/princepersia_tt.jar` | `eb16778a12aa0bac8b7fc40787c4757c0910f4d6622c77d00ed2ead147c7ea86` | Fases, regiões e animações |
| 5 | `All Java Mobile Phone Games/S/Super Mario 2/MarioMp2.jar` | `16ede07fe8584bf2453ee78d165a9cfc9896bfb4cc460e8f72b826468d4ed407` | GameCanvas, Sprite e TiledLayer |
| 6 | `All Java Mobile Phone Games/L/Lemmings/Lemmings.jar` | `41f07e9dc3318123334483cd9ecda3e3a7d7f5cb18086883f896368c895d4b28` | Simulação de entidades e estados |
| 7 | `828 Java Games/1XCrossingDice.jar` | `8db1413d8135bfc300525375ae0ff398548707d0d8f824cb610d797130e67c9d` | Minimax, heurística e profundidade |
| 8 | `828 Java Games/AncientEmpires.jar` | `2dda1c490d8783642cc783164af2e57057098fc73b9fb656ac57974f1b2b8cc4` | Estados estratégicos e dados de mundo |
| 9 | `828 Java Games/WorldFighting.jar` | `d5d3da079ac379e9a90a5ce65a9596b39c5fcb66de4cb868f9004e4141f71201` | Packing de 127 imagens e animações |
| 10 | `All Java Mobile Phone Games/C/Com2Us Bowling 2/c2ubowling2.jar` | `f83ec4dc56cc9cb747e485d6bb60c500278986ec6c48b0f2a5b0f6a00ec8eebe` | Sprites e frames em jogo esportivo |
| 11 | `828 Java Games/Colin McRae 04 (s60).jar` | `eb05f180891e1f8d182933911abf905d8467503ef8598edd8dea1da717ab15ec` | Lógica de corrida, física e FPS |
| 12 | `828 Java Games/7Zwerge.jar` | `6df7ffc301a3524aa0935ac23311d9e132ce4c1dbf81129e5485052afc0828f2` | Formatos de níveis e MIDI |

## Requisitos para concluir um estudo

1. Revalidar SHA-256 e encontrar as classes/métodos concretos.
2. Descompilar bytecode e recuperar fluxo de atualização, renderização, recursos e regras, registrando pseudocódigo original e citações internas.
3. Executar o original em emulador J2ME sempre que viável; separar comportamento observado de hipótese.
4. Identificar famílias de engines e variantes para evitar redundância.
5. Implementar componentes originais do PocketForge apenas após evidência, integrar e testar.
6. Medir resultados contra baseline e publicar os métodos para reprodução.
7. Atualizar deep/registry.json somente quando houver trabalho e evidências reais.

## Referências

- [Os 100 jogos e 25 reservas](selection-100.md).
- [JSON com hashes e perguntas individuais](selection-100.json).
- [Ledger dos 1.649 JARs](../batches/registry.json).
