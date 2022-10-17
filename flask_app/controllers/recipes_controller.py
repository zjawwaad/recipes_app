from flask_app import app 
from flask import flash, render_template, request, redirect, session
from flask_app.models.recipe_model import Recipe

# Move to recipes controller 
@app.route('/recipes')
def display_recipes():
    if 'email' not in session:
        return redirect ('/')
    list_recipes = Recipe.get_all_with_users()
    return render_template('home.html', list_recipes = list_recipes)

# @app.route('/create/recipe',methods=['POST'])
# def create_recipe():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     if not Recipe.validate_recipe(request.form):
#         return redirect('/new/recipe')
#     data = {
#         "name": request.form["name"],
#         "description": request.form["description"],
#         "instructions": request.form["instructions"],
#         "under30": int(request.form["under30"]),
#         "date_made": request.form["date_made"],
#         "user_id": session["user_id"]
#     }

@app.route('/recipes/new')
def display_create_recipe():
    if 'email' not in session:
        return redirect( '/' )
    return render_template('newrecipe.html')

@app.route( '/recipe/create', methods = ['POST'] )
def create_recipe():
    if Recipe.validate_recipe( request.form ) == False:
        return redirect('/recipes/new')

    data = {
        **request.form,
        "user_id" : session['user_id']
    }

    Recipe.create(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def display_one( id ):
    if 'email' not in session:
        return redirect( '/' )   
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_one_with_user( data )
    return render_template('viewrecipe.html', current_recipe = current_recipe)

@app.route('/recipes/<int:id>/update')
def display_update_recipe( id ):
    if 'email' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_one_with_user( data )
    return render_template( "editrecipe.html", current_recipe = current_recipe)


app.route('/recipe/update<int:id>', methods = ['POST'] )
def update_recipe( id ):
    if Recipe.validate_recipe( request.form ) == False:
        return redirect(f'/recipes/{id}/update')
    recipe_data= {
        **request.form,
        "id" : id,
        "user_id" : session['user_id']
    }
    Recipe.update_one( recipe_data )
    return redirect ('/recipes')


@app.route( '/recipes/<int:id>/delete')
def delete_recipe( id ):
    data = { 
        "id" : id
    }
    Recipe.delete_one( data )
    return redirect( '/recipes')

@app.route( '/user/logout')
def process_logout():
    session.clear()
    return redirect('/')