#!/usr/bin/env python

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

    argparser.add_argument(
        "-e",
        "--element",
        type=str,
        default=None,
        choices=[e.name.lower() for e in PokemonElements.ALL],
        help="Which element to generate monsters for.",
    )

    argparser.add_argument(
        "-s",
        "--subject",
        type=str,
        default=None,
        help="What type of monster to generate (e.g. monkey, dragon, etc.).",
    )

    args = argparser.parse_args()
    number_of_monsters = args.n_monsters
    element_name = args.element
    subject_override = args.subject
    element = (
        None
        if element_name is None
        else PokemonElements.get_element_by_name(element_name)
    )

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

        if element is None:
            n_monsters_to_generate = number_of_monsters * len(all_elements)
        else:
            n_monsters_to_generate = number_of_monsters

        for i in range(n_monsters_to_generate):
            current_element = (
                element if element else all_elements[i % len(all_elements)]
            )
            monsters = current_collection.generate_random_cards(
                element=current_element, subject_override=subject_override
            )
            print(*monsters, sep="\n\n")
        current_collection.export()


if __name__ == "__main__":
    main()
