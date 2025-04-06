// ...existing code...

async function interactWithNPC(npc) {
  console.log(`NPC (${npc.name}): ${npc.dialogs[0]}`);
}

// Example usage
const npc = {
  name: "John the Blacksmith",
  role: "blacksmith",
  dialogs: ["Hello, traveler! Need your sword sharpened?"]
};

interactWithNPC(npc);