from mechanics.rarity import Rarity


class PokemonRarity:
    COMMON = Rarity("common", 0)
    UNCOMMON = Rarity("uncommon", 1)
    RARE = Rarity("rare", 2)

    ALL = [
        COMMON,
        UNCOMMON,
        RARE,
    ]

    RARITY_BY_NAME = {rarity.name: rarity for rarity in ALL}

    @classmethod
    def get_rarity_by_name(cls, name: str) -> Rarity:
        if name not in cls.RARITY_BY_NAME:
            return cls.RARE
        return cls.RARITY_BY_NAME[name]
