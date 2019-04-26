from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyNewPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def index():
        
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
        new_blog=Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        
        blogs = Blog.query.all()
        return render_template('main-blog.html', bloglist = blogs)
    else:
        return render_template('new-blog.html', title_error=title_error, body_error=body_error,blog_title=title, blog_body=body)


@app.route('/blogentry', methods=['POST','GET'])
def blogEntry_post():
    id=request.args['id']

    blog=Blog.query.filter_by(id=id).first()
    return render_template('blog.html', blog=blog)

    


if __name__ == '__main__':
    app.run()