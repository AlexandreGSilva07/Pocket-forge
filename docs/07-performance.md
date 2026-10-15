# 07 — Performance, profiling e orçamento de recursos

## Quatro dimensões distintas
1. **Transferência**: arquivos reais enviados (brutos, gzip/Brotli, cache).
2. **Startup**: download → parse → decode → primeira interação utilizável.
3. **Frame time**: CPU + GPU para render e simulação (p50, p95, p99).
4. **Pico de memória**: JS heap, texturas, Canvas, áudio e decodificação.

Não usar “FPS máximo” como única métrica. Um jogo pode exibir 60 FPS médios e travar perceptivelmente.

## Orçamento de partida (não promessa)
Para um microgame web, começar com 1 MB transferido e frame budget de 16,7 ms em dispositivo de referência; dividir o frame em simulação, desenho, entrada e folga. Para um projeto compacto, começar com 5 MB e reduzir após inspeção. Reajustar conforme escopo, arte e aparelhos escolhidos.

## Métricas a registrar
| Métrica | Método | O que prova |
| --- | --- | --- |
| Bytes brutos e gzip | `scripts/audit.py` | apenas peso local; não rede real |
| Startup e requests | DevTools/Performance | ordem/custo de inicialização |
| Tempo de frame | `performance.now`/Performance panel | distribuição de tempo de execução |
| Dropped frames | trace/performance overlay | experiência sob carga |
| Memória JS | ferramentas do navegador compatíveis | apenas parte da memória |
| Energia/temperatura | ensaio controlado em aparelho real | tendência térmica, não garantia universal |

## Plano de profiling
1. Executar build **sem** ferramentas de debug pesadas para medição base.
2. Fixar navegador, versão, dispositivo, modo de energia, DPR, resolução, cena e seed.
3. Rodar aquecimento, descartar transiente, repetir ensaios.
4. Medir a cena de pior caso (partículas, inimigos, colisões e UI).
5. Registrar p50/p95/p99 de `frameDt`, não apenas uma média.
6. Alterar **uma variável por vez** e comparar confiança do ganho.
7. Verificar se a otimização piora aparência, input ou acessibilidade.

## Hierarquia de otimização
- Remover trabalho desnecessário.
- Reduzir alocações e iterações desnecessárias.
- Culling fora da câmera e broad-phase de colisão.
- Agrupar sprites e minimizar troca de estado gráfico.
- Cachear efeitos estáticos, sombras, fontes e gradientes custosos.
- Comprimir assets sem destruir direção de arte.
- Carregar assets por cena e priorizar conteúdo jogável.
- Só depois considerar shader/custom engine/wasm.

## Delta time e estabilidade
Limitar `dt` ao retornar de aba suspensa. Para física consistente, usar simulação com passos fixos. Nunca atualizar movimento com “pixels por frame” sem dt se FPS variável for aceito.

## Limites do auditor v0.1
`scripts/audit.py` mede peso por extensão e compressão aproximada. Não mede memória GPU, energia, tráfego por rede, FPS ou tempo de parse. Relatórios nunca devem extrapolar essas métricas sem instrumentação real.

## Regressões
Definir no CI limite estático de peso e testes sintáticos; medir FPS e startup em ambiente controlado quando harness de navegador estiver instalado. Comparar contra baseline versionada; distinguir regressão causal de ruído experimental.
