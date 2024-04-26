import re

class Recipe:
    def __init__(self, name: str, ingredients: list[str], attributes: dict[str, str]):
        self.name = name
        self.ingredients = ingredients
        self.attributes = attributes

    @classmethod
    def parse_from_string(cls, recipe_string: str) -> 'Recipe':
        lines = recipe_string.strip().split('\n')
        name = lines[0].strip()
        attributes = {}
        ingredients = []

        for line in lines[1:]:
            line = line.strip()
            if line.startswith('@'):
                attribute, value = line[1:].split('=')
                attributes[attribute.strip()] = value.strip()
            elif line.startswith('-'):
                ingredients.append(line[1:].strip())

        return cls(name=name, ingredients=ingredients, attributes=attributes)

    def __str__(self) -> str:
        recipe_string = self.name + '\n'
        for attribute, value in self.attributes.items():
            recipe_string += f'    @{attribute}={value}\n'
        for ingredient in self.ingredients:
            recipe_string += f'    - {ingredient}\n'
        return recipe_string


def extract_blocks(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    blocks = []

    for line in lines:
        if re.match(r'^\s+.+', line):
            blocks[len(blocks) - 1] += line
        else:
            blocks.append(line)

    return blocks

def load_recipes(file_path: str) -> list[Recipe]:
    blocks = extract_blocks(file_path)
    return [Recipe.parse_from_string(block) for block in blocks]

def write_recipes(file_path: str, recipes: list[Recipe]) -> None:
    with open(file_path, 'w') as file:
        for recipe in recipes:
            file.write(str(recipe) + '\n')

def get_ingredients (recipes: list[Recipe], recipe_names: list[str]) -> list[str]:
    ingredients = set()
    for recipe in recipes:
        if recipe.name in recipe_names:
            for ingredient in recipe.ingredients:
                ingredients.add(ingredient)
    return ingredients