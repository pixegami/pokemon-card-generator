import argparse
import random
from pokemon_content.pokemon_collection import PokemonCollection
from pokemon_content.pokemon_elements import PokemonElements
from content.style import Style
from pokemon_content.pokemon_rarity import PokemonRarity


def main():

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-n",
        "--n_monsters",
        type=int,
        default=1,
        help="Number of monsters to generate per element.",
    )

    args = argparser.parse_args()
    number_of_monsters = args.n_monsters

    pokemon_style: Style = Style(
        subject_type="pokemon",
        style_suffix="--niji",
    )

    classic_collection = PokemonCollection(
        "pokemon-classic",
        theme_style=pokemon_style,
        elements=PokemonElements.ALL,
        rarities=PokemonRarity.ALL,
    )

    all_collections = [
        classic_collection,
    ]

    collection_seed = random.randint(0, 1000000)
    for current_collection in all_collections:
        random.seed(collection_seed)
        all_elements = current_collection.elements
        n_monsters_to_generate = number_of_monsters * len(all_elements)

        for i in range(n_monsters_to_generate):
            element = all_elements[i % len(all_elements)]
            monsters = current_collection.generate_random_cards(element=element)
            print(*monsters, sep="\n\n")
        current_collection.export()


if __name__ == "__main__":
    main()
