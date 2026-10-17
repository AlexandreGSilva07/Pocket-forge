# PocketForge: música MIDI Java ME → HTML autônomo com áudio real

**Status em 17/10/2026:** implementado e validado no computador do usuário e em 10 JARs independentes.

## O problema

A modalidade AOT do PocketForge já executava uma corrida do Asphalt Nitro em HTML e havia recuperado efeitos WAV IMA ADPCM. Mas a música continuava ausente porque o Chrome não sintetiza Standard MIDI Files (SMF) como arquivos `<audio>`. O jogo armazena suas músicas junto com outros recursos num banco binário, não em arquivos `.mid` nomeados.

## O que foi implementado — motor genérico, sem modificações no jogo

- `scripts/j2me_midi_renderer.py`: pesquisa `MThd` e valida cabeçalhos e comprimentos de trilhas `MTrk` em **qualquer recurso do JAR**, inclusive bancos proprietários e arquivos `.mid` convencionais. Suporta Standard MIDI File formato 0/1, controle de andamento (tempo), program change, note on/off, CC, pitch bend e canal de percussão. Impõe limites de duração, eventos, tamanho e contagem.
- Usa **libfluidsynth** e um banco de instrumentos SoundFont *apenas durante a compilação* para sintetizar os eventos. Comprime o PCM como **Ogg/Opus** por FFmpeg e inclui a mídia resultante em Base64 no HTML único.
- `BrowserPlayer` aceita MIDI via MMAPI `Manager.createPlayer(InputStream, "audio/midi")` e variantes `audio/x-midi`, `audio/sp-midi`. Faz associação **determinística pelos bytes exatos do stream MIDI** ao áudio previamente gerado. O tipo exposto via `getContentType()` preserva o MIME original.
- O desbloqueio de áudio do Chrome é compartilhado por todos os jogos: um `Player.start()` anterior à primeira interação é retomado num evento `pointerdown` ou `keydown` real, e `stop()`/ `close()` anulam a retomada. Não há código específico para Asphalt.
- O HTML continua **offline** via `file://`: nenhuma JVM, runtime Java interpretado, dependência de CDN, Java instalado, SoundFont ou ferramenta de síntese é necessária **no navegador**.

## Resultado real — Asphalt Nitro 1.1.7

O JAR (SHA-256 `a96827c5c6539bcaff2d7d23f8bad0cf1dafd8d421af38f97664a25c49fcd9cf`) continha **8 músicas MIDI** no banco binário de recursos `10`. Todas foram extraídas e sintetizadas automaticamente sem regras por título. Durações MIDI encontradas: aproximadamente 46,1 s; 76,8 s; 84,3 s; 63,8 s; 63,8 s; 63,8 s; 7,5 s; 9,3 s.

O compilador criou um HTML único de **15.281.944 bytes**, com ~3,27 MB de mídia musical Ogg original de síntese (antes da codificação Base64), mais código e recursos gráficos. Local:

`~/Downloads/PocketForge-Asphalt-Nitro-AOT-Musica.html`

**Verificação Playwright Chromium em file://:** oito faixas incorporadas, 26 objetos de áudio após inicialização (25 WAV/PCM + 1 Ogg de música); três músicas distintas foram instanciadas durante o fluxo de menus. Uma música ficou em reprodução, com duração Ogg ~78 s e relógio avançando, zero erros de decodificação, zero exceções de página e zero requisições externas.

**Política de reprodução automática:** antes de interagir, a música do menu estava pausada com a flag de gesto pendente. Após o primeiro clique no botão `OK / 5`, passou para `paused=false`, `readyState=4`, relógio em aproximadamente 0,82 s; depois avançou até 3,21 s sem erros ou avisos. Isso prova que o Chrome está **reproduzindo a mídia**, mas o som audível nos alto-falantes depende de confirmação humana no computador.

## Testes e requisitos de compilação

`tests/browser_j2me_aot_compiler.py` inclui agora **10 JARs autorais**. O novo `MidiMIDlet.java` é compilado pelo TeaVM e inicia um MIDI format 0 criado durante o teste, convertendo-o a Ogg/Opus e verificando som pronto e relógio avançando em Chromium, sem rede nem Java no navegador.

Para compilar JARs com MIDI na máquina de desenvolvimento:

```bash
# Debian/Ubuntu, máquina de build — NÃO no navegador
sudo apt-get install libfluidsynth3 timgm6mb-soundfont ffmpeg
python3 scripts/compile_j2me_aot.py Jogo.jar --out Jogo-Com-Musica.html
```

O compilador identifica o banco GM do sistema; opcionalmente, `POCKETFORGE_SOUNDFONT=/caminho/GM.sf2` escolhe outro banco. JARs sem MIDI continuam compilando mesmo sem FluidSynth. Se encontrar MIDI e não houver sintetizador/banco, o compilador interrompe com mensagem explícita, sem distribuir HTML falsamente silencioso.

## Qualidade e licenciamento

- A sequência de notas e o tempo vêm do MIDI **original**; os timbres sintetizados variam conforme o SoundFont, portanto podem **não ser idênticos aos do celular original**.
- **TimGM6mb.sf2**, instalado no PC, é disponibilizado pelo Debian sob **GPL-2** (ver `/usr/share/doc/timgm6mb-soundfont/copyright`). A fonte sonora **não é copiada** para o código do PocketForge, mas os arquivos de áudio gerados podem incorporar amostras derivadas dela. Avaliar licenças antes de distribuir HTMLs que incluam essa mídia; o HTML de Asphalt e seus assets comerciais foram mantidos **privados no computador**.
- Suporte coberto: SMF tipo 0 e 1; não são cobertos formatos SMAF/MMF, RMF, arquivos criptografados ou MIDI de formato 2. Tracks com duração superior a 360 s ou recursos fora dos limites são rejeitados.
- A renderização MIDI é feita **no build**, não em tempo real no navegador. Isso garante HTML independente do sintetizador, ao custo de aumentar o tamanho do arquivo.
- Ainda não há certificação de compatibilidade com todos os jogos Java ME ou de identidade exata de instrumentos e mixagem.

## Referências de implementação

- [FluidSynth](https://www.fluidsynth.org/)
- [Standard MIDI Files 1.0 — MIDI Association](https://midi.org/standard-midi-files)
- [FFmpeg / libopus](https://ffmpeg.org/ffmpeg-codecs.html)
