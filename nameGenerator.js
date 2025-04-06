const firstNames = [
  "Jan", "Eliška", "Lukáš", "Anna", "Robert", "Sofie", "Vilém", "Emma",
  "Oliver", "Mia", "Jakub", "Isabela", "Benjamin", "Karolína", "Jindřich", "Amálie"
];

const lastNames = [
  "Novák", "Svoboda", "Dvořák", "Černý", "Procházka", "Kučera", "Veselý", "Horák",
  "Němec", "Pokorný", "Král", "Růžička", "Fiala", "Sedláček", "Kolář", "Urban"
];

const titles = ["Pan", "Paní", "Mistr", "Dr.", "Kapitán", "Profesor"];

/**
 * Generuje náhodné jméno kombinací křestního jména a příjmení.
 * @returns {string} Náhodně vygenerované jméno.
 */
function generateRandomName() {
  const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
  const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
  return `${firstName} ${lastName}`;
}

/**
 * Generuje náhodný titul.
 * @returns {string} Náhodně vygenerovaný titul.
 */
function generateRandomTitle() {
  return titles[Math.floor(Math.random() * titles.length)];
}

/**
 * Generuje celé jméno s volitelným titulem.
 * @param {boolean} includeTitle - Zda zahrnout titul.
 * @returns {string} Náhodně vygenerované jméno s volitelným titulem.
 */
function generateFullName(includeTitle = false) {
  const name = generateRandomName();
  if (includeTitle) {
    const title = generateRandomTitle();
    return `${title} ${name}`;
  }
  return name;
}

/**
 * Přiřadí náhodné jméno NPC, pokud má `generatedName: true`.
 * @param {Object} npc - Objekt NPC.
 */
function assignRandomNameToNPC(npc) {
  if (npc.generatedName) {
    npc.name = generateRandomName();
  }
}

// Příklad použití:
const npc = { generatedName: true };
assignRandomNameToNPC(npc);
console.log(`Přiřazené jméno: ${npc.name}`);
console.log(generateFullName(true)); // Výstup: "Pan Jan Novák"
console.log(generateFullName(false)); // Výstup: "Jan Novák"

// Export funkcí pro použití v jiných částech hry.
module.exports = { generateRandomName, assignRandomNameToNPC, generateFullName };
