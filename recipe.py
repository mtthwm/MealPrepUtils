import re
import random

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

def search_ingredients(recipes, attributes):
    results = []
    for recipe in recipes:
        for attribute in attributes:
            if '=' in attribute:
                key, value = re.split(r'[=<>]', attribute)
                if key in recipe.attributes and recipe.attributes[key] == value:
                    results.append(recipe)
                    break
            elif '>' in attribute:
                key, value = re.split(r'[=<>]', attribute)
                if key in recipe.attributes and int(recipe.attributes[key]) > int(value):
                    results.append(recipe)
                    break
            elif '<' in attribute:
                key, value = re.split(r'[=<>]', attribute)
                if key in recipe.attributes and int(recipe.attributes[key]) < int(value):
                    results.append(recipe)
                    break
            else:
                if attribute in recipe.ingredients:
                    results.append(recipe)
                    break
    return results

def get_random_recipes(recipes: list[Recipe], count: int, average_effort: int):
    # Calculate the weights based on the difference between each recipe's effort and the average effort
    weights = [1 / (1 + abs(int(recipe.attributes.get('effort', 0)) - average_effort)) for recipe in recipes]

    if count >= len(recipes):
        return recipes
    
    # Randomly select "count" number of recipes based on the weights
    selections = set()
    while (len(selections) < count):
        selections.add(random.choices(recipes, weights=weights, k=1)[0])
    
    return selections
        