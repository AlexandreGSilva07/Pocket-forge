# Wave 01 — bytecode method inventory for 12 J2ME games

> These 12 JARs were verified by their complete SHA-256 and passed to javap for actual bytecode disassembly. **These mechanically obtained method inventories are not 12 fully understood/reconstructed engines.**

| # | JAR | Classes | Methods | Instructions | Branch instructions | Errors |
|---:|---|---:|---:|---:|---:|---:|
| 1 | \`3D Adventure\` (\`f2667dd8ee20\`) | 2 | 23 | 21665 | 461 | 0 |
| 2 | \`Doom RPG\` (\`6925de2ce810\`) | 23 | 342 | 35529 | 3041 | 0 |
| 3 | \`Geopod DC\` (\`595a04f90efc\`) | 12 | 176 | 19916 | 1050 | 0 |
| 4 | \`Prince Of Persia The Two Thrones\` (\`eb16778a12aa\`) | 6 | 255 | 33645 | 3722 | 0 |
| 5 | \`Mario MIDP2\` (\`16ede07fe858\`) | 16 | 109 | 17490 | 378 | 0 |
| 6 | \`Lemmings\` (\`41f07e9dc331\`) | 9 | 124 | 14794 | 940 | 0 |
| 7 | \`Xrossing Dice\` (\`8db1413d8135\`) | 25 | 205 | 5508 | 391 | 2 |
| 8 | \`Ancient Empires\` (\`2dda1c490d87\`) | 8 | 158 | 21682 | 1610 | 0 |
| 9 | \`World Fighting\` (\`d5d3da079ac3\`) | 13 | 173 | 12295 | 767 | 0 |
| 10 | \`C2S_Bowling2\` (\`f83ec4dc56cc\`) | 4 | 115 | 26871 | 1929 | 0 |
| 11 | \`colin mcrae rally 4\` (\`eb05f180891e\`) | 7 | 96 | 15666 | 1089 | 0 |
| 12 | \`7Zwerge\` (\`6df7ffc301a3\`) | 10 | 92 | 8311 | 676 | 0 |

## Evidence records

Each numbered JSON stores EVERY readable class and method signature, instruction count, branch count, top method-local call targets/opcodes, important methods, aggregated call references, and non-code resource names/sizes. No full source or bytecode text is published.
Game executability and visual behavior have NOT been verified here. Static methods may be dead code; calls don't imply hot paths.

## Next required work

Manual reconstruction of selected methods, original-game runtime tests, functional PocketForge implementations and measured benchmarks are separate stages.

## Validation

Source corpus SHA-256 is pinned in ../batches/registry.json; each record checks exact JAR SHA-256. Run via scripts/deep_bytecode_wave.py with the source ZIP on GitHub Actions.
