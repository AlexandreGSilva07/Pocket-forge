# PocketForge AOT — áudio IMA ADPCM para Java ME (sem servidor)

## Diagnóstico reproduzido em 17/10/2026

O Asphalt Nitro J2ME já compila e executa uma corrida no Chrome, porém exibia:

```
MMAPI playback failed: The element has no supported sources.
```

A causa foi confirmada **nos bytes do áudio original em execução**, não inferida pelo tipo MIME: o BrowserPlayer carregava **25 elementos `audio/x-wav`**; todos eram contêineres RIFF/WAVE com `wFormatTag=0x0011` (**IMA/DVI ADPCM**), 8000 Hz, mono, blocos de 256 bytes. O Chrome reconhecia o tipo WAV mas marcava `MEDIA_ERR_SRC_NOT_SUPPORTED (4)` para todos os elementos (`networkState=3`).

## Correção geral da plataforma

- `compiler/teavm-aot/src/main/java/pocketforge/media/ImaAdpcmWav.java`: conversão determinística RIFF/WAVE IMA ADPCM (4 bits) → WAV PCM 16 bits, em Java compilável pelo TeaVM. Suporta mono e estéreo, preditor e índice por bloco, fator de passo, `fact`/quantidade de amostras, limites de tamanho e validação de dados.
- `BrowserPlayer` detecta esse formato **pelos bytes do WAV**, independentemente do nome do jogo; normaliza o stream antes de criar o elemento `HTMLAudioElement`. A API Java ME do programa permanece `Manager.createPlayer(...)` com o mesmo `Player`, seus estados e controles. O HTML gerado segue sem JAR, sem JVM, sem FFmpeg, sem bibliotecas remotas e sem servidor.
- WAV PCM, MP3 e outros codecs anteriormente suportados não passam pela conversão de ADPCM.
- As fontes proprietárias do jogo não entram no Git; o áudio é interpretado **em runtime** a partir dos recursos do JAR transformados no momento da compilação.

## Testes no computador do usuário

1. Extração privada de um dos 25 efeitos ADPCM da execução real: decodificação Java com **2.188 amostras mono PCM 16-bit idênticas às decodificadas pelo FFmpeg**.
2. WAV IMA ADPCM **estéreo** produzido localmente e decodificado por ambas as ferramentas: **5.000 quadros × 2 canais iguais amostra por amostra**.
3. Recompilação privada do Asphalt Nitro: **25/25 elementos de áudio com `wFormatTag=1` (PCM)**, 25/25 `readyState=4`, **zero erros de mídia**, zero `MMAPI playback failed` e zero requisições de rede na inspeção da tela principal.
4. Com **gesto real de mouse** no Chrome, a promessa `HTMLAudioElement.play()` foi concluída com sucesso para um dos áudios decodificados; seu relógio avançou até o fim (`0,2735s`), sem exceções. Isso demonstra reprodução no navegador, mas o volume físico das caixas de som do usuário deve ser confirmado por ele.
5. Uma nova fixture **`AdpcmMIDlet.java`** com IMA ADPCM gerado no próprio teste foi adicionada a `tests/browser_j2me_aot_compiler.py`. Os **nove JARs autorais** passaram em HTML `file://` no Chrome: leitura dos bytes de RIFF PCM na página, evento de áudio reproduzível após gesto, preservação de desenho/teclado/outros codecs.

Arquivo privado atualizado: `~/Downloads/PocketForge-Asphalt-Nitro-AOT-Com-Som.html` (aproximadamente 10,7 MB).

## Limitações e próximos passos

- **MIDI ainda não implementado**. Alguns JARs Java ME também usam `audio/midi` ou formatos proprietários; esses continuam exigindo sintetizador/conversor e testes gerais. A presente correção cobre efeitos **IMA ADPCM**, não garante música ou áudio completo de todos os jogos.
- Nem todo formato WAV é PCM ou IMA; outros tipos precisarão de decodificadores próprios.
- Políticas do navegador podem bloquear reprodução automática antes de um gesto do usuário; jogos carregados em arquivo `file://` continuam sujeitos a essa restrição.
- A confirmação de que o usuário efetivamente escuta os efeitos depende de verificar o volume, dispositivo de saída e o HTML atualizado no Chrome.
- A detecção e conversão são generalistas; **não** há condicionais específicas para Asphalt Nitro.

## Uso

```bash
python3 scripts/compile_j2me_aot.py Jogo.jar --out Jogo-Com-Som.html
```

O computador que compila usa JDK, Maven e TeaVM; o arquivo HTML final é autônomo e offline.

## Evolução posterior: música MIDI

O [marco MIDI com FluidSynth](midi-offline-soundfont.md) adicionou conversão automática de SMF para Ogg/Opus no build. Assim, o suporte MIDI anteriormente ausente foi implementado e testado com a música do Asphalt e um JAR autoral. Permanecem limites de timbres e formatos opcionais.
