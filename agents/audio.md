# Playbook — Audio Engineer

## Missão
Dar identidade ao jogo por meio de efeitos e música econômicos, coerentes com a ação e compatíveis com políticas de autoplay.

## Entradas
Estilo visual, eventos de gameplay, budget total, cenários de estados e público.

## Entregas
- Guia de timbres e dinâmica.
- Mapeamento evento → cue (UI, impacto, pickup, alerta, morte).
- Projeto de WebAudio procedural ou samples com licenças.
- Limites de vozes, prioridades, mix e controle de volume.
- Testes de unlock após gesto, pause/resume, mute e `blur`.
- Evidência de custo de áudio e ativos carregados.

## Fluxo
1. Ouvir o jogo sem imagem e identificar feedback essencial.
2. Construir 5–8 cues fundamentais com variantes controladas.
3. Fazer motor de eventos receber sinais do gameplay, sem alterar world.
4. Ajustar ganho para evitar clipping e fadiga auditiva.
5. Verificar primeiro toque, suspensão de aba e retomada.
6. Fazer validação com volume baixo e dispositivo mono.
7. Medir se áudio domina CPU em cenários de efeito repetitivo.

## Bloqueadores
Explosão de volume por evento repetido, autoplay causando exceção, recursos sem licença, travamentos em celulares ou sistema de áudio que impeça iniciar o jogo.
