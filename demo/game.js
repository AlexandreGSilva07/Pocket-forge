"use strict";
/* PocketForge / Lumen Shift — Canvas 2D, no dependencies. */
(() => {
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d", { alpha: false });
  if (!ctx) { document.getElementById("overlayDescription").textContent = "Canvas 2D indisponível neste navegador."; return; }
  const $ = id => document.getElementById(id);
  const overlay = $("centerOverlay"), title = $("overlayTitle"), description = $("overlayDescription");
  const primary = $("primaryButton"), dashButton = $("dash"), pauseButton = $("pause");
  const muteButton = $("mute"), scoreLabel = $("score"), energyLabel = $("energy");
  const bestLabel = $("best"), statusLabel = $("status"), cooldownLabel = $("cooldown");
  const reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const TAU = Math.PI * 2;
  const PF = window.PocketForgeCompact;
  const TilePack = window.PocketForgeTilePack;
  if (!PF) throw new Error("PocketForge compact renderer not loaded");
  const TILE = 48, tileAtlas = PF.createTileAtlas(document, TILE);
  let tileMap;
  const rand = (min, max) => min + Math.random() * (max - min);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const distance = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
  const store = window.PocketForgeState.createStore((() => {
    try { return window.localStorage; } catch (_) { return null; }
  })(), { namespace: "lumen-shift", version: 1 });
  store.migrateLegacyNumber("pocketforge-lumen-best", "best");
  const audioBus = window.PocketForgeAudio.createAudio(window, { maxVoices: 12 });
  let width = 800, height = 600, dpr = 1, last = 0, now = 0;
  let state = "menu", score = 0, lives = 3, elapsed = 0, spawnTimer = 0, orbTimer = 0;
  let invulnerable = 0, dashTime = 0, dashCooldown = 0, muted = false;
  let touch = null, best = 0, shake = 0;
  let stars = [], enemies = [], orbs = [], particles = [], keys = new Set();
  const player = { x: 0, y: 0, r: 16, vx: 0, vy: 0, angle: -Math.PI / 2 };
  best = store.readNumber("best", 0);
  bestLabel.textContent = String(Math.floor(best)).padStart(4, "0");

  function resize() {
    const rect = canvas.getBoundingClientRect();
    width = Math.max(300, rect.width); height = Math.max(300, rect.height);
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const generated = PF.createTileMap(Math.ceil(width / TILE) + 1, Math.ceil(height / TILE) + 1, (x, y) => {
      const variant = (x * 23 + y * 41 + x * y) % 17;
      return variant === 0 ? 2 : variant === 7 ? 3 : 1;
    });
    // Roundtrip through our versioned compact binary level format.
    const packed = TilePack.encodePFLevel({
      cols: generated.width, rows: generated.height,
      tileWidth: TILE, tileHeight: TILE, tiles: generated.tiles
    });
    const decoded = TilePack.decodePFLevel(packed);
    tileMap = { width: decoded.cols, height: decoded.rows, tiles: decoded.tiles };
    stars = Array.from({ length: Math.min(130, Math.floor(width * height / 5700)) }, () => ({
      x: rand(0, width), y: rand(0, height), size: rand(.5, 2.1), phase: rand(0, TAU)
    }));
    player.x = clamp(player.x || width / 2, 22, width - 22);
    player.y = clamp(player.y || height / 2, 105, height - 30);
  }
  window.addEventListener("resize", resize);
  resize();

  function unlockAudio() { if (!muted) audioBus.unlock(); }
  function beep(freq, dur = .13, kind = "sine", vol = .04) {
    audioBus.play(freq, dur, kind, vol);
  }
  function sparkle(x, y, color, count = 12, speed = 160) {
    const n = reducedMotion ? Math.min(4, count) : count;
    for (let i = 0; i < n; i++) {
      if (particles.length >= 200) particles.shift();
      const angle = rand(0, TAU), magnitude = rand(speed * .3, speed);
      particles.push({ x, y, vx: Math.cos(angle) * magnitude, vy: Math.sin(angle) * magnitude,
        life: rand(.22, .64), maxLife: .64, size: rand(1.5, 4.5), color });
    }
  }
  function spawnEnemy() {
    const edge = Math.floor(rand(0, 4));
    const x = edge === 0 ? -25 : edge === 1 ? width + 25 : rand(10, width - 10);
    const y = edge === 2 ? -25 : edge === 3 ? height + 25 : rand(100, height - 20);
    enemies.push({ x, y, r: rand(13, 21), speed: rand(45, 74) + Math.min(80, elapsed * 1.2),
      angle: rand(0, TAU), pulse: rand(0, TAU) });
  }
  function spawnOrb() {
    if (orbs.length >= 8) return;
    orbs.push({ x: rand(34, Math.max(35, width - 34)), y: rand(115, Math.max(116, height - 42)),
      r: 10, phase: rand(0, TAU) });
  }
  function setUI(next, heading, text, label) {
    state = next;
    overlay.classList.toggle("active", next !== "playing");
    overlay.setAttribute("aria-hidden", next === "playing" ? "true" : "false");
    if (heading) title.innerHTML = heading;
    if (text) description.textContent = text;
    if (label) primary.innerHTML = label + " <span>→</span>";
    dashButton.disabled = next !== "playing";
    pauseButton.textContent = next === "paused" ? "▶" : "Ⅱ";
    statusLabel.textContent = next === "playing" ? "EM JOGO" : next === "paused" ? "PAUSADO" : next === "defeat" ? "FIM DA PARTIDA" : "PRONTO PARA INICIAR";
  }
  function begin() {
    unlockAudio();
    player.x = width / 2; player.y = height / 2; player.vx = 0; player.vy = 0; player.angle = -Math.PI / 2;
    score = 0; lives = 3; elapsed = 0; spawnTimer = .9; orbTimer = 1.4;
    enemies = []; orbs = []; particles = []; touch = null;
    invulnerable = 1; dashTime = 0; dashCooldown = 0; shake = 0;
    setUI("playing"); beep(440, .1); beep(720, .18);
    primary.blur();
  }
  function lose() {
    if (score > best) {
      best = Math.floor(score);
      store.writeNumber("best", best);
    }
    beep(190, .44, "sawtooth", .045);
    setUI("defeat", "Fim da <em>jornada</em>", "Você alcançou " + Math.floor(score) + " pontos. Cada tentativa deixa seu reflexo mais rápido.", "TENTAR DE NOVO");
  }
  function togglePause() {
    if (state === "playing") setUI("paused", "Em <em>pausa</em>", "Seu progresso está seguro. Continue quando quiser.", "CONTINUAR");
    else if (state === "paused") setUI("playing");
  }
  function dash() {
    if (state !== "playing" || dashCooldown > 0) return;
    unlockAudio();
    dashCooldown = 2.8; dashTime = .24; invulnerable = Math.max(invulnerable, .30);
    if (Math.abs(player.vx) + Math.abs(player.vy) < 5) { player.vx = Math.cos(player.angle) * 340; player.vy = Math.sin(player.angle) * 340; }
    sparkle(player.x, player.y, "#65f8ff", 26, 230); beep(660, .16, "triangle", .06);
  }
  primary.addEventListener("click", () => state === "paused" ? togglePause() : begin());
  dashButton.addEventListener("click", e => { e.stopPropagation(); dash(); });
  pauseButton.addEventListener("click", togglePause);
  muteButton.addEventListener("click", () => {
    muted = !muted; audioBus.setMuted(muted); muteButton.textContent = muted ? "♩" : "♫";
    muteButton.setAttribute("aria-pressed", String(muted));
    if (!muted) { unlockAudio(); beep(580, .09); }
  });
  window.addEventListener("keydown", e => {
    const key = e.key.toLowerCase();
    if (["arrowup", "arrowdown", "arrowleft", "arrowright", " "].includes(key)) e.preventDefault();
    keys.add(key);
    if (e.repeat) return;
    if (key === " " && state === "playing") dash();
    if (key === "p" || key === "escape") togglePause();
    if (key === "m") muteButton.click();
    if (key === "enter" && state !== "playing") primary.click();
  });
  window.addEventListener("keyup", e => keys.delete(e.key.toLowerCase()));
  window.addEventListener("blur", () => { keys.clear(); touch = null; if (state === "playing") togglePause(); });
  canvas.addEventListener("pointerdown", e => {
    if (state !== "playing") return;
    unlockAudio();
    canvas.setPointerCapture(e.pointerId);
    touch = { id: e.pointerId, x: e.clientX - canvas.getBoundingClientRect().left, y: e.clientY - canvas.getBoundingClientRect().top };
  });
  canvas.addEventListener("pointermove", e => {
    if (!touch || touch.id !== e.pointerId) return;
    const box = canvas.getBoundingClientRect();
    touch.x = e.clientX - box.left; touch.y = e.clientY - box.top;
  });
  const releasePointer = e => { if (touch && touch.id === e.pointerId) touch = null; };
  canvas.addEventListener("pointerup", releasePointer);
  canvas.addEventListener("pointercancel", releasePointer);

  function update(dt) {
    elapsed += dt; score += dt * 5.5;
    invulnerable = Math.max(0, invulnerable - dt);
    dashCooldown = Math.max(0, dashCooldown - dt);
    dashTime = Math.max(0, dashTime - dt);
    shake = Math.max(0, shake - dt * 15);
    let x = 0, y = 0;
    if (keys.has("a") || keys.has("arrowleft")) x--;
    if (keys.has("d") || keys.has("arrowright")) x++;
    if (keys.has("w") || keys.has("arrowup")) y--;
    if (keys.has("s") || keys.has("arrowdown")) y++;
    if (touch) {
      const dx = touch.x - player.x, dy = touch.y - player.y, len = Math.hypot(dx, dy);
      if (len > 18) { x = dx / len; y = dy / len; } else { x = 0; y = 0; }
    }
    const len = Math.hypot(x, y);
    if (len > 0) { x /= len; y /= len; player.angle = Math.atan2(y, x); }
    if (dashTime > 0) {
      const vx = len ? x : Math.cos(player.angle), vy = len ? y : Math.sin(player.angle);
      player.vx = vx * 650; player.vy = vy * 650;
      if (Math.random() < .8) sparkle(player.x, player.y, "#62dbe6", 2, 60);
    } else {
      player.vx = x * 230; player.vy = y * 230;
    }
    player.x = clamp(player.x + player.vx * dt, 20, width - 20);
    player.y = clamp(player.y + player.vy * dt, 98, height - 22);
    spawnTimer -= dt; orbTimer -= dt;
    if (spawnTimer <= 0) { spawnEnemy(); spawnTimer = Math.max(.28, 1.35 - elapsed * .013); }
    if (orbTimer <= 0) { spawnOrb(); orbTimer = rand(1.7, 2.8); }
    for (let i = enemies.length - 1; i >= 0; i--) {
      const e = enemies[i], dir = Math.atan2(player.y - e.y, player.x - e.x);
      e.x += Math.cos(dir) * e.speed * dt; e.y += Math.sin(dir) * e.speed * dt;
      e.angle += dt; e.pulse += dt * 3;
      if (distance(e, player) < e.r + player.r) {
        if (dashTime > 0) {
          score += 35; sparkle(e.x, e.y, "#fc7bc2", 14, 210); enemies.splice(i, 1); beep(380, .09, "square", .024);
        } else if (invulnerable <= 0) {
          lives--; invulnerable = 1.4; shake = reducedMotion ? 0 : 8;
          sparkle(player.x, player.y, "#ff6da4", 22, 170); beep(180, .27, "sawtooth");
          if (lives <= 0) { lose(); break; }
        }
      }
    }
    for (let i = orbs.length - 1; i >= 0; i--) {
      const o = orbs[i]; o.phase += dt * 4;
      if (distance(o, player) < o.r + player.r + 4) {
        score += 60; sparkle(o.x, o.y, "#79f9e5", 17, 100); orbs.splice(i, 1); beep(960, .15);
      }
    }
    updateParticles(dt);
    const value = String(Math.floor(score)).padStart(4, "0");
    if (scoreLabel.textContent !== value) scoreLabel.textContent = value;
    energyLabel.textContent = "◆ ".repeat(lives).trim() || "—";
    bestLabel.textContent = String(Math.floor(best)).padStart(4, "0");
    dashButton.classList.toggle("cooling", dashCooldown > 0);
    cooldownLabel.style.transform = "rotate(" + (dashCooldown / 2.8 * 360) + "deg)";
    cooldownLabel.style.opacity = dashCooldown > 0 ? "1" : "0";
  }
  function updateParticles(dt) {
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i]; p.x += p.vx * dt; p.y += p.vy * dt; p.vx *= .97; p.vy *= .97;
      p.life -= dt; if (p.life <= 0) particles.splice(i, 1);
    }
  }
  function drawGrid() {
    ctx.save(); ctx.globalAlpha = .3;
    PF.drawTileMap(ctx, tileAtlas, tileMap, { size: TILE, viewWidth: width, viewHeight: height });
    ctx.restore();
    stars.forEach(s => {
      ctx.fillStyle = "rgba(163,217,255," + (.12 + Math.sin(now * 1.8 + s.phase) * .12) + ")";
      ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, TAU); ctx.fill();
    });
  }
  function glow(x, y, radius, color, alpha = .28) {
    const g = ctx.createRadialGradient(x, y, 0, x, y, radius);
    g.addColorStop(0, color); g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.globalAlpha = alpha; ctx.fillStyle = g; ctx.fillRect(x - radius, y - radius, radius * 2, radius * 2); ctx.globalAlpha = 1;
  }
  function draw() {
    ctx.fillStyle = "#080f20"; ctx.fillRect(0, 0, width, height);
    glow(width * .22, height * .68, Math.min(390, width * .5), "#157e9f", .2);
    glow(width * .8, height * .3, Math.min(390, width * .5), "#7048a9", .15);
    drawGrid();
    ctx.save();
    if (shake > 0) ctx.translate(rand(-shake, shake), rand(-shake, shake));
    orbs.forEach(o => {
      const rr = o.r + Math.sin(o.phase) * 2;
      glow(o.x, o.y, 31, "#3dfac5", .32);
      ctx.strokeStyle = "#62ffdc"; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(o.x, o.y, rr, 0, TAU); ctx.stroke();
      ctx.fillStyle = "#b4fff3"; ctx.beginPath(); ctx.arc(o.x, o.y, 4, 0, TAU); ctx.fill();
    });
    enemies.forEach(e => {
      glow(e.x, e.y, 45, "#df317d", .3);
      ctx.save(); ctx.translate(e.x, e.y); ctx.rotate(e.angle * .6);
      ctx.strokeStyle = "#ff85bd"; ctx.lineWidth = 2.2; ctx.fillStyle = "#521e49";
      ctx.beginPath();
      for (let j = 0; j < 6; j++) {
        const a = j * TAU / 6, r = e.r * (j % 2 ? .8 : 1.16);
        if (!j) ctx.moveTo(Math.cos(a) * r, Math.sin(a) * r);
        else ctx.lineTo(Math.cos(a) * r, Math.sin(a) * r);
      }
      ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
    });
    if (state !== "menu" && (invulnerable <= 0 || Math.floor(now * 10) % 2 === 0)) {
      glow(player.x, player.y, dashTime > 0 ? 85 : 53, "#28e6ef", dashTime > 0 ? .55 : .33);
      ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(player.angle + Math.PI / 2);
      ctx.shadowBlur = reducedMotion ? 0 : 12; ctx.shadowColor = "#5cffef";
      ctx.beginPath(); ctx.moveTo(0, -20); ctx.lineTo(13, 13); ctx.lineTo(0, 7); ctx.lineTo(-13, 13);
      ctx.closePath(); ctx.fillStyle = "#58e9eb"; ctx.fill();
      ctx.strokeStyle = "#d7ffff"; ctx.lineWidth = 1.4; ctx.stroke(); ctx.restore();
    }
    particles.forEach(p => {
      ctx.globalAlpha = clamp(p.life / p.maxLife, 0, 1);
      ctx.fillStyle = p.color; ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
    });
    ctx.globalAlpha = 1; ctx.restore();
  }
  function frame(timestamp) {
    const dt = last ? clamp((timestamp - last) / 1000, 0, .05) : 0;
    last = timestamp;
    if (state !== "paused") now += dt;
    if (state === "playing") update(dt);
    else if (state !== "paused") updateParticles(dt);
    draw();
    requestAnimationFrame(frame);
  }
  setUI("menu", "Lumen <em>Shift</em>", "Atravesse uma arena luminosa. Colete energia, evite os perseguidores e use o impulso para abrir caminho.", "COMEÇAR");
  requestAnimationFrame(frame);
})();
