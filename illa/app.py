from flask import Flask, render_template, request, redirect, url_for
from database import SessionLocal, engine
from models import Base, Book

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    db = SessionLocal()
    books = db.query(Book).all()
    db.close()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    db = SessionLocal()
    try:
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            pages=int(request.form['pages'])
        )
        db.add(book)
        db.commit()
    except Exception as e:
        db.rollback()
        return f"Error: {e}", 400
    finally:
        db.close()
    return redirect(url_for('index'))

@app.route('/delete_book', methods=['POST'])
def delete_book():
    db = SessionLocal()
    try:
        author = request.form['author']
        title = request.form['title']
        book = db.query(Book).filter(Book.author == author, Book.title == title).first()
        if book:
            db.delete(book)
            db.commit()
    except Exception as e:
        db.rollback()
        return f"Error: {e}", 400
    finally:
        db.close()
    return redirect(url_for('index'))


app.run(host='0.0.0.0', port=5000, debug=True)
