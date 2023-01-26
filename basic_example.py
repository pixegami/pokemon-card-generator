from random import choice

rarity = ["common", "uncommom", "rare"]
elements = ["fire", "water", "grass"]
creature = ["lizard", "bear", "monkey"]

for i in range(5):
    print(f"{i}: ", choice(rarity), choice(elements), choice(creature))
