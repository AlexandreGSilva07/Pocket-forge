# Aquisição comprovada de fontes móveis — 16/10/2026

**Resultado: 12 downloads verificados, 3 tentativas sem sucesso; 129.873.112 bytes no total (123,9 MiB).**

Execução: https://github.com/AlexandreGSilva07/Pocket-forge/actions/runs/38984198862

**Método:** scripts/research_fetch_legacy_sources.py (verifica formato, SHA-256, lista ZIP, amostra limitada de APIs sem executar software), e workflow .github/workflows/legacy-source-acquisition.yml. Artefatos expiram em cinco dias. Os hashes foram revalidados numa sandbox separada, após transferência dos três artefatos. **O CI terminou com sucesso, mas o êxito do CI não significa êxito individual dos 15 downloads.**

| Arquivo | Bytes | SHA-256 |
|---|---:|---|
| FreeJ2ME — código-fonte | 777.528 | 3575e5b3fc7ac29a8ba19d70682fbea167b8a1662655b17355977f585831335f |
| FreeJ2ME-Pro — fonte | 1.387.822 | 8787f310ee39040c6086468ec5823dc7243b6837ca08a705febd472d25db462f |
| J2ME Loader — fonte | 5.599.168 | 6a25b981a4ea70255b4b8ece6d093501bba95d721c4dbc979cb7555a560613ae |
| EKA2L1 — fonte | 34.259.339 | 26720d413af31d8a7c772881742483e3e71b37b9f06918eaeb900557caf38779 |
| SquirrelJME — fonte | 23.562.122 | cbc171993c7d92dff8214fbf26e3ecedc2352fab983c25ca797842002234baa9 |
| phoneME — fonte Git | 38.530.851 | b469a5024fdbbfca0cdc4d5bbfc6f8dfa2ab689ed35e8d6df11162517f3a6117 |
| phoneME MR2 Linux/x86 — runtime | 5.283.505 | 386558f0f4abcf9c5a4eb80ddecc36f527937b47825349f3f0ed1077bdc0728d |
| phoneME MR2 Linux/ARM — runtime | 5.379.672 | 5d59c102d973e31ed5f494465d4f6df7f033768408a20e6f816fbe7c6bb69f8e |
| phoneME MR2 Windows/x86 — runtime | 5.342.365 | e7aa3b464d653bfd88a24c26a50f448eb0582e6479697debb7b62f6c84906619 |
| Symbian-Archive — índice | 237.654 | 246965f7d63a01876fe68fed1adb2861e60a30b9ebd41f169451cd13751c3821 |
| BlackBerry JDE-Samples — fonte | 8.041.248 | 020dff3e3fa286fb4296557f92b9d774d34d1fd9d02af9f93550ceafbeb74443 |
| DoJa 5.x — guia PDF | 1.471.838 | b40a7cd9ffe004b9e0cfc0c07f8f33fd5a2ab9bfd493cf22ed1ccb5b9875d517 |

## Pendências comprovadas

1. **phoneME MR2 source b23 (ZIP histórico):** servidor retornou HTTP 404. O arquivo Git de phoneME foi obtido, mas não é prova de que o snapshot exato b23 esteja representado.
2. **Palm-dev-docs:** pacote excedeu teto de 85 MiB por recurso. Não é erro de autenticação confirmado.
3. **J2ME Polish:** pacote excedeu teto de 85 MiB por recurso.

Esses 15 alvos representam downloads diretos selecionados do catálogo maior. Muitas das 39 URLs originais são páginas, índices, SDKs restritos ou links para terceiros, e **não** se deve afirmar que todos os SDKs, SOs e firmwares foram baixados.

## Descobertas da leitura real dos arquivos

- **FreeJ2ME:** ZIP contém implementações/classes Java das famílias M3G/JSR 184, incluindo Graphics3D, Camera, Image2D e AnimationController; Nokia DirectGraphics; e Mascot Capsule micro3D v3. Isso comprova presença de fontes, não conformidade plena.
- **FreeJ2ME-Pro:** variantes dessas APIs; o README menciona mudanças em DirectGraphics.drawImage, entrada TextField/TextBox, M3G e Mascot Capsule. Uma comparação de implementações reais, e não apenas de APIs de nome igual, é a próxima tarefa.
- **J2ME Loader:** código nativo C++ sob app/src/main/cpp/m3g/ e headers javax_microedition_m3g_*. Pode esclarecer ponte Java-nativo, alocação, renderização e overhead, mas nada foi executado.
- **phoneME fonte:** 15.939 entradas ZIP (11.513 arquivos não-diretório), incluindo componentes cldc, midp, jsr135, jsr239, pcsl, pisces e preverifier. Também há implementação de RecordStore e camadas de UI. A análise separada do runtime é essencial para não atribuir otimizações da VM ao jogo.
- **phoneME MR2:** Windows/x86 contém runMidlet.exe e preverify.exe, além de bibliotecas e classes; os três ZIPs contêm milhares de classes e ferramentas. Não houve teste de compatibilidade em sistemas atuais.
- **Symbian-Archive:** o ZIP contém principalmente links/documentação, não o SDK proprietário completo.
- **BlackBerry JDE-Samples:** inventário inclui mais de 400 arquivos Java; as amostras não são um JDE completo.
- **DoJa:** obtido manual/guia PDF, não instalador de SDK.
- **EKA2L1** e **SquirrelJME** são fontes de projetos de emulação/VM, **não** ROMs ou provas de que os 100 JARs selecionados funcionarão.

## Como usar no PocketForge

Prioridade: estudar operações reais de GameCanvas, DirectGraphics, M3G e Mascot Capsule em emuladores diferentes; avaliar source nativo do J2ME Loader e VM do phoneME; usar JARs do corpus apenas temporariamente, checar hashes e comparar comportamento observado. Quando houver achado aplicável, implementar **código próprio HTML5** e medir peso, memória, FPS e fidelidade contra baseline.

**Limites:** zero jogos originais executados nesta aquisição, zero SDKs proprietários instalados, zero benchmarks e zero novas reconstruções integrais. Não atualizar o estado dos 100 jogos sem evidência. Nada baixado foi commitado. Não atrelar o motor a Nokia/Symbian: continuam sendo fontes históricas entre várias outras plataformas.
