from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import random

app = Flask(__name__)

loaded_food_names = []
loaded_tags = set()
donteat = "donteat"

def get_random_food_and_tag():
    conn = sqlite3.connect('amuguna.db')
    c = conn.cursor()
    food_name = None
    tags = None
    c.execute("SELECT COUNT(*) FROM amuguna_food WHERE food_name NOT IN ({0})".format(','.join(['?']*len(loaded_food_names))), loaded_food_names)
    count = c.fetchone()[0]
    if count == 0:
        conn.close()
        return None, None
    while food_name is None or any(tag in loaded_tags for tag in tags):
        c.execute("SELECT food_name, tag1, tag2, tag3, tag4 FROM amuguna_food WHERE food_name NOT IN ({0}) ORDER BY RANDOM() LIMIT 1".format(','.join(['?']*len(loaded_food_names))), loaded_food_names)
        food = c.fetchone()
        if food is None:
            return None, None
        food_name = food[0]
        tags = (food[1], food[2], food[3], food[4])
    loaded_tags.update(tags)
    conn.close()
    return food_name, tags



@app.route('/')
def index():
    food_name, tags = get_random_food_and_tag()
    if food_name:
        random_tag = random.choice(tags)
        return render_template('index.html', food_name=food_name, tags=tags, random_tag=random_tag)
    else:
        return render_template('index.html', donteat = "donteat")


@app.route('/select', methods=['POST'])
def select():
    loaded_food_names.clear()
    loaded_tags.clear()
    return redirect(url_for('congrats'))

@app.route('/congrats')
def congrats():
    return render_template('chuka.html')

@app.route('/tag', methods=['POST'])
def tag():
    clicked_tag = request.form['tag']
    loaded_tags.add(clicked_tag)
    new_food_name, new_tags = get_random_food_and_tag()
    if new_food_name is None:
        return render_template('index.html', donteat = "donteat")
    while any(tag in new_food_name for tag in loaded_tags):
        new_food_name, new_tags = get_random_food_and_tag()
    random_tag = random.choice(new_tags)
    return render_template('index.html', food_name=new_food_name, tags=new_tags, random_tag=random_tag)

@app.route('/gunang', methods=['POST'])
def gunang():
    if 'random_tag' in request.form:
        loaded_tags.remove(request.form['random_tag'])
    else:
        # Handle the case where the key 'random_tag' does not exist
        return redirect(url_for('index'))  # redirect back to the index page

    new_food_name, new_tags = get_random_food_and_tag()
    if new_food_name is None:
        return render_template('index.html', donteat = "donteat")
    random_tag = random.choice(new_tags)
    return render_template('index.html', food_name=new_food_name, tags=new_tags, random_tag=random_tag)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)