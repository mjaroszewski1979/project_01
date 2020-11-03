from flask import Flask, render_template, url_for,request
import os


app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/success',methods=['POST'] )
def success():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = 'User {name}, {email} have requested contact'.format(email=email, name=name)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login('mjaroherokuapp@gmail.com', 'mjaroherokuapp1234')
        server.sendmail('mjaroszewski1979@gmail.com', email, message)
    return render_template('success.html', name=name)

if __name__=='__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
