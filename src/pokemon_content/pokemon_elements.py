from mechanics.element import Element


class PokemonElements:
    NEUTRAL = Element(
        "Neutral",
        ascii_color="\033[37m",
        is_neutral=True,
    )
    FIRE = Element(
        "Fire",
        ascii_color="\033[31m",
    )
    WATER = Element(
        "Water",
        ascii_color="\033[34m",
    )
    GRASS = Element(
        "Grass",
        ascii_color="\033[32m",
    )
    ELECTRIC = Element(
        "Electric",
        ascii_color="\033[33m",
    )
    PSYCHIC = Element(
        "Psychic",
        ascii_color="\033[35m",
    )

    ALL = [NEUTRAL, FIRE, WATER, GRASS, ELECTRIC, PSYCHIC]
    _ELEMENTS_BY_NAME = {element.name.lower(): element for element in ALL}

    def get_element_by_name(name: str) -> Element:
        return PokemonElements._ELEMENTS_BY_NAME[name.lower()]


def get_resist(element: Element) -> Element:
    if element == PokemonElements.FIRE:
        return PokemonElements.GRASS
    elif element == PokemonElements.WATER:
        return PokemonElements.FIRE
    elif element == PokemonElements.GRASS:
        return PokemonElements.ELECTRIC
    elif element == PokemonElements.ELECTRIC:
        return PokemonElements.PSYCHIC
    else:
        return None


def get_weakness(element: Element) -> Element:
    if element == PokemonElements.FIRE:
        return PokemonElements.WATER
    elif element == PokemonElements.WATER:
        return PokemonElements.ELECTRIC
    elif element == PokemonElements.GRASS:
        return PokemonElements.FIRE
    elif element == PokemonElements.ELECTRIC:
        return None
    elif element == PokemonElements.NEUTRAL:
        return PokemonElements.PSYCHIC
    else:
        return None
