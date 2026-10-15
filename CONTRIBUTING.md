# Como contribuir com PocketForge

## Premissa
Contribuições devem melhorar **jogos reais**: correção, arte, ergonomia, desempenho ou reprodutibilidade. Evitar documentação que prometa capacidades que scripts não implementam.

## Propor alteração
1. Descrever problema observado e escopo.
2. Relacionar ao Game Brief/critério de aceite quando houver.
3. Criar alteração mínima acompanhada de testes e exemplos.
4. Rodar `python3 -m unittest discover -s tests -v`, `node --check demo/game.js` e `python3 scripts/audit.py demo`.
5. Quando alterações de gameplay afetarem input/estados, executar `python3 tests/browser_smoke.py` após instalar Playwright e Chromium; ou conferir o workflow GitHub Actions.
6. Informar impacto no tamanho final.
7. Documentar resultado **observado** e trabalho não testado.

## Diretrizes de código
- Sem dependências de runtime externas para o demo de referência.
- Preferir funções pequenas e contratos estáveis.
- Evitar alterar física e arte em um mesmo PR sem justificativa.
- Documentar licenças/proveniência de recursos.
- Separar bugs bloqueadores de melhorias cosméticas.

## Pull requests
Incluir: problema, mudança, como testar, evidências, impacto no bundle, riscos e compatibilidade. Capturas são úteis, mas não substituem reprodução do gameplay.
