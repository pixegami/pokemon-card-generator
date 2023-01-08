from dataclasses import dataclass
import random
from pokemon_content.pokemon_content_pool import (
    AMBIENCE_BY_ELEMENT,
    get_closest_match,
    get_creature_types,
    get_environments,
    get_random_ambience,
    get_random_detail_adjective,
    get_random_rarity_adjective,
    get_random_series_adjective,
    get_random_style_suffix,
)
from content.collection import Collection
from content.style import Style
from mechanics.element import Element
from mechanics.card import Card
from mechanics.rarity import Rarity
from mechanics.ability import Ability
from pokemon_content.pokemon_prompts import (
    generate_card_name,
    generate_desc,
    get_image_prompt,
    get_visual_description,
)
from util.ability_name_library import get_ability_name
from util.gpt_call import is_openai_enabled


@dataclass
class PokemonCollection(Collection):

    BASE_POINTS = 4
    ABILITY_TO_HP_PTS = 2  # 1 ability cost is worth 2 HP points.
    NEUTRAL_ELEMENT_CHANCE = 0.5
    MIXED_ELEMENT_CHANCE = 0.5

    def generate_card(
        self,
        element: Element,
        rarity: Rarity,
        inherited_style: Style = None,
        series_index: int | None = None,
        subject_override: str = None,
    ) -> Card:

        is_part_of_series = series_index is not None
        if is_part_of_series:
            max_ability_points = self.get_points_budget(rarity.index, series_index)
        else:
            max_ability_points = self.get_points_budget(rarity.index, 1)

        hp_points = random.randint(0, max_ability_points // 2)
        ability_points = max_ability_points - hp_points
        ability_costs = self.get_ability_points_costs(ability_points, rarity.index)
        abilities = self.generate_abilities(element, ability_costs)

        for ability in abilities:
            ability.name = get_ability_name(ability)

        # Calculate HP
        bonus_hp_points = max_ability_points + (hp_points * self.ABILITY_TO_HP_PTS)
        hp = 10 * bonus_hp_points

        style = self.generate_style(
            inherited_style, element, rarity, series_index, subject_override
        )

        card = Card(
            index=len(self.cards) + 1,
            name="Untitled Card",
            element=element,
            rarity=rarity,
            abilities=abilities,
            hp=hp,
            style=style,
        )

        card.image_prompt = get_image_prompt(card)
        card.visual_description = get_visual_description(card)

        # Generate a name for the card.
        if is_openai_enabled:
            card.name = generate_card_name(card, self.card_names_seen)
            card.description = generate_desc(card)

        card.image_prompt = get_image_prompt(card)
        card.visual_description = get_visual_description(card)
        self.card_names_seen.add(card.name)
        self.cards.append(card)
        return card

    def generate_style(
        self,
        inherited_style: Style,
        element: Element,
        rarity: Rarity,
        series_index: int | None = None,
        subject_override: str = None,
    ) -> Style:

        style = Style(
            style_prefix=self.theme_style.style_prefix,
            style_suffix=self.theme_style.style_suffix,
        )

        style.subject_type = self.theme_style.subject_type

        # Pick the card's subject (creature type)
        if inherited_style is not None:
            style.subject = inherited_style.subject
            style.subject_adjectives = inherited_style.subject_adjectives
            style.detail = inherited_style.detail
            style.environment = inherited_style.environment
        else:

            if subject_override is not None:
                subject = get_closest_match(subject_override)
                style.subject = subject.name
            else:
                potential_subjects = get_creature_types(element)
                reduced_subjects: set = potential_subjects - self.subjects_seen
                if len(reduced_subjects) == 0:
                    reduced_subjects = potential_subjects

                subject = random.choice(list(reduced_subjects))
                self.subjects_seen.add(subject)
                style.subject = subject.name

            potential_details = set(subject.details)
            reduced_details: set = potential_details - self.subjects_seen
            if len(reduced_details) == 0:
                reduced_details = potential_details

            detail = random.choice(list(reduced_details))
            detail_adjective = get_random_detail_adjective(element=element)
            style.detail = detail.text(detail_adjective)

            # Pick the environment
            potential_environments = get_environments(element)
            style.environment = random.choice(potential_environments)

        # Pick adjective(s) for the subject.
        rarity_prefix = get_random_rarity_adjective(rarity.index)
        series_prefix = get_random_series_adjective(series_index)
        element_prefix = f"{element.name.lower()}-type"

        if series_index is not None:
            size_prefix = series_prefix
            if rarity.index >= 2:
                size_prefix += f" {rarity_prefix}"
        else:
            size_prefix = rarity_prefix

        style.subject_adjectives = [
            *self.theme_style.subject_adjectives,
            size_prefix,
            element_prefix,
        ]

        # Set the ambience
        if rarity.index >= 2 and series_index == 2:
            # Use the last background for the final card in the series.
            style.ambience = AMBIENCE_BY_ELEMENT.get(element)[-1]
        else:
            style.ambience = get_random_ambience(element)

        # Set the style suffix
        style.style_suffix = (
            f"{get_random_style_suffix(series_index)} {self.theme_style.style_suffix}"
        )

        return style

    def generate_abilities(self, element: Element, ability_costs: list[int]):
        abilities = []
        for i, cost in enumerate(ability_costs):
            is_primary = i == 0
            if (
                not is_primary
                and random.random() < PokemonCollection.NEUTRAL_ELEMENT_CHANCE
            ):
                ability_element = self.get_default_element()
            else:
                ability_element = element

            ability = PokemonCollection.generate_ability(ability_element, cost)
            abilities.append(ability)
        return abilities

    @staticmethod
    def get_points_budget(rarity_index: int, series_index: int) -> int:
        # Cards in a series start weaker, but get stronger as the series progresses.
        rarity_bonus = rarity_index
        series_bonus = series_index - 1
        return PokemonCollection.BASE_POINTS + rarity_bonus + series_bonus

    @staticmethod
    def generate_ability(element: Element, cost: int) -> Ability:

        is_mix = (
            not element.is_neutral
            and cost > 1
            and (random.random() < PokemonCollection.MIXED_ELEMENT_CHANCE)
        )
        ability = Ability(
            name="New Ability", element=element, cost=cost, is_mixed_element=is_mix
        )
        return ability

    @staticmethod
    def get_ability_points_costs(ability_points: int, rarity_index: int) -> list[str]:
        # Determine how many abilities the card will have, and how many points each ability will cost.
        if ability_points >= 6:
            return [4, ability_points - 4]
        elif ability_points >= 4:
            first_ability_cost = random.choice([3, 4])
            if first_ability_cost == 4:
                return [4]
            else:
                return [first_ability_cost, ability_points - first_ability_cost]
        elif ability_points == 3:
            if rarity_index < 1:
                return [2, 1]
            else:
                return [3] if random.random() < 0.5 else [2, 1]
        else:
            return [ability_points]
