# Playbooks do PocketForge

Os oito playbooks são **responsabilidades orientadas por contratos**, não agentes residentes ou processos paralelos já implementados. Um único agente pode percorrê-los em passagens sucessivas; harness multiagente é trabalho futuro.

| Papel | Escopo principal | Handoff |
| --- | --- | --- |
| [Director](director.md) | visão, brief, limites | brief e critérios |
| [Architect](architect.md) | stack, contratos, estados | módulos e ADRs |
| [Gameplay](gameplay.md) | mecânicas e controles | jogo interativo, testes |
| [Visual](visual.md) | art bible e produção de assets | assets, proveniência |
| [Audio](audio.md) | trilha, cues, WebAudio | eventos e teste de áudio |
| [Profiler](profiler.md) | medições e gargalos | relatórios e comparações |
| [Reviewer](reviewer.md) | verificação independente | PASS/FAIL/NOT TESTED |
| [Release](release.md) | build, offline e licenças | pacote e relatório |

Fluxo recomendado: **Director → Architect → Gameplay + Visual + Audio → Profiler → Reviewer → Release**. A revisão pode devolver a tarefa a qualquer papel. Todos reportam paths, decisões, evidências e riscos, conforme [pipeline](../docs/01-pipeline.md).
