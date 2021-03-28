import urllib.request
import json
import os
from prettytable import PrettyTable

max_txt_len = 40

menu_url = 'https://www.themealdb.com/api/json/v1/1/categories.php'

def get_json_from_url(url):
    resp = urllib.request.urlopen(url).read().decode()
    return json.loads(resp)

def get_json_from_file(path):
    with open(path, 'rb') as f:
        return json.load(f)

categories = get_json_from_url(menu_url)['categories']
tot_categories = len(categories)

def show_categories():
    table = PrettyTable(('Id', 'Name', 'Description'))
    for c in categories:
        c_id = c['idCategory']
        c_name = c['strCategory']
        c_desc = c['strCategoryDescription']
        if len(c_desc) > max_txt_len:
            c_desc = c_desc[:max_txt_len] + '...'
        table.add_row((c_id, c_name, c_desc))
    print('\n'*100)
    os.system('clear')
    print(table)

while True:
    show_categories()
    print('\n1: Select category, 2: See a description, 3: Exit')
    ans = input('-> ')
    if ans == '1':
        print('Enter category id: ')
        try:
            ans = int(input('-> '))
            if ans < 1 or ans > tot_categories:
                input('The answer was not a valid id! ')
        except ValueError:
            input('You must enter a number! ')
        else:
            category_url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c='
            category_url += categories[ans-1]['strCategory']
            chosen_category_json = get_json_from_url(category_url)['meals']

            meal_options = PrettyTable(('Id', 'Name'))
            for meal in chosen_category_json:
                meal_options.add_row((meal['idMeal'], meal['strMeal']))

            while True:
                print('\n'*100)
                os.system('clear')
                print(meal_options)
                print('\n1: Select meal, 2: Go back to main menu')
                ans = input('-> ')

                if ans == '1':
                    print('Enter the meal ID: ')
                    ans = input('-> ')

                    meal_id_found = False
                    for meal in chosen_category_json:
                        if str(meal['idMeal']) == ans:
                            meal_id_found = True

                    if meal_id_found:
                        meal_url = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i='
                        meal_url += ans

                        meal_data = get_json_from_url(meal_url)['meals'][0]
                        meal_name = meal_data['strMeal']
                        meal_id = meal_data['idMeal']

                        meal_area = meal_data['strArea']
                        meal_instructions = meal_data['strInstructions']

                        while True: 
                            print('\n'*100)
                            os.system('clear')
                            print('- - - - - - - - -')
                            print(f'Showing recipie for: {meal_name}: (id: {meal_id})')
                            print(f'Location: {meal_area}')
                            print('- - - - - - - - -\n')

                            print(f'Instructions: [Option 1]')
                            print(f'Ingredients:  [Option 2]')

                            print('\n1: View instructions, 2: View ingredients, 3: Go back to sub-menu')
                            ans = input('-> ')

                            if ans == '1':
                                print('\n'*100)
                                os.system('clear')
                                input(meal_instructions)
                            elif ans == '2':
                                print('\n'*100)
                                os.system('clear')
                                print(f'Showing ingredients for {meal_name}:\n')

                                ingredient_table = PrettyTable(('Ingredient', 'Amount'))
                                for ingredient_numb in range(20):
                                    ingredient = 'strIngredient' + str(ingredient_numb+1)
                                    measure = 'strMeasure' + str(ingredient_numb+1)
                                    ingredient = meal_data[ingredient]
                                    measure = meal_data[measure]
                                    if ingredient == '' or ingredient == None:
                                        break
                                    ingredient_table.add_row((ingredient, measure))
                                input(ingredient_table)
                            elif ans == '3':
                                break
                            else:
                                input('Invalid option, please re-enter ')
                    else:
                        input('Your meal ID was not found, please press enter and then try again! ')

                elif ans == '2':
                    break
                else:
                    input('Invalid option, please re-enter ')
            
    elif ans == '2':
        print('Enter category id: ')
        try:
            ans = int(input('-> '))
            if ans < 1 or ans > tot_categories:
                input('The answer was not a valid id! ')
        except ValueError:
            input('You must enter a number! ')
        else:
            input(categories[ans-1]['strCategoryDescription'])
    elif ans == '3':
        break
    else:
        input('Your input was not an option! ')