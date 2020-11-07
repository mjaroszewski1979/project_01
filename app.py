from flask import Flask, redirect, render_template, url_for, request, session, g
import smtplib
import imghdr
from email.message import EmailMessage
import os

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='maciej', password='jaroszewski'))

app = Flask(__name__)
app.secret_key = 'secretkey'
port = int(os.environ.get('PORT', 5000))


@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/success',methods=['POST'] )
def success():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = 'Thank you {name} for your email. Please enter username: maciej and password: jaroszewski to view my full resume. Go to https://mjaro.herokuapp.com/login'.format(email=email, name=name)

        msg = EmailMessage()
        msg['Subject'] = 'Confirmation'
        msg['From'] = 'mjaroherokuapp@gmail.com'
        msg['To'] = email
        msg.set_content(message)

        with open('static/images/python.png', 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name

        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)    


        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('mjaroherokuapp@gmail.com', 'mjaroherokuapp1234')
            smtp.send_message(msg)
            
    return render_template('success.html', name=name)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('about'))
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/about')
def about():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('about.html')


if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
