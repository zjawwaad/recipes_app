from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at= data['created_at']
        self.updated_at=['updated_at']

    @classmethod
    def get_one_email(cls , data ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes_schema').query_db(query, data)

        if len( result ) > 0:
            current_user = cls( result[0] )
            return current_user
        else:
            return None

    @classmethod
    def create( cls, data ):
        query = "Insert INTO users( first_name, last_name, email, password ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return result


    @staticmethod
    def validate( data ):
        is_valid = True
        if len( data['first_name'] ) < 2:
            flash ("First name must be at least two characters" "error_registration_first_name")
            is_valid = False
        if len( data['last_name'] ) < 2:
            flash ("Last name must be at least two characters" "error_registration_last_name")
            is_valid = False
        if not EMAIL_REGEX.match( data['email'] ):
            flash( "Invalid email", "error_registration_email" )
            is_valid = False
        if data['password'] != data['confirm']:
            flash( "Passwords do not match", "error_registration_confirm" )
            is_valid = False
        return is_valid





        users = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            users.append( cls(user) )
        return users

