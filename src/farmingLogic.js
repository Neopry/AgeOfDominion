export function canPlantField(player, field, seedType) {
    // Kontrola, zda je pole připraveno
    if (!field.isCreated || !field.isTilled || !field.isFertilized) {
        return false;
    }

    // Kontrola, zda má hráč požadovaný druh semínka
    if (!player.inventory.hasItem(seedType)) {
        return false;
    }

    // Snížení výdrže hráče
    player.stamina -= 5;

    return true;
}

export function canHarvestField(player, field) {
    // Kontrola, zda je pole zralé ke sklizni
    if (!field.isMature) {
        return false;
    }

    // Kontrola, zda má hráč požadovaný nástroj
    if (!player.inventory.hasItem("kosa") && !player.inventory.hasItem("srp")) {
        return false;
    }

    return true;
}

export function npcCanPlantField(npc, field, seedType, storage) {
    // Kontrola, zda je pole připraveno
    if (!field.isCreated || !field.isTilled || !field.isFertilized) {
        return false;
    }

    // Kontrola, zda je ve skladu dostatek semínek
    if (!storage.hasItem(seedType)) {
        return false;
    }

    // NPC nevyužívá výdrž, ale může mít jiné omezení
    return true;
}

export function npcCanHarvestField(npc, field, storage) {
    // Kontrola, zda je pole zralé ke sklizni
    if (!field.isMature) {
        return false;
    }

    // Kontrola, zda je ve skladu dostupný nástroj
    if (!storage.hasItem("kosa") && !storage.hasItem("srp")) {
        return false;
    }

    return true;
}
