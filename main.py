import sys
from datatypes import *
import configparser

def get_ingredient_list(database_path, recipe_names):
    recipes = load_recipes(database_path)
    ingredients = get_ingredients(recipes, recipe_names)
    for ingredient in ingredients:
        print(ingredient)

def search_ingredients(database_path, attributes):
    recipes = load_recipes(database_path)
    for recipe in recipes:
        for attribute in attributes:
            if '=' in attribute:
                key, value = re.split(r'[=<>]', attribute)
                if key in recipe.attributes and recipe.attributes[key] == value:
                    print(recipe.name)
                    break
            if '>' in attribute:
                key, value = re.split(r'[=<>]', attribute)
                if key in recipe.attributes and int(recipe.attributes[key]) > int(value):
                    print(recipe.name)
                    break
            if '<' in attribute:
                key, value = re.split(r'[=<>]', attribute)
                if key in recipe.attributes and int(recipe.attributes[key]) < int(value):
                    print(recipe.name)
                    break
            else:
                if attribute in recipe.ingredients:
                    print(recipe.name)
                    break

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if sys.argv[1] == "ingredients":
        if len(sys.argv) < 3:
            print("Usage: python main.py ingredients <recipe1> ...")
            return

        recipe_names = sys.argv[2:]

        get_ingredient_list(config['Paths']['database_path'], recipe_names)
        return

    if sys.argv[1] == "search":
        if len(sys.argv) < 3:
            print("Usage: python main.py search <attribute1=value1> <attribute2=value2> ...")
            return

        attributes = sys.argv[2:]

        search_ingredients(config['Paths']['database_path'], attributes)

if __name__ == "__main__":
    main()
