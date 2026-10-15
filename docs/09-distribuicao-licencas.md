# 09 — Empacotamento, segurança, licenças e distribuição

## Distribuição web
- Permitir servir por servidor estático simples.
- Preferir assets locais; CDN deve ser opt-in e registrada.
- Sem coleta de dados por padrão e sem trackers.
- Versionar recursos e evitar caches inconsistentes em atualizações.
- Se instalar como PWA, criar manifest e service worker com política explícita de atualização/cache; **v0.1 do demo não contém PWA**.
- Respeitar `prefers-reduced-motion`, áudio só por interação e áreas seguras de touch.

## Política offline
Classificar:
1. `offline-file`: funciona ao abrir o HTML com `file://`.
2. `offline-server`: requer servidor HTTP local, mas nenhum recurso externo.
3. `offline-after-install`: PWA/cache após primeira instalação.

A versão demonstrativa usa `offline-file` (script clássico e CSS locais); servir com `http.server` continua recomendado. Não afirmar PWA sem service worker.

## Ativos de terceiros
Manter `assets/ATTRIBUTION.md` ou manifesto com autor, origem, URL e licença. Respeitar requisitos de atribuição, SA, redistribuição e marcas registradas. Um prompt que gera “um Mario idêntico” não elimina riscos de propriedade intelectual.

## Suprimentos
- Preferir dependências fixadas e revisadas.
- Usar `npm audit` apenas quando existir projeto npm; não adicionar npm apenas para rodar um demo standalone.
- Auditar recursos remotos, scripts inline e permissões.
- Não armazenar segredos/API keys no jogo cliente.
- Validar entrada do usuário se existir editor, ranking ou importação de arquivos.
- Se usar modelos de IA, documentar proveniência de dados e licença dos pesos quando aplicável.

## Responsividade e input
Não confiar em `hover` no celular. Botões essenciais com área de toque confortável, feedback claro, contraste e orientação de tela prevista. Testar com menu de acessibilidade e reduced motion.

## Checklist de release
1. Build sem erro.
2. Load com conexão desligada quando promessa for offline.
3. Controles em dispositivo-alvo.
4. Nenhum recurso quebrado.
5. Metas de tamanho verificadas.
6. Bugs conhecidos documentados.
7. Licenças/atribuição auditadas.
8. Mensagens e screenshots de lançamento representam o jogo executável.
9. Propriedade e direitos de distribuição confirmados.
10. Versão, commit e alterações descritos.
