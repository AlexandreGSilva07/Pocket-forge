# Estudo dirigido de bytecode — 3D Adventure

**JAR SHA-256:** `f2667dd8ee20f37d323d16a705ef9e26ed4e61f704af185e1dbb187cf7cf5761`

**Status:** `METHOD_REVIEW_PARTIAL` — métodos reais desmontados/interpretados, **não** jogo inteiro plenamente compreendido, portado ou executado. Ferramenta: OpenJDK 21 `javap -c -p` sobre binários originais enviados em conversa; recursos ZIP lidos sem executar MIDlets. Data: 15/10/2026.

### Evidência de bytecode real

- Original disponível entre os JARs enviados na conversa; SHA-256 calculado sobre os bytes originais: `f2667dd8ee20f37d323d16a705ef9e26ed4e61f704af185e1dbb187cf7cf5761`.
- `adventure/a.class` e `adventure/MIDlet1.class`: **duas classes de jogo**; 47.261 bytes de classfiles (o JAR inteiro mede 20.363 bytes comprimidos). Isso é uma **medida de tamanho**, não memória efetiva de execução.
- Desmontagem com `javap -classpath 3D-Adventure.jar -c -p adventure.a` (não apenas leitura de símbolos): presença dos métodos `run()`, `paint(Graphics)`, `keyPressed(int)`, `keyReleased(int)`.
- `paint(Graphics)`: chamadas concretas `DirectGraphics.drawPixels(short[], boolean, int, int, int, int, int, int, int, int)`. O bytecode usa o tipo `short[][]` para buffers `a2` e constantes `444`/ `4444` nos formatos de pixels, e desenha em regiões pequenas.
- São representações diretas de buffers compactos do lado do Java ME. **Não está provado** que cada `drawPixels` realiza renderização 3D; o método também desenha elementos de interface/menus. A reconstrução do pipeline de geometria no `run()` permanece pendente.

### Consequência implementável

Criar testes de **pixel buffer 16-bit / blit parcial / imagem decodificada** em Canvas/WebGL, verificando fidelidade e consumo medido. Um `Uint16Array` reduz armazenamento temporário de pixel em CPU versus RGBA 32-bit, mas a conversão para tela pode anular a economia e precisa ser medida. Não impor RGB444 ao motor moderno sem benchmark.

### Evidência/limites

Estudo parcial de método de render real. Não houve execução do JAR original, nem prova de um motor 3D inteiro reconstruído. Não publicar código ou recursos originais; registrar apenas assinatura, estrutura e observações.

## Experimento funcional adicionado ao motor (Pixel Surface)

O módulo autoral `demo/engine/pixels.js` acrescenta framebuffer `Uint16Array` em RGBA4444 **definido pelo PocketForge**, desenho por pixel/linhas, clipping e conversão explícita para `ImageData` do Canvas 2D. A demonstração `demo/pixel-lab.html` gera uma cena estilizada original em resolução lógica 160×120 e mede FPS localmente; testes em `tests/pixel_engine.test.cjs` validam packing, bytes, clipping, rasterização e upload.

**Comparação ainda pendente:** menor armazenamento do buffer CPU não garante menor gasto final ou render mais rápido, pois `Canvas.putImageData` recebe RGBA8 (dobro dos bytes por pixel) e pode dominar o custo. A amostra J2ME evidencia *a técnica*, não superioridade no hardware atual.
