# Pesquisa em escala: 2.309 JARs da coleção Nokia64 (2002–2005)

> **Data da auditoria:** 15/10/2026 (Cuiabá) / 16/10/2026 (UTC).
> **Método:** download e inspeção **estática** de um ZIP público em runner temporário do GitHub Actions. **Nenhum jogo foi executado e não foram redistribuídos JARs ou assets originais.**
> **Execução e evidência:** [GitHub Actions #38828578276](https://github.com/AlexandreGSilva07/Pocket-forge/actions/runs/38828578276).
> **Dados detalhados:** [artifact pocketforge-j2me1000-audit](https://github.com/AlexandreGSilva07/Pocket-forge/actions/runs/38828578276/artifacts/12016061528) (CSV/JSON/Markdown; validade configurada para 30 dias).
> **Corpus:** [Internet Archive — Nokia64, 1000 J2ME Games Pack](https://archive.org/details/1000_J2ME_Games_Pack).

## 1. Procedência e volume observado

O nome comercial da coleção sugere “1000+ jogos”, mas **a contagem foi feita nos arquivos reais**, não baseada na descrição do site.

| Indicador | Resultado observado |
|---|---:|
| Arquivo original | \`1000JavaGames.zip\` |
| Tamanho | 161.222.413 bytes (~153,8 MiB) |
| Entradas no ZIP externo | 7.283 |
| Arquivos JAR processados com sucesso | **2.309** |
| SHA-256 distintos | **1.649** |
| Duplicatas exatas | 660 |
| Falhas de leitura | 8 |
| Mediana do tamanho JAR | 53.959 bytes |
| Percentil 90 de tamanho JAR | 123.842 bytes |
| Maior JAR | 702.126 bytes |
| Menor JAR | 2.127 bytes |

**Limite conceitual:** 1.649 JARs com hashes distintos não significam 1.649 títulos. Um único jogo pode possuir builds para aparelhos, idiomas e resoluções diferentes. Inversamente, arquivos com o mesmo conteúdo são duplicatas exatas.

### Conteúdo total dos JARs analisados

| Recurso | Ocorrências |
|---|---:|
| Classfiles Java | **26.263** |
| Imagens (pela extensão) | **41.975** |
| PNGs indexados por paleta | **35.794** |
| PNGs truecolor/gray (conforme cabeçalho) | 5.734 |
| Arquivos de áudio | **3.320** |
| Outros recursos não classificados | 15.277 |

Esses totais **incluem conteúdos repetidos em JARs duplicados** e não equivalem a um inventário de assets únicos.

## 2. Perfis e APIs reconhecidas

### Perfis declarados

| Perfil MIDP | JARs |
|---|---:|
| MIDP 1.0 | 2.078 |
| MIDP 2.0 | 133 |
| Não identificado | 98 |

### Presença de referências no bytecode

| API ou símbolo | JARs com referência |
|---|---:|
| \`javax.microedition.lcdui.Graphics\` | 2.288 |
| \`javax.microedition.rms.RecordStore\` | 1.904 |
| \`java.lang.Thread\` | 1.923 |
| \`com.nokia.mid.ui.DirectGraphics\` | **630** |
| \`javax.microedition.media.Manager\` | 354 |
| \`GameCanvas\` | 78 |
| \`Sprite\` (API J2ME Game) | 19 |
| \`TiledLayer\` | 12 |
| \`javax.microedition.m3g\` | 19 |
| \`java.lang.Float\` | 3 |
| Bluetooth | 2 |
| FileConnection | 1 |

**Importante:** encontrar uma referência em um \`.class\` indica presença no bytecode; não demonstra frequência de chamada ou que o caminho gráfico é dominante na execução. “Float operations” aqui significa referência a \`java.lang.Float\`, **não** um detector de opcodes de ponto flutuante.

## 3. O que aprendemos e o que ainda precisa de prova

### P0 — paletas e formatos compactos
A presença de 35.794 PNGs indexados é uma forte evidência de uso frequente de paletas neste acervo, coerente com um ambiente de download e memória limitados. **Não é prova** de que PNG indexado seja sempre a melhor escolha na web atual; comparar também PNG, WebP, AVIF, sprites em atlas e memória decodificada.

### P0 — especializações de renderização
630 JARs referenciam Nokia DirectGraphics. São bons candidatos para estudos aprofundados de estratégias de bitmap/pixel e de primitivas gráficas específicas. Isto **não prova** que usem rasterização 3D, nem que um algoritmo específico seja superior em CPUs/GPU modernas.

### P0 — persistência simples
1.904 JARs referenciam RMS RecordStore. No PocketForge, podemos estabelecer uma API mínima para snapshots/versionamento e medir custo e robustez, mas sem presumir que RMS antigo deve ser reproduzido.

### P1 — orçamentos de temporalidade
1.923 JARs referenciam Thread. Não confundir presença de \`Thread\` com implementação adequada de frame pacing. Requer desmontagem de loops e reconstrução do comportamento.

### P1 — recursos em massa e deduplicação
660 arquivos são duplicatas exatas; a etapa seguinte é agrupar **variantes** do mesmo jogo por recursos e bytecode semelhante, antes de interpretar a coleção como ampla diversidade arquitetural.

## 4. Plano para revisar a skill

| Prioridade | Trabalho | Critério de aceitação |
|---|---|---|
| P0 | Fingerprints por classes e assets para clusterização por motor/família | Detectar variantes além de hashes idênticos com amostra manual validada |
| P0 | Selecionar 30–50 títulos estruturalmente diversos | Justificativa por clusters, tipo de renderização e tamanho |
| P0 | Desmontagem dirigida de render loops, atlas, tilemaps, animações, IA e formatos de níveis | Diagrama, pseudocódigo próprio, medidas estáticas e validação cruzada |
| P0 | Recriar padrões com componentes próprios em Canvas/WebGL | Demonstrações completas e executáveis |
| P0 | Comparar implementações no mesmo dispositivo | Tamanho transferido, carga, RAM, frame time e qualidade visual |
| P1 | Atualizar módulos \`docs/03\`, \`docs/04\`, \`docs/05\`, \`docs/07\` e \`docs/16\` | Regras referenciam experimentos comparáveis e evidência |
| P1 | Integrar padrões vencedores em generators e templates | Testes de regressão e demo jogável por família |

O objetivo do PocketForge **continua sendo jogos modernos ultraleves** com liberdade estética. O acervo J2ME serve como fonte de hipóteses para engenharia, não como limitação de linguagem, tecnologia ou estilo.

## 5. Reprodutibilidade, restrições e segurança

- Workflow: [\`.github/workflows/j2me-research.yml\`](../../.github/workflows/j2me-research.yml).
- Auditor: [\`scripts/audit_j2me_archive.py\`](../../scripts/audit_j2me_archive.py).
- Download feito para o diretório temporário do runner; arquivo ZIP original descartado ao terminar.
- Sem instalação nem execução de MIDlets, sem extração executável em disco; arquivos de classe foram inspecionados como bytes.
- Os resultados CSV e JSON foram guardados apenas como artifact do Actions, e podem ser baixados separadamente do acervo.
- A coleção é pública para acesso, mas isso não representa declaração de domínio público para cada jogo.
- As oito falhas de leitura precisam ser caracterizadas antes de declarar cobertura completa do corpus.
- Um zip externo pode conter formatos e imagens sem extensão não reconhecidos pela heurística atual.

**Status:** auditoria estrutural de 2.309 JARs concluída; engenharia reversa aprofundada, implementação de componentes derivados e benchmarks reais continuam pendentes.