import json
import random
import re
import string
from mechanics.element import Element
from mechanics.ability import Ability
from pokemon_content.pokemon_elements import PokemonElements
from util.gpt_call import gpt_client

DEFAULT_PATH = "data/ability_names.json"


def get_ability_name(ability: Ability) -> str:
    key = ability.ability_key
    with open(DEFAULT_PATH, "r") as f:
        ability_name_map = json.load(f)

    if key in ability_name_map:
        potential_names = ability_name_map[key]
        return random.choice(potential_names)
    else:
        print(f"Could not find ability name for {key}")
        return generate_ability_name(ability, 1)[0]


def generate_all_ability_names_to_file(path: str, elements: list[Element]) -> list[str]:

    ability_name_map = {}
    all_ability_names = set()
    abilities_per_key = 4
    all_mixed_element_values = [False, True]
    all_cost_values = [1, 2, 3, 4]

    for element, cost, is_mixed_element in [
        (element, cost, is_mixed_element)
        for element in elements
        for cost in all_cost_values
        for is_mixed_element in all_mixed_element_values
    ]:

        if element.is_neutral and is_mixed_element:
            continue

        ability = Ability(
            name="Ability",
            element=element,
            cost=cost,
            is_mixed_element=is_mixed_element,
        )

        # Generate more names for expensive abilities.
        abilities = generate_ability_name(ability, abilities_per_key + cost)

        # Make sure we don't add anything we've already seen.
        unique_abilities = [x for x in abilities if x not in all_ability_names]
        ability_name_map[ability.ability_key] = unique_abilities
        all_ability_names.update(unique_abilities)

        # Save each step so we don't lose progress if something goes wrong.
        with open(path, "w") as f:
            json.dump(ability_name_map, f, indent=2)


def generate_ability_name(ability: Ability, n: int) -> list[str]:
    ability_names = []
    prompt = generate_ability_name_prompt(ability, n)
    response = gpt_client().get_completion(prompt, max_tokens=512)
    common_delimters_regex = r"[\n\.\,\?\!\:\;]"
    response_text = response.choices[0].text
    ability_names = re.split(common_delimters_regex, response_text)

    # For all the ability names, remove any characters that are not letters or spaces.
    ability_names = [
        re.sub(r"[^a-zA-Z\s]", "", ability_name) for ability_name in ability_names
    ]

    # Remove empty strings from the list
    ability_names = [ability_name for ability_name in ability_names if ability_name]

    # Trim any whitespace from the beginning and end of each ability name
    ability_names = [ability_name.strip() for ability_name in ability_names]

    # Remove any names that do not have a letter in them.
    ability_names = [
        ability_name
        for ability_name in ability_names
        if re.search(r"[a-zA-Z]", ability_name)
    ]

    # Set them all to the same casing.
    ability_names = [string.capwords(ability_name) for ability_name in ability_names]
    print(f"Prompt: {prompt}\n")
    print(f"Raw Response: {response_text}\n")
    print(f"Generated {len(ability_names)} ability names: {ability_names}\n")
    return ability_names


def generate_ability_name_prompt(ability: Ability, n: int):
    cost_adjectives = [
        "weak, basic",
        "standard",
        "strong",
        "extremely powerful",
    ]
    ability_cost_description = cost_adjectives[ability.cost - 1]
    ability_elemental_description = (
        f"{ability.element.name} elemental"
        if not ability.element.is_neutral
        else "physical, neutral, non-elemental"
    )

    if not ability.element.is_neutral:
        if ability.is_mixed_element:
            ability_elemental_description = f"semi-physical {ability.element.name}"
        elif ability.cost > 2:
            ability_elemental_description = f"mythical {ability_elemental_description}"

    ability_description = f"{ability_cost_description} {ability_elemental_description}"

    if ability.cost <= 2:
        word_limit_prompt = f"(single-word ability names only)"
    else:
        word_limit_prompt = f"(max 1-2 words per ability name)"

    prompt = f"Generate {n} unique, original Pokemon attack name(s) for a {ability_description} attack "
    prompt += f"({word_limit_prompt}):\n"
    return prompt


if __name__ == "__main__":
    generate_all_ability_names_to_file(
        "data/generated_ability_names.json", [PokemonElements.FIGHTING]
    )
