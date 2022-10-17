from flask_app import app 
from flask import flash, render_template, request, redirect, session
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

# from curses import flash
bcrypt= Bcrypt( app )

@app.route('/')                           
def login():
    return render_template('login.html')  

@app.route ('/registration', methods = ['POST'])
def register(): 

    if User.validate( request.form ) == False:
        return redirect( '/' )

    user_exists = User.get_one_email( request.form )
    if user_exists != None:
        flash( "This email already exists", "error_registration_email")
        return redirect( '/' )
    #proceed to create user
    data = { 
        **request.form,
        "password" : bcrypt.generate_password_hash( request.form['password'])
    }
    user_id = User.create( data )
    
    session['first_name'] = data['first_name']
    session['email'] = data['email']
    session['user_id'] = user_id

    return redirect( '/recipes' )



@app.route('/user/login', methods = ['POST'])
def process_login():
    current_user = User.get_one_email( request.form )
    if current_user != None:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        if not bcrypt.check_password_hash(current_user.password, request.form ['password']):
            flash('Wrong Credentials', "error_login_credentials")
            return redirect( '/' )
    
        session['first_name'] = current_user.first_name
        session['email'] = current_user.email
        session['user_id'] = current_user.id

        return redirect( '/recipes' )
    else:
        flash('Wrong Credentials', "error_login_credentials")
        return redirect(  '/' )




if __name__=="__main__":
    app.run(debug=True)     