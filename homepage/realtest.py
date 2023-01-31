import random

amuguna_food = [
    {'food_name': 'Pizza', 'tag1': 'Italian', 'tag2': 'Cheese', 'tag3': 'Vegetable', 'tag4': 'Tomato Sauce'},
    {'food_name': 'Hamburger', 'tag1': 'Fast Food', 'tag2': 'Beef', 'tag3': 'Bread', 'tag4': 'Cheese'},
    {'food_name': 'Sushi', 'tag1': 'Japanese', 'tag2': 'Rice', 'tag3': 'Seafood', 'tag4': 'Wasabi'},
    # add more food items here
]

selected_tag = None
while amuguna_food:
    food = random.choice(amuguna_food)
    tags = [tag for tag in food.values() if tag not in ('food_name', selected_tag)]
    if not tags:
        break
    selected_tag = random.choice(tags)
    amuguna_food = [f for f in amuguna_food if selected_tag not in f.values()]
    print(food['food_name'], selected_tag)
else:
    print('donteat')