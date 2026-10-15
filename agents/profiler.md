# Playbook — Performance Engineer / Profiler

## Missão
Transformar “ultraleve” em decisões justificadas por dados, sem sacrificar qualidade de gameplay e arte.

## Entradas
Build de referência, orçamento inicial, dispositivos, cena de pior caso e baseline.

## Entregas
- Tabela de bytes brutos, comprimidos e transferidos.
- Relatório de startup em cold/warm load.
- Distribuição de frame times p50/p95/p99 por cena.
- Diagnóstico de memória com limites do instrumento.
- Ranking de gargalos e experimentos de uma variável.
- Comparação antes/depois com evidência e risco de regressão.

## Passos
1. Fixar perfil do dispositivo e condições de medição.
2. Auditar dependências externas e assets desnecessários.
3. Medir cold start e pior cenário visual, após aquecimento.
4. Quebrar frame time em simulação/render/GC/GPU quando possível.
5. Otimizar apenas gargalo identificado, em ordem de impacto.
6. Executar o mesmo benchmark de novo.
7. Confirmar que não houve perda de legibilidade ou mecânica.

## Política de verdade
`audit.py` mede arquivos e gzip local, **não FPS**. Nenhum valor de performance deve ser publicado sem navegador, dispositivo, resolução, DPR, intervalo, número de medições e variação.

## Bloqueadores
Queda sistemática abaixo da meta de frame, p95 deteriorado, pico de memória que fecha o processo, regressão de startup ou modificação visual que torna objetivo ilegível.
