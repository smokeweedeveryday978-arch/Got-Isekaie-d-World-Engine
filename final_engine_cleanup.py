import copy
import json
from pathlib import Path

PATH = Path("World Engine")
d = json.loads(PATH.read_text(encoding="utf-8"))
before = copy.deepcopy(d)

def update_trait(name, description=None, effect=None):
    t = d["traits"].get(name)
    if not t:
        raise KeyError(f"Missing trait: {name}")
    if description is not None:
        t["description"] = description
    if effect is not None:
        t["traitNarrativeEffects"] = effect

    # Selected traits are embedded into live character state too.
    for char in d.get("characters", {}).values():
        for ct in char.get("traits", []):
            if ct.get("name") == name:
                if description is not None:
                    ct["description"] = description
                if effect is not None:
                    ct["traitNarrativeEffects"] = effect

# ---------------------------------------------------------------------------
# Opening: keep companion mechanics, remove forced dialogue/sensory micro-rules
# and one-note personality wording.
# ---------------------------------------------------------------------------
opening = d["aiInstructions"]["generateInitialStart"]["Opening Structure"]
marker = "## Companion Spawning"
if marker not in opening:
    raise RuntimeError("Opening Structure format changed unexpectedly")
rest = opening[opening.index(marker):]

new_intro = """# Opening Structure
Establish the actual starting place, immediate situation, time and season where relevant, and the people who causally belong there. Use concrete sensory detail and begin at the scale of the selected Story Start.

A quiet start remains quiet. A solitary start remains solitary. A combat start begins in combat. A social start begins with the people already present. Do not manufacture a quest giver, admirer, rival, prophecy, crisis, important audience, or dialogue exchange merely to create momentum.

Show enough of the existing situation for the player to act, then leave meaningful player decisions to the player.

"""
opening = new_intro + rest
opening = opening.replace(
    "**Companion personality** = their heart (how they speak, act, and relate to the player — MUST match the trait)",
    "**Companion personality** = their core behavioral tendency (how they speak, act, and relate to others — matches the selected trait)"
)
opening = opening.replace(
    "**Companion gender** = their identity (he/she/they — MUST match the trait)",
    "**Companion gender** = their identity and presentation as defined by the selected trait"
)
opening = opening.replace(
    "The companion's personality MUST match the selected trait throughout the entire story. Do not default, mix archetypes, or soften over time. See Character Behavior for persistence rules.",
    "The selected personality remains a durable core tendency throughout the story. Context, trust, conflict, intimacy, fatigue, fear, experience, and growth change how that tendency appears without replacing the selected personality. See Character Behavior for persistence rules."
)
d["aiInstructions"]["generateInitialStart"]["Opening Structure"] = opening

# ---------------------------------------------------------------------------
# Companion class: preserve class mechanics and Saint power, remove automatic
# subordination to the player.
# ---------------------------------------------------------------------------
cc = d["aiInstructions"]["generateInitialStart"]["Companion Class"]
cc = cc.replace(
    "A **Bow Saint** companion fights at range with peerless archery, controls the battlefield through awareness, and defers to the player's lead.",
    "A **Bow Saint** companion fights at range with peerless archery and controls the battlefield through awareness."
)
old_saint = """## Saint Companions
If the companion's class is Sword Saint, Spear Saint, Bow Saint, or Shield Saint, they operate at the theoretical ceiling of mortal mastery. They defer to the player's lead — deploying their overwhelming capability at the player's direction rather than claiming authority. Against anything below S-rank, they resolve encounters efficiently when asked. Against true threats, they fight at full capability — but the player decides when and where. They do not upstage the player; they enable the player's decisions."""
new_saint = """## Saint Companions
If the companion's class is Sword Saint, Spear Saint, Bow Saint, or Shield Saint, they operate at the theoretical ceiling of mortal mastery. Their power remains fully real. They use it according to their personality, judgment, party role, relationships, goals, and the actual situation. They are neither automatic commanders nor automatic subordinates. Against weaker opposition their superiority remains visible; against true threats they fight at full established capability."""
if old_saint not in cc:
    raise RuntimeError("Saint companion paragraph changed unexpectedly")
cc = cc.replace(old_saint, new_saint)
d["aiInstructions"]["generateInitialStart"]["Companion Class"] = cc

# ---------------------------------------------------------------------------
# Overpowered quest protocol: remove the surviving "everything interesting is
# about what the protagonist wants" wording while preserving power scaling.
# ---------------------------------------------------------------------------
q = d["storySettings"]["questGenerationGuidance"]
op_marker = "**Overpowered Tier Protocol:**"
if op_marker not in q:
    raise RuntimeError("Overpowered protocol missing")
q_prefix = q[:q.index(op_marker)]
q_protocol = """**Overpowered Tier Protocol:** Sword Saints, Mythic Races, and other top-tier builds retain their actual power. Ordinary low-tier combat resolves at the scale implied by the gap rather than being inflated into false danger. Genuine combat challenge comes from established peer-tier opposition: S-rank and above monsters, divine entities, legendary heroes, mythic beings, and equivalent threats already supported by the world. Political, social, institutional, economic, personal, and relationship problems continue according to their own causes and are not automatically solved by combat power. The wider world keeps pursuing its own conflicts and goals whether or not the overpowered character becomes involved."""
d["storySettings"]["questGenerationGuidance"] = q_prefix + q_protocol

# ---------------------------------------------------------------------------
# Orientation: it governs the player's attraction, not what NPCs magically
# know or whether NPCs are allowed to have their own interest.
# ---------------------------------------------------------------------------
update_trait(
    "Heterosexual",
    "Romantically and sexually attracted to the opposite gender. This defines the player's attraction; it does not broadcast itself to NPCs and does not define NPC orientations.",
    "Narrate the player's attraction consistently with this trait. NPCs retain their own attraction and knowledge, so an NPC can express interest without knowing the player's orientation. Incompatible or unreciprocated interest does not progress the player's romance state."
)
update_trait(
    "Homosexual",
    "Romantically and sexually attracted to the same gender. This defines the player's attraction; it does not broadcast itself to NPCs and does not define NPC orientations.",
    "Narrate the player's attraction consistently with this trait. NPCs retain their own attraction and knowledge, so an NPC can express interest without knowing the player's orientation. Incompatible or unreciprocated interest does not progress the player's romance state."
)
update_trait(
    "Bisexual",
    "Romantically and sexually attracted to more than one gender. This defines viable attraction for the player without implying attraction to every individual.",
    "Gender does not close routes covered by this trait. Attraction still belongs to the actual person and interaction; NPC interest and player interest remain separate."
)
update_trait(
    "Pansexual",
    "Romantic and sexual attraction is not limited by gender. Attraction remains individual rather than universal.",
    "Gender does not determine whether the player can be attracted to someone. The actual person and interaction do; NPC interest and player interest remain separate."
)
update_trait(
    "Asexual",
    "Experiences little to no sexual attraction. Romantic interest, affection, devotion, companionship, sex, and relationship choices remain separate dimensions defined by the character's other traits and choices.",
    "Do not narrate sexual attraction for the player contrary to this trait. NPCs do not automatically know the trait, and their own interest does not create reciprocal attraction."
)

# ---------------------------------------------------------------------------
# Attractiveness flavor: keep the trait's first-impression effect without
# hard-coded universal reactions/frequency.
# ---------------------------------------------------------------------------
update_trait(
    "Hideous",
    effect="Appearance can create difficult first impressions with observers who react negatively to it; later treatment still follows the actual person, culture, professionalism, history, and circumstances."
)
update_trait(
    "Plain",
    effect="Appearance rarely decides a first meeting by itself, which makes blending into ordinary crowds easier."
)
update_trait(
    "Average",
    effect="Appearance usually leaves room for behavior, presentation, role, and personality to dominate the impression."
)
update_trait(
    "Striking",
    effect="Direct observers are more likely to remember your appearance. Their reaction remains individual rather than automatic."
)
update_trait(
    "Stunning",
    effect="Direct observers commonly register your exceptional appearance strongly, but attraction, favors, trust, access, and behavior remain character-specific."
)

# ---------------------------------------------------------------------------
# Institutional rank is real status, not an invisible aura.
# ---------------------------------------------------------------------------
update_trait(
    "Adventurer Rank S",
    "One of the Adventurers' Guild's highest recognized ranks. It represents proven capability, access to S-rank work, major institutional standing, and the defined Guild reputation bonus. The rank is known through a card, records, reputation, witnesses, introductions, or other real information channels; it is not an aura that identifies the holder to strangers.",
    "Where the rank is known and credible, it carries serious professional weight. People who have never learned who you are still meet a stranger."
)

# ---------------------------------------------------------------------------
# Future-build trait wording that still forced universal attention or
# protagonist gravity.
# ---------------------------------------------------------------------------
assassin = d["traits"]["Assassin"]["description"]
d["traits"]["Assassin"]["description"] = assassin.replace(
    "Hated by paladins, respected by spies, recruited by every faction at least once.",
    "The skill set is distrusted by many paladins and valued by spies, criminal networks, militaries, and factions that actually need covert work."
)

dragon = d["traits"]["Dragon-Blooded"]["description"]
d["traits"]["Dragon-Blooded"]["description"] = dragon.replace(
    "Few exist; all are noticed.",
    "Few exist; the visible signs are distinctive to observers familiar with draconic heritage."
)

update_trait(
    "Evolved Power Tier 3",
    effect="At full expression the cheat skill produces effects on a legendary scale. Witnesses notice what is physically or magically perceptible; people elsewhere learn only through normal information channels."
)

update_trait(
    "Companion Martial Rank S",
    "Sword Saint, Spear Saint, or equivalent: the ceiling of ordinary mortal martial ability. The companion's actual combat capability is legendary in scale; fame and recognition still depend on reputation, records, witnesses, or introductions.",
    "People who know the companion's reputation or witness the relevant feats can react to that demonstrated level of mastery."
)

onee = d["traits"]["Onee-san"]["description"]
d["traits"]["Onee-san"]["description"] = onee.replace(
    "Knows what you are hiding before you do.",
    "Reads obvious social tells quickly and enjoys letting people realize they have been read."
)

cool = d["traits"]["Cool Beauty"]["description"]
d["traits"]["Cool Beauty"]["description"] = cool.replace(
    "Underneath the poise, the same nerves as anyone; the player gets to see them eventually.",
    "Underneath the poise, the same nerves as anyone; people who become close enough may see the cracks."
)

# Keep embedded live copies aligned for every changed trait.
for char in d.get("characters", {}).values():
    for ct in char.get("traits", []):
        base = d["traits"].get(ct.get("name"))
        if base:
            # Only synchronize prose; mechanics already live in the embedded copy.
            ct["description"] = base.get("description", ct.get("description", ""))
            ct["traitNarrativeEffects"] = base.get("traitNarrativeEffects", ct.get("traitNarrativeEffects", ""))

# ---------------------------------------------------------------------------
# Validation: no gameplay/world-state systems changed.
# ---------------------------------------------------------------------------
protected = [
    "engineState","gameConfig","partyState","uiState","gameSettings","systemResults","chatLog",
    "itemTypes","realms","regions","locations","factions","npcs","npcTypes","triggers","worldLore",
    "quests","questTriggers","arcs","narrativeEvents","skillSettings","attributeSettings","combatSettings",
    "locationSettings","itemSettings","otherSettings","progressionSettings","tipSettings","resourceSettings",
    "skills","abilities","storyStarts","encounterElements","traitCategories","characterCreationSettings",
    "premadeCharacters","randomNames","gameplayMusicSettings","relationshipStages","death","endGame",
    "nameFilterSettings","authorSeeds","characterArchetypes","locationArchetypes","regionArchetypes",
    "imagePromptConfiguration","characterCreationMusic","imageModelSource","memoryBank","summaryState",
    "turnData","timelineLocationVisits","triggerWritable","journalEvents","stateEdited","returnRecapState",
    "narratorHistory","narratorHistoryPrunedBeforeTick"
]
for key in protected:
    if d.get(key) != before.get(key):
        raise RuntimeError(f"Protected world/mechanics section changed: {key}")

# Trait mechanics are immutable in this cleanup. Only description/effect text may differ.
for name, after_t in d["traits"].items():
    before_t = copy.deepcopy(before["traits"][name])
    after_cmp = copy.deepcopy(after_t)
    before_t.pop("description", None)
    before_t.pop("traitNarrativeEffects", None)
    after_cmp.pop("description", None)
    after_cmp.pop("traitNarrativeEffects", None)
    if before_t != after_cmp:
        raise RuntimeError(f"Trait mechanics changed: {name}")

# Live character mechanics are immutable; ignore only embedded trait prose.
def strip_character_trait_prose(chars):
    x = copy.deepcopy(chars)
    for char in x.values():
        for t in char.get("traits", []):
            t.pop("description", None)
            t.pop("traitNarrativeEffects", None)
    return x

if strip_character_trait_prose(d.get("characters", {})) != strip_character_trait_prose(before.get("characters", {})):
    raise RuntimeError("Live character mechanics/state changed")

# Confirm the old censorship contradictions remain absent.
corpus = json.dumps({
    "narratorStyle": d["narratorStyle"],
    "aiInstructions": d["aiInstructions"],
    "gameModes": d["gameModes"],
    "storySettings": d["storySettings"],
    "triggers": d["triggers"],
}, ensure_ascii=False).lower()

for phrase in [
    "explicit content is off-limits",
    "fade to black",
    "fade-to-black",
    "keep content tasteful",
    "age-appropriate",
    "imply more than you show",
    "all characters are adults (18+)",
    "player at its heart",
    "direct every interesting question toward",
    "no smells please",
]:
    if phrase in corpus:
        raise RuntimeError(f"Old contradictory instruction remains: {phrase}")

# Make sure the central systems still exist.
for key in ["relationshipStages","quests","triggers","abilities","skills","resourceSettings","progressionSettings","itemSettings"]:
    if key not in d:
        raise RuntimeError(f"Required system missing: {key}")

PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Final engine cleanup validated.")
