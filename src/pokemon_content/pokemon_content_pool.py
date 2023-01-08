from dataclasses import dataclass, field
import random
from pokemon_content.pokemon_elements import PokemonElements

from mechanics.element import Element


@dataclass
class Detail:
    relation: str
    detail: str
    quantifier: str | None = None

    def text(self, adjective: str = None):
        quantifier = f"{self.quantifier} " if self.quantifier else ""
        if adjective:
            return f"{self.relation} {quantifier}{adjective} {self.detail}"
        return f"{self.relation} {quantifier}{self.detail}"

    def __hash__(self) -> int:
        return hash(self.detail)


@dataclass
class CreatuteType:
    name: str
    details: list[Detail] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.name)


HOLDABLE_WEAPONS = []


def with_holdable_weapon(detail: str, quantifier: str = None) -> Detail:
    detail = Detail(relation="holding", detail=detail, quantifier=quantifier)
    HOLDABLE_WEAPONS.append(detail)
    return detail


def with_detail(detail: str, quantifier: str = None) -> Detail:
    return Detail(relation="with", detail=detail, quantifier=quantifier)


def wearing_detail(detail: str, quantifier: str = None) -> Detail:
    return Detail(relation="wearing", detail=detail, quantifier=quantifier)


HOLD_SWORD = with_holdable_weapon("sword", "a")
HOLD_BOW = with_holdable_weapon("bow", "a")
HOLD_STAFF = with_holdable_weapon("staff", "a")
HOLD_SHIELD = with_holdable_weapon("shield", "a")
HOLD_AXE = with_holdable_weapon("axe", "an")
HOLD_DAGGER = with_holdable_weapon("dagger", "a")
HOLD_SPEAR = with_holdable_weapon("spear", "a")
HOLD_MACE = with_holdable_weapon("mace", "a")
HOLD_HAMMER = with_holdable_weapon("hammer", "a")
HOLD_CLUB = with_holdable_weapon("club", "a")
HOLD_LANCE = with_holdable_weapon("lance", "a")
HOLD_WHIP = with_holdable_weapon("whip", "a")
HOLD_GLAIVE = with_holdable_weapon("glaive", "a")

# WITH_EYES = with_detail("eyes")
WITH_CLAWS = with_detail("claws")
WITH_TAIL = with_detail("tail", "a")
WITH_HORNS = with_detail("horns")
WITH_HOOVES = with_detail("hooves")
WITH_TUSKS = with_detail("tusks")
WITH_FUR = with_detail("fur")
WITH_SKIN = with_detail("skin")
WITH_ANTLERS = with_detail("antlers")
WITH_SCALES = with_detail("scales")
WITH_SHELL = with_detail("shell")
WITH_CRYSTAL_CORE = with_detail("crystal core", "a")
WITH_HALO = with_detail("halo", "a")
WITH_WINGS = with_detail("wings")
WITH_FINS = with_detail("fins")
WITH_TENTACLES = with_detail("tentacles")
WITH_FEATHERS = with_detail("feathers")
WITH_TALONS = with_detail("talons")
WITH_BEAK = with_detail("beak", "a")
WITH_CARAPACE = with_detail("carapace", "")
WITH_TEXTURE = with_detail("texture")


WEARING_ARMOR = wearing_detail("armor")
WEARING_BRACERS = wearing_detail("bracers")
WEARING_GEMS = wearing_detail("gemstones")
BODY_WEARABLES = [WEARING_ARMOR, WEARING_BRACERS, WEARING_GEMS]

WEARING_MASK = wearing_detail("mask", "a")
WEARING_CROWN = wearing_detail("crown", "a")
WEARING_CRYSTAL_HEADBAND = wearing_detail("crystal headband", "a")
HEAD_WEARABLES = [WEARING_MASK, WEARING_CROWN, WEARING_CRYSTAL_HEADBAND]

ALL_WEARABLES = [*BODY_WEARABLES, *HEAD_WEARABLES]
LIZARD_DETAILS = [WITH_TAIL, WITH_SCALES, *ALL_WEARABLES, *HOLDABLE_WEAPONS]
NO_HAND_REPTILE_DETAILS = [WITH_TAIL, WITH_SCALES, *ALL_WEARABLES]


WOLF = CreatuteType("wolf", [WITH_TAIL, WITH_CLAWS, WITH_FUR, *ALL_WEARABLES])
BEAR = CreatuteType("bear", [WITH_CLAWS, WITH_FUR, *ALL_WEARABLES])
MONKEY = CreatuteType(
    "monkey", [WITH_TAIL, WITH_FUR, *ALL_WEARABLES, *HOLDABLE_WEAPONS]
)
GORILLA = CreatuteType(
    "gorilla", [WITH_TAIL, WITH_FUR, *ALL_WEARABLES, *HOLDABLE_WEAPONS]
)

BULL = CreatuteType("bull", [WITH_HORNS, WITH_HOOVES, WITH_SKIN, *ALL_WEARABLES])
BISON = CreatuteType("bison", [WITH_HORNS, WITH_HOOVES, WITH_SKIN, *ALL_WEARABLES])
ELEPHANT = CreatuteType(
    "elephant", [WITH_HOOVES, WITH_TUSKS, WITH_SKIN, *ALL_WEARABLES]
)
BOAR = CreatuteType("boar", [WITH_HOOVES, WITH_TUSKS, WITH_SKIN, *ALL_WEARABLES])
TIGER = CreatuteType("tiger", [WITH_CLAWS, WITH_FUR, *ALL_WEARABLES])
LYNX = CreatuteType("lynx", [WITH_CLAWS, WITH_FUR, *ALL_WEARABLES])
LION = CreatuteType("lion", [WITH_CLAWS, WITH_FUR, *ALL_WEARABLES])
RABBIT = CreatuteType("rabbit", [WITH_FUR, *ALL_WEARABLES, *HOLDABLE_WEAPONS])
FOX = CreatuteType("fox", [WITH_TAIL, WITH_FUR, *ALL_WEARABLES])
DEER = CreatuteType("deer", [WITH_HOOVES, WITH_ANTLERS, *ALL_WEARABLES])
IBEX = CreatuteType("ibex", [WITH_HOOVES, WITH_ANTLERS, *ALL_WEARABLES])
GOAT = CreatuteType("goat", [WITH_HOOVES, WITH_ANTLERS, *ALL_WEARABLES])
HORSE = CreatuteType("horse", [WITH_HOOVES, *ALL_WEARABLES])
CAT = CreatuteType("cat", [WITH_CLAWS, WITH_FUR, *ALL_WEARABLES])


LAND_MAMMALS = [
    WOLF,
    BEAR,
    MONKEY,
    GORILLA,
    BULL,
    BISON,
    ELEPHANT,
    BOAR,
    TIGER,
    LYNX,
    LION,
    RABBIT,
    FOX,
    DEER,
    IBEX,
    GOAT,
    HORSE,
    CAT,
]

REPTILE = CreatuteType("reptile", [WITH_TAIL, WITH_SKIN, *ALL_WEARABLES])
CLAM = CreatuteType(
    "clam",
    [WITH_SHELL, WITH_CRYSTAL_CORE],
)
PENGUIN = CreatuteType(
    "penguin", [WITH_TAIL, WITH_FUR, *ALL_WEARABLES, *HOLDABLE_WEAPONS]
)
ORCA = CreatuteType("orca", [WITH_TAIL, WITH_SKIN, WEARING_ARMOR])
SHARK = CreatuteType("shark", [WITH_TAIL, WITH_FINS, WEARING_ARMOR])
SQUID = CreatuteType(
    "squid",
    [WITH_CRYSTAL_CORE, WITH_TENTACLES],
)
CRUSTACEAN = CreatuteType(
    "crustacean",
    [WITH_CLAWS, WITH_SHELL, WEARING_ARMOR, WITH_CRYSTAL_CORE, WITH_CARAPACE],
)
TORTOISE = CreatuteType(
    "tortoise", [WITH_TAIL, WITH_SHELL, WITH_CARAPACE, *ALL_WEARABLES]
)
SEA_HORSE = CreatuteType("sea-horse", [WITH_TAIL, WITH_SHELL, *ALL_WEARABLES])
SEA_SNAKE = CreatuteType(
    "sea-snake", [WITH_TAIL, WITH_SCALES, WEARING_ARMOR, *HEAD_WEARABLES]
)
FISH = CreatuteType("fish", [WITH_TAIL, WITH_SCALES, WEARING_ARMOR])
OCTOPUS = CreatuteType("octopus", [WITH_TENTACLES, WEARING_ARMOR])
DRAGON = CreatuteType("dragon", [*LIZARD_DETAILS, WITH_CRYSTAL_CORE])
SERPENT = CreatuteType("serpent", [*NO_HAND_REPTILE_DETAILS])
CROCODILE = CreatuteType("crocodile", [*NO_HAND_REPTILE_DETAILS])

BIRD_DETAILS = [WITH_TAIL, WITH_FEATHERS, WITH_BEAK, *ALL_WEARABLES]
SWAN = CreatuteType("swan", [*BIRD_DETAILS])

MARINE_CREATUTES = [
    REPTILE,
    CLAM,
    PENGUIN,
    SHARK,
    SQUID,
    CRUSTACEAN,
    TORTOISE,
    SEA_HORSE,
    FISH,
    OCTOPUS,
    SERPENT,
    CROCODILE,
    SWAN,
]

BIRD = CreatuteType("bird", [*BIRD_DETAILS])
PARROT = CreatuteType("parrot", [*BIRD_DETAILS])
OWL = CreatuteType("owl", [*BIRD_DETAILS])
EAGLE = CreatuteType("eagle", [*BIRD_DETAILS])
HAWK = CreatuteType("hawk", [*BIRD_DETAILS])
FALCON = CreatuteType("falcon", [*BIRD_DETAILS])
CROW = CreatuteType("crow", [*BIRD_DETAILS])
OSTRICH = CreatuteType("ostrich", [*BIRD_DETAILS])

BIRDS = [BIRD, PARROT, OWL, EAGLE, HAWK, FALCON, CROW, OSTRICH, SWAN]

DRAGON = CreatuteType("dragon", [*LIZARD_DETAILS, WITH_CRYSTAL_CORE])
LIZARD = CreatuteType("lizard", [*LIZARD_DETAILS])
CHAMELEON = CreatuteType("chameleon", [*LIZARD_DETAILS])
FRILLED_LIZARD = CreatuteType("frilled-lizard", [*NO_HAND_REPTILE_DETAILS])
GECKO = CreatuteType("gecko", [*LIZARD_DETAILS])

REPTILES = [DRAGON, LIZARD, CHAMELEON, FRILLED_LIZARD, SERPENT, GECKO]

INSECT_DETAILS = [WITH_CRYSTAL_CORE, WITH_WINGS]

BUTTERFLY = CreatuteType("butterfly", [*INSECT_DETAILS])
MANTIS = CreatuteType("mantis", [*INSECT_DETAILS])
BEETLE = CreatuteType("beetle", [*INSECT_DETAILS])
LADYBUG = CreatuteType("ladybug", [*INSECT_DETAILS])
DRAGONFLY = CreatuteType("dragonfly", [*INSECT_DETAILS])
SPIDER = CreatuteType("spider", [*INSECT_DETAILS])
SCORPION = CreatuteType("scorpion", [*INSECT_DETAILS])

INSECTS = [
    MANTIS,
    BEETLE,
    LADYBUG,
    DRAGONFLY,
    SPIDER,
]

ABSTRACT_DETAILS = [WITH_CRYSTAL_CORE, WITH_TEXTURE]
PUMPKIN = CreatuteType("pumpkin", [WITH_SKIN, WITH_CRYSTAL_CORE])
GHOST = CreatuteType("ghost", [WITH_SKIN, WITH_CRYSTAL_CORE])
TREANT = CreatuteType("treant", [WITH_SKIN, WITH_CRYSTAL_CORE])
GOLEM = CreatuteType("golem", [*HOLDABLE_WEAPONS, WITH_CRYSTAL_CORE, *ALL_WEARABLES])
ABSTRACT_TYPES = [PUMPKIN, GHOST, TREANT, GOLEM]

CREATURES_BY_ELEMENT = {
    PokemonElements.NEUTRAL: set(BIRDS + LAND_MAMMALS),
    PokemonElements.FIRE: set(LAND_MAMMALS + REPTILES),
    PokemonElements.WATER: set(MARINE_CREATUTES + REPTILES),
    PokemonElements.GRASS: set(INSECTS + REPTILES + LAND_MAMMALS),
    PokemonElements.ELECTRIC: set(LAND_MAMMALS + REPTILES + BIRDS),
    PokemonElements.PSYCHIC: set(INSECTS + LAND_MAMMALS + REPTILES + BIRDS),
}

ENVIRONMENTS_BY_ELEMENT = {
    PokemonElements.NEUTRAL: ["village", "field", "grassland"],
    PokemonElements.FIRE: ["volcano", "desert"],
    PokemonElements.WATER: ["ocean", "lake", "river"],
    PokemonElements.GRASS: ["forest", "jungle", "woods"],
    PokemonElements.ELECTRIC: ["mountain", "city", "thunderstorm"],
    PokemonElements.PSYCHIC: ["castle", "cave", "crypt"],
}
GLOBAL_DETAIL_ADJECTIVES = [
    "white",
    "dark",
    "golden",
    "regal",
    "ornate",
    "ancient",
]

DETAIL_ADJECTIVES_BY_ELEMENT = {
    PokemonElements.NEUTRAL: ["white", "shiny", "prismatic", "opal", "diamond"],
    PokemonElements.FIRE: ["red and white", "orange and black", "fiery", "ruby"],
    PokemonElements.WATER: [
        "blue and white",
        "white and black",
        "teal and navy",
        "blue crystal",
        "cyan glittering",
        "sapphire",
    ],
    PokemonElements.GRASS: [
        "green and brown",
        "white and green",
        "stone",
        "wooden",
        "leafy",
        "green runic",
    ],
    PokemonElements.ELECTRIC: [
        "yellow and teal",
        "yellow and black",
        "golden",
        "lightning-charged",
    ],
    PokemonElements.PSYCHIC: [
        "amethyst",
        "purple cosmic",
        "galaxy-pattern",
        "violet hypnotic",
    ],
}

AMBIENCE_BY_ELEMENT = {
    PokemonElements.NEUTRAL: [
        "pastel colors",
        "bright lighting",
        "soft ambient light",
        "faded prismatic bokeh background",
        "silver galaxy background",
    ],
    PokemonElements.FIRE: [
        "red and purple ambient lighting",
        "blue and red ambient lighting",
        "lava texture background",
        "orange galaxy background",
    ],
    PokemonElements.WATER: [
        "teal and blue ambient lighting",
        "aurora background",
        "sparkling blue background",
        "gleaming bubble background",
        "sapphire blue galaxy background",
    ],
    PokemonElements.GRASS: [
        "green and orange ambient lighting",
        "green and teal ambient lighting",
        "emerald bokeh lighting",
        "sunlight ray ambience",
        "emerald galaxy background",
    ],
    PokemonElements.ELECTRIC: [
        "yellow and teal ambient lighting",
        "lightning background",
        "orange galaxy background",
    ],
    PokemonElements.PSYCHIC: [
        "pink bokeh lighting",
        "violet shadows",
        "dreamy background",
        "galaxy background",
    ],
}

ALL_SUBJECTS = [*LAND_MAMMALS, *MARINE_CREATUTES, *REPTILES, *INSECTS, *BIRDS]
ALL_SUBJECTS_BY_NAME = {subject.name: subject for subject in ALL_SUBJECTS}


def get_rarity_adjectives_set(rarity_index: int) -> set[str]:
    if rarity_index == 0:
        return {"simple", "basic"}
    if rarity_index == 1:
        return {"strong", "rare", "special"}
    if rarity_index == 2:
        return {"legendary", "epic", "mythical"}
    else:
        return {""}


def get_series_adjectives_set(series_index: int) -> set[str]:
    if series_index == 0:
        return {"chibi cute", "chibi young"}
    if series_index == 1:
        return {"young", "", "dynamic"}
    if series_index == 2:
        return {"gigantic", "massive"}
    else:
        return {""}


def get_style_suffix(series_index: int | None) -> set[str]:
    if series_index == 0:
        return {"anime chibi drawing style, pastel background"}
    if series_index == 1:
        return {"anime sketch with watercolor"}
    if series_index == 2:
        return {"polished final by studio ghibli"}
    else:
        return {"anime sketch"}


def get_random_style_suffix(series_index: int | None) -> str:
    return random.choice(list(get_style_suffix(series_index)))


def get_random_rarity_adjective(rarity_index: int) -> str:
    return random.choice(list(get_rarity_adjectives_set(rarity_index)))


def get_random_series_adjective(series_index: int | None) -> str:
    if series_index is None:
        return ""
    return random.choice(list(get_series_adjectives_set(series_index)))


def get_creature_types(element: Element) -> set[CreatuteType]:
    return CREATURES_BY_ELEMENT.get(element)


def get_closest_match(subject_override: str):
    if subject_override in ALL_SUBJECTS_BY_NAME:
        return ALL_SUBJECTS_BY_NAME[subject_override]
    else:
        # Create a new subject with the name of the override.
        return CreatuteType(subject_override, [WEARING_ARMOR])


def get_environments(element: Element) -> set[str]:
    return ENVIRONMENTS_BY_ELEMENT.get(element)


def get_random_ambience(element: Element) -> str:
    # Get a random ambience, but don't return the last one, which is for fully evolved pokemon.
    return random.choice(AMBIENCE_BY_ELEMENT.get(element)[:-1])


def get_random_detail_adjective(element: Element) -> str:
    joined_adjectives = GLOBAL_DETAIL_ADJECTIVES + DETAIL_ADJECTIVES_BY_ELEMENT.get(
        element
    )
    return random.choice(joined_adjectives)
