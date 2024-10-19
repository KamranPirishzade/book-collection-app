from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
all_books = []

db=SQLAlchemy(app)



class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250),nullable=False,unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return f"Book {self.title}"



@app.route('/')
def home():
    with app.app_context():
        books = Book.query.all()
    return render_template("index.html",books=books)


@app.route("/add",methods=["GET","POST"])
def add():
    if request.method == "POST":
        rating=request.form.get("rating")
        book=request.form.get("book")
        author=request.form.get("author")
        with app.app_context():
            db.create_all()
            new_book=Book(title=book, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))

        # all_books.append({"rating":rating,"book":book,"author":author})

    return render_template("add.html")

@app.route("/edit", methods=["GET","POST"])
def change_rating():
    if request.method == "POST":

        with app.app_context():
            book_id=int(request.args.get("id"))
            book = Book.query.get(book_id)
            book.rating= request.form.get("nrating")
            db.session.commit()
            return redirect(url_for("home"))
    with app.app_context():
        book_id = int(request.args.get('id'))
        book = Book.query.get(book_id)

    return render_template("change_rating.html",book=book)


@app.route("/del")
def delete():

    id=request.args.get('id')
    with app.app_context():
        book=Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

