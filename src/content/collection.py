from dataclasses import dataclass, field
from functools import cached_property
import json
import os
import random
import shutil
from content.style import Style
from mechanics.card import Card
from mechanics.element import Element
from mechanics.rarity import Rarity


@dataclass
class Collection:

    collection_name: str
    theme_style: Style = field(default_factory=Style)

    rarities: list[Rarity] = field(default_factory=list)
    elements: list[Element] = field(default_factory=list)
    cards: list[Card] = field(default_factory=list)

    # Prevent duplicate cards and names.
    subjects_seen: set[str] = field(default_factory=set)
    card_names_seen: set[str] = field(default_factory=set)

    def generate_random_cards(
        self, element: Element = None, subject_override: str = None
    ) -> list[Card]:
        element = element if element else random.choice(self.elements)
        n_series = random.randint(1, 3)
        return self.generate_card_series(element, n_series, subject_override)

    def generate_card_series(
        self, element: Element, n: int = 1, subject_override: str = None
    ) -> list[Card]:

        # The last card in the series is always the highest in the series.
        # Each card in the series is one rarity higher than the previous.
        # Find the index of the starting rarity based on which rarities are available

        rarity_range = max(len(self.rarities) - n, 0)
        starting_rarity_index = (
            random.randint(0, rarity_range) if rarity_range > 0 else 0
        )
        new_cards = []
        card_style = None

        for i in range(n):
            rarity_index = min(len(self.rarities) - 1, starting_rarity_index + i)
            rarity = self.rarities[rarity_index]
            card = self.generate_card(
                element=element,
                rarity=rarity,
                inherited_style=card_style,
                series_index=i if n > 1 else None,
                subject_override=subject_override,
            )

            if i == 0:
                card_style = card.style

            new_cards.append(card)

        return new_cards

    def generate_card(
        self,
        element: Element,
        rarity: Rarity,
        style: Style = None,
        series_index: int | None = None,
        subject_override: str = None,
    ) -> Card:
        pass

    def get_default_element(self) -> Element:
        return self.elements[0]

    def to_json(self):
        return {
            "collection_name": self.collection_name,
            "cards": [card.to_json() for card in self.cards],
        }

    def export(self):
        collection_path = f"./output/{self.collection_name}/"
        cards_folder = f"./output/{self.collection_name}/cards"
        images_folder = f"./output/{self.collection_name}/images"
        rendered_cards_folder = f"./output/{self.collection_name}/renders"

        # If collection path exists, delete it.
        if os.path.exists(collection_path):
            shutil.rmtree(collection_path)

        os.makedirs(collection_path, exist_ok=True)
        os.makedirs(cards_folder, exist_ok=True)
        os.makedirs(images_folder, exist_ok=True)
        os.makedirs(rendered_cards_folder, exist_ok=True)

        # Export entire collection as a single file.
        with open(f"{collection_path}/{self.collection_name}.json", "w") as f:
            json.dump(self.to_json(), f, indent=2)

        # Export the collection's cards.
        for card in self.cards:
            card_path = f"{cards_folder}/{card.index:03d}_{card.snake_case_name}.json"
            with open(card_path, "w") as f:
                json.dump(card.to_json(), f, indent=2)

        # Export all image prompts so its easy to generate images.
        with open(f"{collection_path}/_image_prompts.txt", "w") as f:
            for card in self.cards:
                f.write(f"[{card.index:03d}] {card.name}\n")
                f.write(card.image_prompt)
                f.write("\n\n")
