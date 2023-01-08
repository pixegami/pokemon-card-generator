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
