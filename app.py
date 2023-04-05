from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///art.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/articles")
def articles():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles.html", articles=articles, art_cnt=len(articles))


@app.route("/articles/<int:id>")
def article_detail(id):
    post = Article.query.get(id)
    return render_template("post-detail.html", post = post)


@app.route("/articles/<int:id>/delete")
def article_delete(id):
    post = Article.query.get(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect("/articles")
    except Exception as e:
        return str(e)


@app.route("/articles/<int:id>/update", methods=["GET", "POST"])
def article_update(id):
    if request.method == "GET":
        post = Article.query.get(id)
        return render_template("update.html", post=post)

    elif request.method == "POST":
        post = Article.query.get(id)
        date = post.date
        db.session.delete(post)
        db.session.commit()

        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text, date=date)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/articles")
        except Exception as e:
            return str(e)


@app.route("/create-article", methods = ["GET","POST"])
def createarticle():
    if request.method == "GET":
        return render_template("create-article.html")
    elif request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    app.run(debug=False)