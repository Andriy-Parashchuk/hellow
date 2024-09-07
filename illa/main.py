from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel


app = FastAPI()
library = {}


class Book(BaseModel):
    title: str
    author: str
    pages: int


@app.post("/books/")
def create_book(
    title: str = Query(..., min_length=3, max_length=30),
    author: str = Query(..., min_length=3, max_length=30),
    pages: int = Query(..., gt=10)
):
    book = Book(title=title, author=author, pages=pages)
    if book.author in library:
        for existing_book in library[book.author]:
            if existing_book.title == book.title:
                raise HTTPException(status_code=400, detail="Книга з такою назвою вже існує у цього автора.")
        library[book.author].append(book)
    else:
        library[book.author] = [book]
    return book


@app.get("/books/")
def get_all_books(author: str = Query(None, min_length=3, max_length=30)):
    if author:
        if author not in library:
            raise HTTPException(status_code=404, detail="Автор не знайдений")
        return library[author]
    return library

@app.put("/books/")
def update_book(
    title: str = Query(..., min_length=3, max_length=30),
    author: str = Query(..., min_length=3, max_length=30),
    new_title: str = Query(None, min_length=3, max_length=30),
    new_pages: int = Query(None, gt=10)
):
    if author not in library:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    for book in library[author]:
        if book.title == title:
            if new_title:
                book.title = new_title
            if new_pages:
                book.pages = new_pages
            return book
    raise HTTPException(status_code=404, detail="Книга не знайдена")

@app.delete("/books/")
def delete_book(
    title: str = Query(..., min_length=3, max_length=30),
    author: str = Query(..., min_length=3, max_length=30)
):
    if author not in library:
        raise HTTPException(status_code=404, detail="Автор не знайдений")
    for book in library[author]:
        if book.title == title:
            library[author].remove(book)
            if not library[author]:
                del library[author]
            return {"message": "Книга видалена"}
    raise HTTPException(status_code=404, detail="Книга не знайдена")