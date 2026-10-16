# PocketForge — 100 jogos prioritários para engenharia reversa completa (+25 reservas)

> Seleção baseada nos 17 inventários, ainda SEM decompilar ou executar os JARs nesta fase. Gênero e técnica são hipóteses a verificar.

## Método e limites

- Foram lidos e confrontados os 17 JSONs (1.649 SHA-256 distintos) com o ledger.
- Preferência por exemplos âncora com metadados já examinados; complementação por pontuação estrutural verificável.
- Cotas temáticas garantem diversidade; normalização de títulos limita variantes aparentemente repetidas.
- O escore mede potencial investigativo, NÃO qualidade ou eficiência confirmada.
- JAD não encontrado significa ausência de descritor com nome/caminho correspondente; não inventar.
- Nenhum JAR, código proprietário ou asset original é incluído.
- JBenchmark3D é uma ferramenta de benchmark, não um jogo: fica apenas como controle técnico fora das 100 vagas.

Selecionados: 100 principais + 25 reservas; 100 âncoras verificadas; 55 principais com JAD associado.

## Frentes e metas de pesquisa

| Área | Vagas | Investigação real planejada |
|---|---:|---|
| 3D e rasterização | 20 | Identificar algoritmos reais de projeção, buffers, M3G e rasterização em software. |
| Mundos, mapas, sprites | 20 | Examinar formatos de mapas, colisão, câmera, atlas e ciclos de animação. |
| IA, regras e estratégia | 17 | Analisar busca, heurísticas, regras, simulação e serialização. |
| Arte, recursos e animação | 16 | Investigar compressão de texturas, spritesheets, efeitos e carregamento. |
| Física, corrida e esportes | 15 | Investigar movimento, colisão, física simplificada e ritmo de atualização. |
| Compactação, áudio e minimalismo | 12 | Investigar recursos binários, som e estruturas ultraleves. |

## 100 candidatos principais

| # | Área | Arquivo JAR exato | ID SHA-256 | Classes | Imagens | Áudio | Referências discriminantes |
|---:|---|---|---|---:|---:|---:|---|
| 1 | 3D e rasterização | `828 Java Games/3D-Adventure.jar` | `f2667dd8ee20f37d` | 2 | 5 | 0 | drawPixels |
| 2 | 3D e rasterização | `Doom RPG (motorola)/doom_rpg_kr.jar` | `6925de2ce810de09` | 23 | 17 | 2 | GameCanvas, drawRGB, drawRegion |
| 3 | 3D e rasterização | `Speedchaser3D(1pant)/Speedchaser3D_6630_6680.jar` | `570137fb12a30c7d` | 11 | 22 | 3 | GameCanvas, J2ME M3G |
| 4 | 3D e rasterização | `GeopodDC 3D/GeopodDC3D.jar` | `595a04f90efc3ab0` | 12 | 88 | 3 | GameCanvas, J2ME M3G, drawRegion |
| 5 | 3D e rasterização | `3D Ferrari Experience/3DFerrariExperience.jar` | `7820f0e4feaa34d9` | 27 | 1 | 0 | J2ME M3G, drawPixels, drawRegion |
| 6 | 3D e rasterização | `3D Sentris/3D Sentry.jar` | `91dc9b076607f65c` | 22 | 26 | 8 | GameCanvas, J2ME M3G, drawRegion |
| 7 | 3D e rasterização | `Free Flight 3D/FreeFlight3D.jar` | `0061ce9a799a5182` | 2 | 47 | 3 | J2ME M3G |
| 8 | 3D e rasterização | `FormulaGP 3D/FormulaGP3D.jar` | `7cd885f2f3b6673a` | 22 | 71 | 3 | GameCanvas, J2ME M3G |
| 9 | 3D e rasterização | `Fast And Fourious 3D(sonido)/fastNfourious3D_6630_6680.jar` | `fdb3878423d958d6` | 17 | 59 | 7 | GameCanvas, J2ME M3G, drawRGB |
| 10 | 3D e rasterização | `3D River Storm/River Storm 3D.jar` | `1c257b8f4750fa4f` | 32 | 31 | 0 | GameCanvas, drawRGB, drawRegion |
| 11 | 3D e rasterização | `WOLF/wolf.jar` | `5fca5ecb35d81029` | 2 | 4 | 0 | drawPixels |
| 12 | 3D e rasterização | `828 Java Games/mdoom.jar` | `7e9255bdb69bfff8` | 5 | 5 | 0 | estrutura e assets |
| 13 | 3D e rasterização | `Alpha Zone 3D/3DAlphaZone.jar` | `aca04f45a763262b` | 11 | 1 | 0 | drawPixels, drawRGB |
| 14 | 3D e rasterização | `Alpha wing 2(relentiza)/AlphaWing2.NP.jar` | `f12cba37444efb1d` | 20 | 15 | 13 | GameCanvas, J2ME M3G, drawRegion |
| 15 | 3D e rasterização | `Submarine3D/Submarine3D.jar` | `54900dfbeae417d9` | 36 | 24 | 5 | J2ME M3G, Sprite, drawRGB |
| 16 | 3D e rasterização | `Bomberman 3D/BOMBERMAN3D.jar` | `68ff95bdb6a98ae9` | 7 | 10 | 40 | J2ME M3G, drawRegion |
| 17 | 3D e rasterização | `828 Java Games/3DBalloonRace.jar` | `12e9d0c928e3887e` | 11 | 1 | 0 | drawPixels |
| 18 | 3D e rasterização | `Minigolf Castles 3D (graf)/Mini Golf Castles 3D From Sumea.jar` | `327b40c1880c5d00` | 31 | 1 | 0 | J2ME M3G, drawPixels |
| 19 | 3D e rasterização | `Playman Winter Games 3D/PlaymanWinterGames3D_K750I.jar` | `7fe2dcf68a2f0a37` | 22 | 12 | 0 | GameCanvas, J2ME M3G, drawPixels |
| 20 | 3D e rasterização | `Racing Fever GT 3D/RacingFeverGT3D.jar` | `4a982ba640ed1eb1` | 36 | 1 | 0 | J2ME M3G, drawPixels |
| 21 | Mundos, mapas, sprites | `Prince Of Persia 3 Portugal (teclas)/princepersia_tt.jar` | `eb16778a12aa0bac` | 6 | 6 | 0 | TiledLayer, drawRegion |
| 22 | Mundos, mapas, sprites | `Super Mario 2/MarioMp2.jar` | `16ede07fe8584bf2` | 16 | 18 | 6 | GameCanvas, Sprite, TiledLayer |
| 23 | Mundos, mapas, sprites | `Lemmings/Lemmings.jar` | `41f07e9dc3318123` | 9 | 34 | 7 | GameCanvas, drawRegion |
| 24 | Mundos, mapas, sprites | `Metal Slug/MetalSlug.jar` | `6ee6abe79fa3384a` | 3 | 5 | 0 | TiledLayer |
| 25 | Mundos, mapas, sprites | `Forsaken Fortress/ForsakenFortress.jar` | `b2123515834acbf6` | 5 | 5 | 1 | TiledLayer, drawRGB, drawRegion |
| 26 | Mundos, mapas, sprites | `Sabrewulf/sabrewulfmod.jar` | `f5bb40fc57fa1a77` | 2 | 20 | 0 | GameCanvas, TiledLayer |
| 27 | Mundos, mapas, sprites | `Arkanoid_Revenge_of_DOTH/Arkanoid_Revenge_of_DOTH_6230i.jar` | `419981c167210fe4` | 22 | 21 | 2 | GameCanvas, Sprite, TiledLayer |
| 28 | Mundos, mapas, sprites | `Atomic Betty/AtomicBetty-byhizir.jar` | `653f9f36ae9fa3e9` | 27 | 33 | 12 | Sprite, TiledLayer |
| 29 | Mundos, mapas, sprites | `Copia de Rayman3/Rayman3.jar` | `e0ebfff6e4d09917` | 5 | 1 | 0 | GameCanvas, drawRegion |
| 30 | Mundos, mapas, sprites | `Prince of Persia/PrinceOfPersia.jar` | `0496747ec2e54571` | 14 | 16 | 5 | GameCanvas, drawRegion |
| 31 | Mundos, mapas, sprites | `Splinter Cell/SplinterCell.jar` | `f6f67084e36fc572` | 29 | 40 | 0 | estrutura e assets |
| 32 | Mundos, mapas, sprites | `Prince Of Persia WW/Warior_Within_kr.jar` | `dc4613d8ca496141` | 5 | 0 | 0 | GameCanvas, drawRegion |
| 33 | Mundos, mapas, sprites | `828 Java Games/LotrTwoTowers.jar` | `b43de60be499614c` | 17 | 58 | 0 | estrutura e assets |
| 34 | Mundos, mapas, sprites | `Dragon Island/DragonIsland.jar` | `833ee0c0dd63b0f1` | 21 | 1 | 0 | estrutura e assets |
| 35 | Mundos, mapas, sprites | `Galleon Dawn/GalleonDawn.jar` | `dccfcc099abc54d5` | 5 | 47 | 4 | GameCanvas, drawRegion |
| 36 | Mundos, mapas, sprites | `Tomb Raider - Osiris Codex/TombRaide1osiriscodex.jar` | `53ff23af45a60829` | 5 | 1 | 1 | estrutura e assets |
| 37 | Mundos, mapas, sprites | `Underworld - Vampires Night/underworldVampiresNight.jar` | `dad3e0b342a6a4a7` | 12 | 15 | 0 | drawPixels |
| 38 | Mundos, mapas, sprites | `828 Java Games/DragonFire2Episode1.jar` | `fec5387bb46a363f` | 7 | 141 | 7 | estrutura e assets |
| 39 | Mundos, mapas, sprites | `828 Java Games/Scooby-Doo2DarkDungeons.jar` | `1d6f0b6fd11c1bbc` | 9 | 1 | 0 | estrutura e assets |
| 40 | Mundos, mapas, sprites | `Caveman/caveman.jar` | `e0161e5b70912972` | 10 | 28 | 0 | estrutura e assets |
| 41 | IA, regras e estratégia | `828 Java Games/1XCrossingDice.jar` | `8db1413d8135bfc3` | 25 | 23 | 0 | minimax |
| 42 | IA, regras e estratégia | `828 Java Games/AncientEmpires.jar` | `2dda1c490d878364` | 8 | 1 | 0 | drawPixels |
| 43 | IA, regras e estratégia | `Age of Empires 2/age_kr.jar` | `88895f7d3f1c792f` | 18 | 1 | 0 | drawPixels, drawRegion |
| 44 | IA, regras e estratégia | `AD 1503/anno_1503.jar` | `7437e29bc1ea3548` | 16 | 11 | 6 | estrutura e assets |
| 45 | IA, regras e estratégia | `Chess Buddy 3 (T720)/ChessBuddy3.jar` | `a09af1e67c5a9b3b` | 39 | 32 | 0 | estrutura e assets |
| 46 | IA, regras e estratégia | `Strategy War/StrategyWar-1[1].3.2.jar` | `1feea4b29398c20f` | 23 | 13 | 8 | estrutura e assets |
| 47 | IA, regras e estratégia | `828 Java Games/BattleOfEmpires.jar` | `b92476850bab71c9` | 12 | 75 | 0 | estrutura e assets |
| 48 | IA, regras e estratégia | `Empire Earth/200611230940787945.jar` | `b4520a37c965441b` | 2 | 73 | 1 | drawRegion |
| 49 | IA, regras e estratégia | `828 Java Games/Chessmaster.jar` | `a6c3b4e7de653f95` | 5 | 1 | 0 | drawPixels |
| 50 | IA, regras e estratégia | `NetMobileChess V.0.96/NetMobileChess.jar` | `55b180a980b1cc2b` | 22 | 50 | 0 | estrutura e assets |
| 51 | IA, regras e estratégia | `Soccer Manager/SoccerManager.jar` | `7735ee34ba383ab8` | 10 | 3 | 0 | drawPixels |
| 52 | IA, regras e estratégia | `828 Java Games/5Chess.jar` | `493f99e040eba120` | 6 | 3 | 0 | estrutura e assets |
| 53 | IA, regras e estratégia | `828 Java Games/ChessPuzzle.jar` | `41516940885040bb` | 9 | 4 | 0 | estrutura e assets |
| 54 | IA, regras e estratégia | `828 Java Games/ChineseChess.jar` | `fd6839865d23cafd` | 11 | 21 | 0 | drawPixels |
| 55 | IA, regras e estratégia | `Chess/SpruceChess.jar` | `019bed0ab5e9510e` | 7 | 72 | 0 | estrutura e assets |
| 56 | IA, regras e estratégia | `FiveStones/FiveStones.jar` | `ca2ac0f3a761209e` | 22 | 5 | 1 | GameCanvas |
| 57 | IA, regras e estratégia | `828 Java Games/ConcealedChess.jar` | `91a5793d3a8d57ce` | 29 | 37 | 0 | estrutura e assets |
| 58 | Arte, recursos e animação | `828 Java Games/WorldFighting.jar` | `d5d3da079ac379e9` | 13 | 127 | 18 | estrutura e assets |
| 59 | Arte, recursos e animação | `Speed Addict/SpeedAddict.jar` | `a42501ccf16b7e00` | 9 | 93 | 0 | GameCanvas |
| 60 | Arte, recursos e animação | `Agassi Tennis/AgassiTennis.jar` | `8e52c49e9e419c9b` | 2 | 87 | 9 | GameCanvas |
| 61 | Arte, recursos e animação | `C2S_ProBasebal/C2S_ProBaseball__v600_.jar` | `cbbc05ac00ad3624` | 4 | 115 | 14 | GameCanvas, Sprite |
| 62 | Arte, recursos e animação | `Dragon Fire/C2S__Dragon.jar` | `2ea836c6af6cb0ff` | 3 | 23 | 7 | estrutura e assets |
| 63 | Arte, recursos e animação | `King_Of_Fighters M2(sonido)/King_Of_Fighters_M2_K750.jar` | `fa19c43c48e7e587` | 9 | 4 | 3 | Sprite |
| 64 | Arte, recursos e animação | `828 Java Games/KamikazeQuest.jar` | `3a3bacdeac964a80` | 18 | 95 | 5 | GameCanvas |
| 65 | Arte, recursos e animação | `Racing Fever Deluxe 2/RacingFeverDeluxe2.jar` | `454b6b9b846ec70d` | 16 | 21 | 15 | drawPixels |
| 66 | Arte, recursos e animação | `828 Java Games/SpaceEncounter.jar` | `327a5cb31aa29a6f` | 18 | 63 | 0 | estrutura e assets |
| 67 | Arte, recursos e animação | `Puzzle Bobble/PuzzleBobble.jar` | `80e42bf52df75a45` | 10 | 40 | 3 | drawPixels |
| 68 | Arte, recursos e animação | `828 Java Games/5Goldminer.jar` | `ce01f323fe180887` | 9 | 19 | 0 | estrutura e assets |
| 69 | Arte, recursos e animação | `828 Java Games/EontheDragon.jar` | `26afb501d7baa333` | 7 | 26 | 16 | estrutura e assets |
| 70 | Arte, recursos e animação | `Com2Us Bowling 2/c2ubowling2.jar` | `f83ec4dc56cc9cb7` | 4 | 19 | 10 | GameCanvas, Sprite |
| 71 | Arte, recursos e animação | `Stealth/Stealth.jar` | `a61a572ffbf67fe2` | 5 | 28 | 6 | GameCanvas |
| 72 | Arte, recursos e animação | `Street Soccer/streetsoccer.jar` | `c058b21868b721d0` | 16 | 9 | 11 | drawPixels |
| 73 | Arte, recursos e animação | `Dragon Fire 2/dragon_fire2.jar` | `1407822bcd622f55` | 10 | 23 | 7 | drawPixels |
| 74 | Física, corrida e esportes | `828 Java Games/Colin McRae 04 (s60).jar` | `eb05f180891e1f8d` | 7 | 55 | 9 | estrutura e assets |
| 75 | Física, corrida e esportes | `V-Rally/vrally.jar` | `6da9561396445c91` | 14 | 8 | 0 | drawPixels |
| 76 | Física, corrida e esportes | `828 Java Games/RacingFever.jar` | `2fd5294dcb1b7130` | 9 | 7 | 5 | estrutura e assets |
| 77 | Física, corrida e esportes | `828 Java Games/AlonsoRacing.jar` | `94bcbb2f41105058` | 5 | 1 | 0 | drawPixels |
| 78 | Física, corrida e esportes | `Beach Rally/beachrally.jar` | `14f89ecbf00ce4e6` | 17 | 4 | 5 | drawPixels |
| 79 | Física, corrida e esportes | `Farm Racing/FarmRacing.jar` | `d691b7148bf9eb89` | 9 | 56 | 0 | GameCanvas |
| 80 | Física, corrida e esportes | `828 Java Games/Fifa2004.jar` | `cc731afda2bfb6d6` | 3 | 20 | 0 | estrutura e assets |
| 81 | Física, corrida e esportes | `828 Java Games/FIFA2005.jar` | `dce18d77d23d7dd4` | 3 | 22 | 4 | estrutura e assets |
| 82 | Física, corrida e esportes | `828 Java Games/SensibleSoccer.jar` | `2b22b8c7a1039077` | 30 | 1 | 0 | estrutura e assets |
| 83 | Física, corrida e esportes | `828 Java Games/SpaceTaxiPinball.jar` | `3a353fe99e21627c` | 11 | 8 | 0 | estrutura e assets |
| 84 | Física, corrida e esportes | `Icy Pinball/Icy Pinball.jar` | `112eb7c3ba7733cf` | 8 | 34 | 0 | GameCanvas |
| 85 | Física, corrida e esportes | `GP Pinball/GPPinball.jar` | `14ffb8a0614093f6` | 9 | 9 | 12 | estrutura e assets |
| 86 | Física, corrida e esportes | `Pinball Dreams/pinbdream.jar` | `42d466335da60c67` | 3 | 79 | 0 | estrutura e assets |
| 87 | Física, corrida e esportes | `828 Java Games/RaymanGolf.jar` | `03e77dd47bcf8147` | 6 | 1 | 0 | drawPixels |
| 88 | Física, corrida e esportes | `Kawai Kart/Kawai_kart_kr.jar` | `5a6f6133dd6a39cf` | 6 | 51 | 5 | GameCanvas |
| 89 | Compactação, áudio e minimalismo | `828 Java Games/SpaceAttack.jar` | `17f8b34603077764` | 12 | 4 | 0 | estrutura e assets |
| 90 | Compactação, áudio e minimalismo | `828 Java Games/SpaceTravel.jar` | `954ec9e0a69acbe7` | 7 | 1 | 0 | estrutura e assets |
| 91 | Compactação, áudio e minimalismo | `Tetris/tetris.jar` | `52714b323033b257` | 53 | 6 | 7 | drawPixels |
| 92 | Compactação, áudio e minimalismo | `Space Invaders/SpruceInvaders.jar` | `28ed3efc8184427e` | 12 | 0 | 0 | estrutura e assets |
| 93 | Compactação, áudio e minimalismo | `828 Java Games/Space Impact III.jar` | `413932bfdf18c0ba` | 11 | 8 | 7 | estrutura e assets |
| 94 | Compactação, áudio e minimalismo | `828 Java Games/7Zwerge.jar` | `6df7ffc301a3524a` | 10 | 15 | 8 | estrutura e assets |
| 95 | Compactação, áudio e minimalismo | `828 Java Games/DieHard.jar` | `42c9116c1b1933d8` | 8 | 2 | 11 | GameCanvas, drawRegion |
| 96 | Compactação, áudio e minimalismo | `828 Java Games/AbsolutePuzzle1.jar` | `4de25ce2e634a03a` | 49 | 10 | 10 | estrutura e assets |
| 97 | Compactação, áudio e minimalismo | `828 Java Games/Space Invaders.jar` | `8fb080ee4f7c4699` | 5 | 5 | 0 | estrutura e assets |
| 98 | Compactação, áudio e minimalismo | `828 Java Games/1000Words.jar` | `66cfeea9801ae9ac` | 5 | 1 | 0 | drawPixels |
| 99 | Compactação, áudio e minimalismo | `828 Java Games/AAFlak88.jar` | `ffb5580c8cf5f05c` | 7 | 21 | 6 | estrutura e assets |
| 100 | Compactação, áudio e minimalismo | `Space Warrior/SpaceWarrior.jar` | `2d9af4f5b5b2335e` | 16 | 13 | 0 | drawPixels |

## 25 reservas

| # | Área | Arquivo JAR exato | SHA prefixo | Classes | Imagens |
|---:|---|---|---|---:|---:|
| 1 | 3D e rasterização | `3D QBlast/3d_qblast.jar` | `286ac91396a4041d` | 12 | 16 |
| 2 | 3D e rasterização | `Xmas Gifts 3D/Xmas_Gifts_3D.jar` | `82c41d4a746ec3e9` | 14 | 0 |
| 3 | 3D e rasterização | `3D Boxing/3DBoxing.jar` | `6de103577398de73` | 7 | 8 |
| 4 | Mundos, mapas, sprites | `Mad Monkey (sonido)/Mad Monkey.jar` | `ac265a82ef05383d` | 12 | 34 |
| 5 | Mundos, mapas, sprites | `828 Java Games/MikisWorld.jar` | `ff78f2a545ad67cb` | 13 | 15 |
| 6 | IA, regras e estratégia | `KX3D Chess/KX3D Chess.jar` | `01af4daf2a76da6e` | 6 | 36 |
| 7 | IA, regras e estratégia | `Air Traffic/AirTraffic.jar` | `b180c06d53ea23c9` | 6 | 41 |
| 8 | IA, regras e estratégia | `Age Of Marco Polo Gold(sonido)/Age Of Marco Polo Gold.jar` | `c0ac2803ad62edbc` | 34 | 13 |
| 9 | Física, corrida e esportes | `Stuntman/stuntman.jar` | `9ea60fbe22b3201a` | 5 | 1 |
| 10 | Física, corrida e esportes | `Ballesteros 3D/Seve B 3D.jar` | `c5df487a27e39dfe` | 12 | 64 |
| 11 | Compactação, áudio e minimalismo | `Atomic Space Rocks/AtomicSpaceRocks.jar` | `5d64f0df7f85bfa1` | 12 | 0 |
| 12 | Compactação, áudio e minimalismo | `828 Java Games/PhotoPuzzle.jar` | `7de4c559cd6114d3` | 5 | 20 |
| 13 | Arte, recursos e animação | `Ex Bubble/EXBUBBLE.JAR` | `61cd3ba8a9b8ea63` | 40 | 236 |
| 14 | Arte, recursos e animação | `Forgotten Warrior (sonido)/Warrior_suite2.jar` | `f08c8034da70871f` | 2 | 181 |
| 15 | Arte, recursos e animação | `828 Java Games/GhostsnGoblins.jar` | `083213262d2922ec` | 4 | 195 |
| 16 | Arte, recursos e animação | `Condition Zero/stoperation_kr.jar` | `0e8834d696de2fad` | 52 | 237 |
| 17 | Arte, recursos e animação | `828 Java Games/ViolenceCombat.jar` | `c85397f627eca2e0` | 2 | 124 |
| 18 | Arte, recursos e animação | `Moto City/MotoCity.jar` | `9e4d006f9f0286e8` | 57 | 160 |
| 19 | Compactação, áudio e minimalismo | `Bomberman Panic/BombermanPanic.jar` | `75d8932f0a7d47d5` | 13 | 5 |
| 20 | Arte, recursos e animação | `Gaya/Gaya.jar` | `0609585cbbd5ff21` | 50 | 151 |
| 21 | Física, corrida e esportes | `Golf tour (cacho pantalla)/Golf Tour.jar` | `4b0047291c8d486e` | 50 | 73 |
| 22 | Arte, recursos e animação | `828 Java Games/Gangland.jar` | `2c0d116bdcfa4404` | 24 | 142 |
| 23 | Arte, recursos e animação | `RTL Racing 2005/In_Fusio_RTL_Racing_2005.jar` | `730a555b8386eb12` | 15 | 82 |
| 24 | Arte, recursos e animação | `Fireblaster/fireblaster.jar` | `2a01922ab9e7277f` | 3 | 88 |
| 25 | Arte, recursos e animação | `Tennis Pro/TennisPro.jar` | `b7334af7dbf1fb4d` | 12 | 83 |

## Protocolo para investigar, não apenas catalogar

1. Confirmar nome, hash, MIDP, JAD e capacidade de emulação de cada exemplar.
2. Analisar bytecode real de classes e métodos, distinguindo APIs referenciadas de chamadas que ocorrem em runtime.
3. Detectar famílias de motores por semelhança de classfiles, recursos e código; trocar variantes redundantes por reservas documentadas.
4. Reconstruir pseudocódigo autoral de algoritmos e explicar invariantes, estruturas de dados e limites.
5. Executar o original em emulador quando possível, registrar comportamento observado e contradições com hipóteses.
6. Selecionar os padrões realmente úteis à web moderna, desenvolver módulos autorais do PocketForge e integrá-los em jogo de referência.
7. Testar e fazer benchmarks comparativos antes de qualquer alegação de aumento de FPS, economia de RAM ou tamanho.

## Arquivos e continuidade

- selection-100.json contém 125 SHA-256 completos, nomes, caminhos JAR/JAD e perguntas técnicas individualizadas por candidato.
- selection-100.csv permite filtrar por frente, tamanho, origem e prioridade.
- A situação atual da engenharia reversa profunda permanece registrada em deep/registry.json: nenhum jogo promovido automaticamente.
- Script reprodutível: scripts/select_j2me_deep_studies.py.
- Testar candidaturas com amostras e revisar as reservas antes de iniciar engenharia completa do corpus selecionado.
