/**
 * Zkontroluje, zda se NPC může přidat do hráčova města.
 * @param {Object} npc - Objekt NPC.
 * @param {Object} playerTown - Objekt hráčova města.
 * @returns {boolean} True, pokud se NPC může přidat.
 */
function canNPCJoin(npc, playerTown) {
  if (!npc.joinable || !npc.joinable.canJoin) {
    return false;
  }

  // Příklad podmínky: Dostatek místa ve městě
  if (playerTown.capacity <= playerTown.currentPopulation) {
    return false;
  }

  // Další podmínky (např. splnění úkolu)
  if (npc.joinable.conditions && !checkPlayerConditions(npc.joinable.conditions)) {
    return false;
  }

  return true;
}

/**
 * Přidá NPC do hráčova města.
 * @param {Object} npc - Objekt NPC.
 * @param {Object} playerTown - Objekt hráčova města.
 * @returns {boolean} True, pokud bylo NPC úspěšně přidáno.
 */
function addNPCToPlayerTown(npc, playerTown) {
  if (canNPCJoin(npc, playerTown)) {
    playerTown.currentPopulation += 1;
    playerTown.residents.push(npc);
    console.log(`${npc.name || "NPC"} bylo přidáno do tvého města.`);
    return true;
  } else {
    console.log(`${npc.name || "NPC"} se nemůže přidat do tvého města.`);
    return false;
  }
}

/**
 * Zkontroluje podmínky hráče (např. splnění úkolů).
 * @param {string} conditions - Podmínky, které musí hráč splnit.
 * @returns {boolean} True, pokud jsou podmínky splněny.
 */
function checkPlayerConditions(conditions) {
  // Zde implementujte logiku pro kontrolu podmínek (např. splnění úkolů)
  console.log(`Kontrola podmínek: ${conditions}`);
  return true; // Příklad: vždy splněno
}

// Příklad použití:
const playerTown = {
  capacity: 10,
  currentPopulation: 5,
  residents: []
};

const npc = {
  name: "Jan Kovář",
  joinable: {
    canJoin: true,
    conditions: "Hráč musí mít dostatek místa ve městě.",
    dialog: "Rád bych se přidal do tvého města, pokud máš místo."
  }
};

if (addNPCToPlayerTown(npc, playerTown)) {
  console.log("NPC bylo úspěšně přidáno.");
} else {
  console.log("NPC se nemohlo přidat.");
}

module.exports = { canNPCJoin, addNPCToPlayerTown };
