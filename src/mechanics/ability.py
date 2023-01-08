from dataclasses import dataclass
from functools import cached_property
import math

from mechanics.element import NEUTRAL, Element

CIRCLE_UNICODE = "●"


@dataclass(kw_only=True)
class Ability:

    name: str
    element: Element
    cost: int = 1  #  Between 1 and 4
    is_mixed_element: bool = False  #  Whether the ability is part neutral.

    @cached_property
    def power(self):
        base_power = self.cost * 10

        # If it's mixed or fully elemental, it's stronger.
        if self.element.is_neutral:
            elemental_bonus_points = 0
        else:
            if self.is_mixed_element or self.cost == 1:
                elemental_bonus_points = 10
            else:
                elemental_bonus_points = 20

        return base_power + elemental_bonus_points

    @cached_property
    def elemental_cost(self) -> int:
        if self.element.is_neutral:
            # No elements are used.
            return 0
        elif self.is_mixed_element:
            # Half of the cost is used (rounded up).
            return math.ceil(self.cost / 2)
        else:
            # All the cost is elemental.
            return self.cost

    @cached_property
    def ability_key(self):
        """Returns a key that can be used to identify the ability of the same stats"""
        mixed_modifier = "mixed" if self.is_mixed_element else "pure"
        extra_power = "standard"
        return f"{self.element.name}_{self.cost}_{mixed_modifier}_{extra_power}".lower()

    def __repr__(self):
        cost_str = ""
        for i in range(self.cost):
            if i < self.elemental_cost:
                # The cost is elemental.
                cost_str += f"{self.element.with_ascii_color(CIRCLE_UNICODE)} "
            else:
                # The cost is neutral.
                cost_str += f"{NEUTRAL.with_ascii_color(CIRCLE_UNICODE)} "

        message = f"{self.name} ({self.element.ascii_name()})\n"
        message += f"  Cost: {cost_str}\n"
        message += f"  Power: {self.power}\n"
        return message

    @property
    def costs_as_elements(self) -> list[str]:
        """Returns a list of elements that the ability costs."""
        return [self.element.name] * self.elemental_cost + [NEUTRAL.name] * (
            self.cost - self.elemental_cost
        )

    def to_json(self):
        return {
            "name": self.name,
            "element": self.element.name,
            "cost": self.cost,
            "is_mixed_element": self.is_mixed_element,
            "power": self.power,
        }
