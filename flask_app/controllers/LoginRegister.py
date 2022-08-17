
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask import render_template, redirect, session, flash, request
from flask import flash

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def register_account():
    session['first_name'] = request.form['first_name']
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    if not User.validate_register(request.form):
        return redirect('/')
    User.add_one(data)
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    
    allUsers = User.get_all()
    for user in allUsers:
        if request.form['email'] == user.email:
            if request.form['password'] == user.password:
                session['first_name'] = user.first_name
                session['id'] = user.id
                return redirect('/dashboard')
            else:
                flash('The password you entered is invalid')
                return redirect('/')
        
    flash('There is no email associated with our database')
    return redirect('/')

@app.route('/dashboard')
def home_page():
    recipes = Recipe.get_all()
    users = User.get_all()
    return render_template('dashboard.html', users= users ,recipes = recipes)

@app.route('/show/<int:id>')
def show_recipe(id):
    recipes = Recipe.get_all()
    return render_template("recipes.html", id = id, recipes = recipes)


@app.route('/edit/<int:id>')
def edit_page(id):
    recipes = Recipe.get_all()
    return render_template('editRecipes.html', recipes = recipes, id = id)

@app.route('/submit/<int:id>', methods=['POST'])
def submit_recipe(id):
    if not Recipe.validate_edit(request.form):
        
        return redirect('/edit/' + str(id))
    
    
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'datecooked' : request.form['datecooked'],
        'underThirty' : request.form['underThirty'],
        'ID' : request.form['ID']
    }
    Recipe.edit(data)
    return redirect('/dashboard')

@app.route('/createRecipe')
def create_recipe():
    return render_template('addRecipe.html')

@app.route('/submitRecipe', methods=['post'])
def success_recipe():
    if not Recipe.validate_edit(request.form):
        return redirect('createRecipe')
    data = {
        'id' : session['id'],
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'datecooked' : request.form['datecooked'],
        'underThirty' : request.form['underThirty']
    }
    Recipe.add_one(data)
    return redirect('/dashboard')