/**
 * Upraví úroveň respektu NPC a aktualizuje jeho názor na hráče.
 * @param {Object} npc - Objekt NPC.
 * @param {number} amount - Hodnota, o kterou se má úroveň respektu změnit (kladná nebo záporná).
 */
function adjustRespectLevel(npc, amount) {
  if (npc.respectLevel !== undefined) {
    npc.respectLevel = Math.min(100, Math.max(0, npc.respectLevel + amount));
    updateOpinionAboutPlayer(npc);
  }
}

/**
 * Aktualizuje názor NPC na hráče na základě jeho úrovně respektu.
 * @param {Object} npc - Objekt NPC.
 */
function updateOpinionAboutPlayer(npc) {
  if (npc.respectLevel >= 80) {
    npc.opinion.aboutPlayer = "Jsi vynikající vůdce a důvěřuji tvým rozhodnutím.";
  } else if (npc.respectLevel >= 50) {
    npc.opinion.aboutPlayer = "Jsi schopný vůdce, ale je co zlepšovat.";
  } else {
    npc.opinion.aboutPlayer = "Nejsem spokojený s tvým vedením. Musíš se zlepšit.";
  }
}

// Příklad použití:
const npc = {
  respectLevel: 50,
  opinion: { aboutPlayer: "Jsi schopný vůdce." }
};
adjustRespectLevel(npc, 10); // Zvýší úroveň respektu o 10
console.log(`Nová úroveň respektu: ${npc.respectLevel}`); // Výstup: 60
console.log(`Aktualizovaný názor: ${npc.opinion.aboutPlayer}`); // Výstup: "Jsi schopný vůdce, ale je co zlepšovat."

module.exports = { adjustRespectLevel, updateOpinionAboutPlayer };
