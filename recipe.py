import json
import requests
from bs4 import BeautifulSoup

API_KEY = 'e4290db1772e4d8c9f40e3b23d925001'  # Replace with your Spoonacular API key

def load_recipes():
    try:
        with open('recipes.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_recipes(recipes):
    with open('recipes.json', 'w') as file:
        json.dump(recipes, file)

def fetch_recipe(recipe_name):
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={recipe_name}&number=1&apiKey={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            recipe = data['results'][0]
            # Fetch recipe details using the ID
            recipe_id = recipe['id']
            details_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}'
            details_response = requests.get(details_url)
            if details_response.status_code == 200:
                details = details_response.json()
                ingredients = [ingredient['name'] for ingredient in details.get('extendedIngredients', [])]
                instructions = details.get('instructions', "No instructions available.")
                # Clean up instructions using BeautifulSoup
                instructions = BeautifulSoup(instructions, "html.parser").get_text()
                return {
                    "name": details['title'],
                    "ingredients": ingredients,
                    "instructions": instructions
                }
    return None

def add_recipe(recipes, recipe_name):
    recipe = fetch_recipe(recipe_name)
    if recipe:
        recipes.append(recipe)
        save_recipes(recipes)
        print(f"Recipe '{recipe_name}' added.")
    else:
        print(f"Recipe '{recipe_name}' not found in the API.")

def view_recipes(recipes):
    for recipe in recipes:
        print(f"\nName: {recipe['name']}")
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print(f" - {ingredient}")
        print("\nInstructions:")
        print(recipe['instructions'])

def search_recipes(recipes, search_term):
    found = [r for r in recipes if search_term.lower() in r['name'].lower()]
    return found

def display_recipe(recipe):
    print(f"\nName: {recipe['name']}")
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(f" - {ingredient}")
    print("\nInstructions:")
    print(recipe['instructions'])

def main():
    recipes = load_recipes()
    while True:
        action = input("\nEnter 'add' to add a recipe, 'view' to view all recipes, or enter a recipe name to see the recipe, or 'exit' to quit: ").strip()

        if action.lower() == 'add':
            recipe_name = input("Enter the recipe name to add: ")
            add_recipe(recipes, recipe_name)
        elif action.lower() == 'view':
            view_recipes(recipes)
        elif action.lower() == 'exit':
            break
        else:
            found_recipes = search_recipes(recipes, action)
            if found_recipes:
                for recipe in found_recipes:
                    display_recipe(recipe)
            else:
                print("No recipes found with that name.")

if __name__ == "__main__":
    main()
