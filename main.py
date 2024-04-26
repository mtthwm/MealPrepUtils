import sys
from recipe import *
import configparser

def get_ingredient_list(database_path, recipe_names):
    recipes = load_recipes(database_path)
    ingredients = get_ingredients(recipes, recipe_names)
    for ingredient in ingredients:
        print(ingredient)

def search_ingredients(database_path, attributes):
    recipes = load_recipes(database_path)
    results = search_ingredients(recipes, attributes)
    for recipe in results:
        print(recipe.name)

def get_recipes(database_path, num, average_effort):
    recipes = load_recipes(database_path)
    recipes = get_random_recipes(recipes, num, average_effort)
    for recipe in recipes:
        print(recipe.name)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if len(sys.argv) < 2:
        print("Usage: python main.py <ingredients|search|...> ...")
        return

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

    if sys.argv[1] == "get_recipes":
        if len(sys.argv) < 4:
            print("Usage: python main.py search <num> <effort>")
            return
        
        num = int(sys.argv[2])
        average_effort = int(sys.argv[3])

        get_recipes(config['Paths']['database_path'], num, average_effort)

if __name__ == "__main__":
    main()
