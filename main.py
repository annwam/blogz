from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:MyNewPass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key='pennyisawesome'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id= db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner ):
        self.title = title
        self.body = body
        self.owner= owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(120), unique=True)
    password= db.Column(db.String(120))
    blogs= db.relationship('Blog', backref= 'owner')

    def __init__(self, username, password):
        self.username =username
        self.password =password


@app.before_request
def require_login():
    allowed_routes=['login','sign_up']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    


@app.route('/login')
def login():
        # username = request.form['username']
        # bopassword = request.form['password']
        # #verify user to db
        # #If errors return message
        # #Send user object to html
        # #if not user--send them login
        # #if valid user send them to blog entry or main blog

    return render_template('login.html')

@app.route('/blog', methods=['POST', 'GET'])
def main_page():
        
        blogs = Blog.query.all()
        return render_template('main-blog.html', bloglist = blogs)
    

@app.route('/newpost', methods=['POST','GET'])
def new_post():

    title_error=''
    body_error=''
    title = ''
    body = ''

    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_body'] 
        #validate 
        if title=='':
            title_error="Please fill in the title"
        if body=='':
            body_error="Please fill in the body"

    if request.method=='POST' and not title_error and not body_error:        
        new_blog=Blog(title, body, User('username','password'))
        db.session.add(new_blog)
        db.session.commit()

        
        blogs = Blog.query.all()
        return render_template('main-blog.html', bloglist = blogs)
    else:
        return render_template('add-new-entry.html', title_error=title_error, body_error=body_error,blog_title=title, blog_body=body)


@app.route('/blogentry', methods=['POST','GET'])
def blogEntry_post():
    id=request.args['id']

    blog=Blog.query.filter_by(id=id).first()
    return render_template('blog.html', blog=blog)

@app.route('/sign_up', methods=['POST','GET'])
def sign_up():
#declare global variables
     user_name_error=''
     password_error=''
     verify_error=''
     existing_user_error=''
     username=''
#     #collect info from signup form
     if request.method=='POST':
         username = request.form['user_name']
         password = request.form['password']
         verify =request.form['verify']
    
        
#Verify username
         if username =='':
             user_name_error="Please enter a valid username"
         elif len(username)<3:
            user_name_error="Username must be more than 3 characters long"
            username = ''
         elif ' ' in username:
            user_name_error= "Your username cannot contain any spaces"
            username= ''

    #verify first password
         if password =='':
            password_error = "Please enter a valid password"
         elif len(password)<3:
            password_error="Password must be more than 3 characters long."
         elif " "in password:
            password_error="Your password cannot contain spaces."
    
        #verify second password
         if verify == '' or verify != password:
            verify_error="Please ensure that passwords match."
            verify = ''
    
    #Existing user error
         existing_user = User.query.filter_by(username=username).first()
         if existing_user:
            existing_user_error="Duplicate username"

#     #  without errors
     if request.method == 'POST' and not user_name_error and not password_error and not verify_error and not existing_user_error:
        #save user to db
           if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            #session['username'] = new_user

       
           return render_template('add-new-entry.html')

    #incase of errors
     else:
           return render_template('signup.html',name=username, 
            user_name_error = user_name_error,password_error = password_error, verify_error=verify_error, existing_user_error=existing_user_error)
     #return render_template('signup.html')



    #save user to db


# @app.route('/signmeup')
# def index():
#     return render_template('index.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect ('login.html')



if __name__ == '__main__':
    app.run()