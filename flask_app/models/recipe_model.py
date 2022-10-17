from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models.user_model import User

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_30 = data['under_30']
        self.created_at= data['created_at']
        self.updated_at=['updated_at']

    @classmethod
    def create( cls, data ):
        query = "INSERT INTO recipes (name, description, instructions, cooked_date, under_30, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30)s, %(user_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)
        
    @classmethod
    def get_all_with_users( cls ):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;'
        
        results = connectToMySQL (DATABASE).query_db ( query )
        list_recipes = []
        print( results )
        for row in results: 
            current_recipe = cls( row )
            user_data= {
                **row,
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
                'id' : row ['users.id']
            }
            current_user = User( user_data )
            current_recipe.user = current_user
            list_recipes.append( current_recipe )
        return list_recipes

    @classmethod
    def get_one_with_user( cls, data ):
        query = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'

        results = connectToMySQL (DATABASE).query_db ( query, data )
        if len( results ) > 0:
            current_recipe = cls( results[0] )
            user_data = {
                **results[0],
                'created_at' : results[0]['users.created_at'],
                'updated_at' :  results[0]['users.updated_at'],
                'id' :  results[0] ['users.id']
            }
            current_recipe.user = User( user_data)
            return current_recipe
        else:
            return None

    @classmethod
    def update_one( cls, data ):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_date = %(cooked_date)s, under_30 = %(under_30)s, user_id = %(user_id)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one( cls, data ):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)



    @staticmethod
    def validate_recipe( data ):
        is_valid = True
        if data['name']== "":
            flash("Name must not be empty", "error_recipe_name")
            is_valid = False
        if data['description']== "":
            flash("Description must not be empty", "error_recipe_description" )
            is_valid = False
        if data['instructions']== "":
            flash("Instructions must not be empty", "error_recipe_instructions")
            is_valid = False
        if data['cooked_date'] is None:
            flash("Cooked Date must not be empty", "error_recipe_cooked_date")
            is_valid = False
        if len( data['name'] ) < 3:
            flash( "Name must be at least 3 characters long", "error_recipe_name")
            is_valid = False
        if len( data['description'] ) < 3:
            flash( "Description must be at least 3 characters long", "error_recipe_description")
            is_valid = False
        if len( data['instructions'] ) < 3:
            flash( "instructions must be at least 3 characters long", "error_recipe_instructions")
            is_valid = False

        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"

        results = connectToMySQL('recipes_schema').query_db(query)

        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes