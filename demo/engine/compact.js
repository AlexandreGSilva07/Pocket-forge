/* PocketForge Compact Rendering Core v0.2
 * Original implementation informed by J2ME corpus research.
 * Canvas 2D region atlas + RLE tilemaps. No J2ME code or assets reused.
 */
(function (root, make) {
  "use strict";
  const api = make();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.PocketForgeCompact = api;
})(typeof window !== "undefined" ? window : (typeof globalThis !== "undefined" ? globalThis : null), function () {
  "use strict";
  function dimension(n, name) {
    if (!Number.isSafeInteger(n) || n <= 0 || n > 16384) throw new RangeError(name + " must be 1..16384");
    return n;
  }
  function byte(n) {
    if (!Number.isInteger(n) || n < 0 || n > 255) throw new RangeError("tile id must be 0..255");
    return n;
  }
  function encodeRLE(tiles) {
    if (!tiles || typeof tiles.length !== "number") throw new TypeError("tiles array required");
    const out = [];
    for (let i = 0; i < tiles.length;) {
      const tile = byte(tiles[i]);
      let count = 1;
      while (i + count < tiles.length && tiles[i + count] === tile && count < 255) count++;
      out.push(count, tile);
      i += count;
    }
    return Uint8Array.from(out);
  }
  function decodeRLE(encoded, expectedLength) {
    if (!encoded || encoded.length % 2) throw new RangeError("RLE requires count/tile pairs");
    if (!Number.isSafeInteger(expectedLength) || expectedLength < 0 || expectedLength > 16777216)
      throw new RangeError("invalid decoded length");
    const out = new Uint8Array(expectedLength);
    let cursor = 0;
    for (let i = 0; i < encoded.length; i += 2) {
      const count = byte(encoded[i]), id = byte(encoded[i + 1]);
      if (!count || cursor + count > expectedLength) throw new RangeError("RLE count out of bounds");
      out.fill(id, cursor, cursor + count);
      cursor += count;
    }
    if (cursor !== expectedLength) throw new RangeError("RLE length mismatch");
    return out;
  }
  function createTileMap(width, height, fn) {
    dimension(width, "width"); dimension(height, "height");
    if (width * height > 16777216) throw new RangeError("tilemap exceeds safety budget");
    if (typeof fn !== "function") throw new TypeError("generator required");
    const tiles = new Uint8Array(width * height);
    for (let y = 0; y < height; y++) for (let x = 0; x < width; x++)
      tiles[y * width + x] = byte(fn(x, y));
    return { width, height, tiles };
  }
  // Atlas is a horizontal strip: tile 0 is transparent, tile IDs 1..N address regions.
  function drawTileMap(ctx, atlas, map, options) {
    if (!ctx || typeof ctx.drawImage !== "function") throw new TypeError("Canvas context required");
    if (!map || !map.tiles || map.tiles.length !== map.width * map.height) throw new TypeError("invalid tilemap");
    const o = options || {}, size = dimension(o.size || 48, "tile size");
    const cameraX = Number(o.cameraX || 0), cameraY = Number(o.cameraY || 0);
    const viewWidth = Math.max(0, Number(o.viewWidth || map.width * size));
    const viewHeight = Math.max(0, Number(o.viewHeight || map.height * size));
    if (![cameraX,cameraY,viewWidth,viewHeight].every(Number.isFinite))
      throw new RangeError("invalid camera or viewport");
    const firstX = Math.max(0, Math.floor(cameraX / size));
    const firstY = Math.max(0, Math.floor(cameraY / size));
    const lastX = Math.min(map.width, Math.ceil((cameraX + viewWidth) / size));
    const lastY = Math.min(map.height, Math.ceil((cameraY + viewHeight) / size));
    let draws = 0;
    for (let y = firstY; y < lastY; y++) {
      for (let x = firstX; x < lastX; x++) {
        const id = map.tiles[y * map.width + x];
        if (!id) continue;
        if (atlas.width && (id + 1) * size > atlas.width) throw new RangeError("tile outside atlas");
        ctx.drawImage(atlas, id * size, 0, size, size, x * size - cameraX, y * size - cameraY, size, size);
        draws++;
      }
    }
    return draws;
  }
  function createTileAtlas(doc, size = 48) {
    dimension(size, "size");
    const canvas = doc.createElement("canvas");
    canvas.width = size * 4; canvas.height = size;
    const c = canvas.getContext("2d");
    if (!c) throw new Error("Canvas 2D unavailable");
    // Tile 0 transparent; tiles 1–3 subtle, generated and packed into one texture.
    c.lineWidth = 1;
    c.strokeStyle = "rgba(90,160,210,.32)";
    c.fillStyle = "rgba(132,206,250,.55)";
    for (let n = 1; n < 4; n++) {
      const x = n * size;
      if (n === 1) {
        c.beginPath(); c.moveTo(x, 0); c.lineTo(x + size, 0);
        c.moveTo(x, 0); c.lineTo(x, size); c.stroke();
      } else if (n === 2) {
        c.beginPath(); c.arc(x + size / 2, size / 2, Math.max(1, size / 40), 0, Math.PI * 2); c.fill();
        c.beginPath(); c.moveTo(x + size / 2, size / 2 - 8);
        c.lineTo(x + size / 2, size / 2 + 8);
        c.moveTo(x + size / 2 - 8, size / 2);
        c.lineTo(x + size / 2 + 8, size / 2); c.stroke();
      } else {
        c.beginPath();
        c.arc(x + size / 2, size / 2, size / 4, 0, Math.PI * 2); c.stroke();
      }
    }
    return canvas;
  }
  return Object.freeze({ encodeRLE, decodeRLE, createTileMap, drawTileMap, createTileAtlas });
});
