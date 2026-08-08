
from fastapi import APIRouter, Query, Header, HTTPException, status, Response
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from schemas import BookAddSchema, BookUpdateSchema, BookResponseSchema, LiteratureGenres

router = APIRouter()

templates = Jinja2Templates(directory="templates")

books_list = [
        {
            "id": 1,
            "title": "Harry Potter",
            "genre": LiteratureGenres.fantasy,
            "author": "Rowling"
        },

        {
            "id": 2,
            "title": "Magus",
            "genre": LiteratureGenres.romance,
            "author": "John Fowles"
        }
    ]


@router.get(
    "/",
    tags=["Книги"],
    response_class=HTMLResponse,)
def home(request: Request):
    #my_header: str = Header(..., alias="X-My-Special.Header")
    # request_custom_header = request.headers.get("X-Request-ID")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        # context={"my_header": my_header}
    )


@router.get(
    "/books/",
    tags=["Книги"],
    summary="Отримати всі книги",
    response_class=HTMLResponse
)
def get_books(request: Request) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="getBooksResponse.html",
        context={"context_data": books_list}
    )


@router.get(
    "/books",
    tags=["Книги"],
    summary="Отримати книги по фільтру(author)",
    response_class=HTMLResponse
)
def get_books_by_filter(
    request: Request,
    author: str = Query(default="")
) -> HTMLResponse:

    if author:
        res_list = list(filter(lambda book: book["author"] == author, books_list))
    else:
        res_list = books_list


    if not res_list:

        raise HTTPException(
            status_code=404,
            detail=f"Book by author '{author}' not found."
        )

    return templates.TemplateResponse(
        request=request,
        name="getBooksResponse.html",
        context={"context_data": res_list},
        status_code=200
    )


@router.post(
    "/books/",
    tags=["Книги"],
    summary="Додати книгу"
)
def add_book(book: BookAddSchema):

    return {
        "status_code": 200,
        "title": book.title,
        "genre": book.genre,
        "author": book.author
    }


@router.put(
    "/books/{id}",
    tags=["Книги"],
    summary="Оновити книгу по id"
)
def update_book(id: int, new_book_data: BookUpdateSchema):

    book_found = False

    for book in books_list:
        if book["id"] == id:
            book["title"] = new_book_data.title
            book["genre"] = new_book_data.genre
            book["author"] = new_book_data.author
            book_found = True

    if not book_found:
        raise HTTPException(
            status_code=400,
            detail=f"Book with id '{id}' not found."
        )


    return {
        "status_code": 200,
        "id": id,
        "title": new_book_data.title,
        "genre": new_book_data.genre,
        "author": new_book_data.author
    }