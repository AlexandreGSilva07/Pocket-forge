# PocketForge J2ME — HTML único que abre por duplo clique

**Status: testado no Google Chrome do computador do usuário em 16/10/2026.**

O motor Java ME (VM JS2ME MIT, adaptadores PocketForge, ZIP, classes CLDC/MIDP, CSS e imagens da interface) foi integrado num **único arquivo HTML autossuficiente**, aberto diretamente usando o protocolo `file://`, sem servidor local ou remoto, sem CDN e sem Java instalado.

## Construir (somente o desenvolvedor)

```bash
python3 scripts/build_j2me_runtime.py             # Obter a VM open source uma vez
python3 scripts/build_j2me_single_html.py          # -> dist/PocketForge-J2ME-Offline.html
```

O HTML universal resultante permite selecionar ou arrastar um **JAR local** na própria página; o navegador não envia o arquivo para a Internet. Depois de gerado, **basta dar dois cliques no HTML**. Nenhuma instalação ou terminal será necessária para o jogador.

## Embutir também o próprio jogo no HTML

```bash
python3 scripts/build_j2me_single_html.py --jar ~/meu-jogo.jar --output dist/Meu-Jogo-Offline.html
```

O segundo HTML inclui os bytes originais do JAR codificados no documento e inicia o MIDlet automaticamente, sem outro arquivo. **Este tipo de HTML pode conter um jogo protegido por copyright: mantenha-o privado e jamais faça commit/distribuição de jogos comerciais sem permissão.** O compilador valida que a entrada é um ZIP/JAR e impõe limite de 64 MiB. Somente o gerador é publicado no repositório.

## Evidências verificadas (Chrome instalado em Debian, protocolo file://)

| Arquivo | Teste | Observações |
|---|---|---|
| `test.jar` upstream (2.219 bytes) | Selecionado no HTML universal | Manifesto reconhecido, 2 recursos, 8 entradas em métodos bytecode, **0 requisições externas e 0 page errors** |
| `asteroids.jar` upstream (16.048 bytes) | Selecionado no HTML universal | Tela Canvas 240×266, mais de 500 cores, frames não idênticos com tempo/teclado, **sem erros de página** |
| `asteroids.jar` upstream | JAR embutido em HTML de 591 KB | Abriu automaticamente pelo file://, renderizou 559 cores, frames mudaram, **0 requisições externas** |
| `AsphaltNitro.jar` 1.1.7 (SHA-256 `a96827c5c6539bcaff2d7d23f8bad0cf1dafd8d421af38f97664a25c49fcd9cf`) | JAR embutido em HTML particular de 3,3 MB | Canvas 240×320, aproximadamente 153 mil entradas no executor; **splash original renderizada, corrida ainda não funciona**, sem erros JS de página ou rede |
| Minecraft Classic J2ME local | JAR selecionado | Canvas criado, mas **falhou com API Mascot Capsule micro3D ausente**; motor não tem cobertura universal |

A verificação de frames do Asteroids compara instantes separados após envio de teclas. Ela demonstra renderização dinâmica, mas **não valida isoladamente causalidade de controles nem gameplay integral**.

O teste automatizado [`tests/browser_j2me_single_html.py`](../../tests/browser_j2me_single_html.py) usa o **Chrome de fato instalado no host quando disponível**, caso contrário o Chromium do Playwright. Exige manifesto real, entrada em bytecode, módulo embutido, **zero requisições externas**, gera screenshot e relatório JSON. O GitHub Actions roda esse teste sem servidor e constrói um HTML temporário com o MIDlet de referência; somente o HTML universal sem jogos é publicado no artefato.

## Limitações

- **RUN não equivale a PORT:** este HTML contém uma máquina virtual JavaScript e, ao embutir um JAR, carrega seu bytecode original. Não é uma tradução AOT do jogo para JS puro.
- `file://` funciona no **Chrome Linux testado**; navegadores com política diferente podem impor restrições. Não afirmar compatibilidade universal entre navegadores.
- O motor ainda tem MIDP/CLDC parciais, MMAPI, M3G/JSR 184, Mascot, Nokia UI e outros serviços incompletos. Um Canvas não é prova de jogo jogável.
- O HTML autônomo do **runtime** ocupa cerca de 569 KiB de arquivo não comprimido; inclui código-fonte JS e licença MIT/BSD. O HTML com JAR será maior porque incorpora os bytes do jogo em Base64.
- JARs de terceiros são código potencialmente não confiável: testar em perfil de navegador isolado, sem dados pessoais.

**Próxima etapa:** melhorar a compatibilidade do runtime para que o Asphalt Nitro saia do carregamento e entre em uma corrida. O formato de arquivo único está resolvido; a execução integral do Asphalt ainda não.
