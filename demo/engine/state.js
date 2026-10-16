/* PocketForge State Core v0.2 — small versioned persistent snapshots.
 * Original implementation informed by widespread J2ME RMS usage.
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.PocketForgeState = api;
})(typeof window !== "undefined" ? window : (typeof globalThis !== "undefined" ? globalThis : null), function () {
  "use strict";
  const NAME = /^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$/;
  function assertName(value, label) {
    if (typeof value !== "string" || !NAME.test(value)) throw new TypeError("invalid " + label);
    return value;
  }
  function createStore(storage, { namespace = "pocketforge", version = 1, maxBytes = 65536 } = {}) {
    assertName(namespace, "namespace");
    if (!Number.isInteger(version) || version < 1 || version > 65535) throw new RangeError("invalid schema version");
    if (!Number.isInteger(maxBytes) || maxBytes < 128 || maxBytes > 1048576) throw new RangeError("invalid size budget");
    const prefix = namespace + ":v" + version + ":";
    const fallback = new Map(); // session-only fallback when storage is blocked
    function identifier(key) { return prefix + assertName(key, "record name"); }
    function load(key) {
      const id = identifier(key);
      if (fallback.has(id)) return fallback.get(id);
      try { return storage ? storage.getItem(id) : null; } catch (_) { return null; }
    }
    function persist(key, value) {
      const id = identifier(key);
      const encoded = JSON.stringify({ schema: version, data: value });
      if (encoded.length > maxBytes) throw new RangeError("snapshot exceeds size budget");
      try {
        if (!storage) throw new Error("storage unavailable");
        storage.setItem(id, encoded);
        fallback.delete(id);
        return true;
      } catch (_) {
        fallback.set(id, encoded);
        return false; // fallback is usable this session, not durable
      }
    }
    function read(key, defaultValue = null) {
      const encoded = load(key);
      if (encoded == null) return defaultValue;
      try {
        const snapshot = JSON.parse(encoded);
        if (!snapshot || snapshot.schema !== version || !Object.prototype.hasOwnProperty.call(snapshot, "data"))
          return defaultValue;
        return snapshot.data;
      } catch (_) { return defaultValue; }
    }
    function readNumber(key, defaultValue = 0) {
      const value = read(key, defaultValue);
      return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : defaultValue;
    }
    function writeNumber(key, value) {
      if (typeof value !== "number" || !Number.isFinite(value) || value < 0) throw new RangeError("invalid record number");
      return persist(key, value);
    }
    function readJSON(key, defaultValue = null) { return read(key, defaultValue); }
    function writeJSON(key, value) {
      if (value == null || typeof value !== "object") throw new TypeError("object or array required");
      return persist(key, value);
    }
    // One-way, non-destructive migration from a raw numerical localStorage key.
    function migrateLegacyNumber(oldKey, newKey) {
      assertName(oldKey, "legacy key");
      if (load(newKey) !== null) return false;
      try {
        const raw = storage && storage.getItem(oldKey);
        if (raw == null || raw.trim() === "") return false;
        const n = Number(raw);
        if (!Number.isFinite(n) || n < 0) return false;
        writeNumber(newKey, n);
        return true;
      } catch (_) { return false; }
    }
    return Object.freeze({ prefix, readNumber, writeNumber, readJSON, writeJSON, migrateLegacyNumber });
  }
  return Object.freeze({ createStore });
});
