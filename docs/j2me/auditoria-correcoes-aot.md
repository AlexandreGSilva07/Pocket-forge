# PocketForge — correção de RMS, teclado, tempo, resolução e logs

**17/10/2026.** Auditoria do HTML AOT do Asphalt Nitro revelou falhas reais, independentes do jogo. Foram corrigidas na biblioteca compartilhada e no compilador TeaVM, sem patches no JAR.

## 1. RMS persistente

A versão anterior de `javax.microedition.rms.RecordStore` mantinha registros somente em `HashMap`/memória. Um teste autoral Java ME com três carregamentos do mesmo HTML em Chrome demonstrou: **0→1, 0→1, 0→1** (perda de dados).

Agora um registro contém IDs estáveis e dados serializados em hexadecimal armazenados sincronicamente em `localStorage`. A chave contém um namespace de aplicativo derivado de fabricante, nome e classe MIDlet, para isolar aplicativos diferentes e manter o mesmo namespace entre recompilações. O método `openRecordStore` recupera o armazenamento ao abrir o HTML novamente. As gravações implementam rollback em caso de erro por quota/bloqueio. O armazenamento é local ao navegador, sem servidor.

Limitações: a API não pretende replicar todas as exceções e fluxos de RMS especificados pela JSR-118; a persistência de `file://` depende do navegador/perfil e **pode ser isolada por caminho/nome do arquivo HTML**. Não há migração automática entre arquivos renomeados. Dados anteriores à correção, que nunca chegaram ao disco, não podem ser recuperados.

## 2. Evitar eventos duplicados de teclado

Quando um botão do painel `#pf-controls` estava focado e o usuário pressionava Enter ou Espaço, o listener global de MIDP recebia a tecla nativa e o handler do botão emitia sua tecla virtual. O listener compartilhado agora ignora **eventos cujo alvo é um botão do painel**; o botão emite uma única tecla virtual. Teclas pressionadas fora dos controles continuam tratadas normalmente.

## 3. TempoControl sem overflow

O cálculo anterior `tempo*100000` usava inteiros de 32 bits no Java, estourava e podia produzir velocidade negativa (`-0.07374×` em 120 BPM). Passou a usar multiplicação `long` com conversão explícita segura antes de configurar o `HTMLAudioElement.playbackRate`. A regressão verifica 144 BPM = 1,2×.

## 4. Configuração de resolução

A API geral de Canvas/Displayable/Graphics usa `PocketForgeConfig.screenWidth/screenHeight`, gerados pelo compilador, em vez de dimensões fixas em todas as camadas. Novo argumento de compilação: `--screen 320x240`, ou outra resolução até 1024×1024. O valor padrão permanece **240×320**, preservando o Asphalt.

A alternativa é um perfil de tela por compilação, não um redimensionamento dinâmico inteligente de jogos que pressupõem dimensões específicas. A conformidade de cada jogo/perfil precisa ser verificada.

## 5. Logs limitados

O console visível no HTML limita cada mensagem a 4.000 caracteres e o histórico retido a 40.000 caracteres, em vez de crescer indefinidamente. A depuração do próprio navegador permanece disponível.

## Validação de regressão

`tests/browser_j2me_aot_compiler.py` compilou os programas autorais de cálculos, recursos, Canvas, input, MMAPI, ADPCM, MIDI e novos casos de **RMS persistente** e **tela 320×240**, e os abriu em Chromium por `file://`. Verifica salvamento após `page.reload()`, ausência de dupla confirmação em botão focado, velocidade de áudio, tamanho da tela e teto dos logs.

Para atualizar o Asphalt Nitro original:

```bash
python3 scripts/compile_j2me_aot.py AsphaltNitro.jar --out AsphaltNitro-Corrigido.html
```

A cópia comercial do jogo e o HTML final **não devem ser publicados no repositório**. Para tentar continuar o progresso após recompilar, utilizar o mesmo navegador/perfil e preferencialmente o mesmo caminho do arquivo; como o HTML antigo não gravava RMS persistente, progresso antigo não é recuperável.
