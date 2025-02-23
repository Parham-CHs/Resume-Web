from flask import Flask, render_template, request, redirect, session
import secrets

import pandas as pd


app = Flask(__name__ , template_folder='./Havij' , static_folder='./Golabi')
app.secret_key = secrets.token_hex(16)

@app.route('/')
@app.route('/home')
def home():
    return render_template('./Resume/index.html')


@app.route('/login')
def login():


        
    failure_message = ""
    if request.args.get('failure'):
        failure_message = "Invalid username or password. Please try again."
    return render_template('login.html', message=failure_message)


@app.route('/register')
def register():
    return render_template('login.html')


@app.route('/login-post', methods=['post'])
def login_post():

    username = request.form['username']
    password = request.form['password']

    df = pd.read_csv('./Data/user_credentials.csv')
    # Check if the username exists
    if username in df['username'].values:
        # Get the correct password for the username
        correct_password = df.loc[df['username'] == username, 'password'].values[0]
        
        if password == correct_password:
            # If password matches, log in the user
            session['username'] = username
            redirect_path = '/home'
        else:
            # If password does not match, redirect to login failure
            redirect_path = '/login?failure=true'
    else:
        # If username does not exist, redirect to login failure
        redirect_path = '/login?failure=true'
    # return redirect(redirect_path)
    return redirect(redirect_path)

    # return render_template('login.html',  message="Invalid username or password. Please try again.")



@app.route('/register-post', methods=['POST'])
def register_post():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']
    
    # Load the DataFrame from the CSV file
    df = pd.read_csv('./Data/user_credentials.csv')
    # Create a new DataFrame with the new user's data
    new_user = pd.DataFrame({
        'username': [name],
        'password': [password],
        'email': [email]
    })

    # Append the new user to the existing DataFrame
    df = pd.concat([df, new_user], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    df.to_csv('./Data/user_credentials.csv', index=False)
    return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
