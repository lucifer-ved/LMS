from api.api import PopulateBooks
from views.base import *
bookmanager_bp = Blueprint('bookmanager_bp',__name__,template_folder="templates/BookManager")
from models import Book
from api import *

@bookmanager_bp.route('/')
def book_list():
    books = Book.query.all()
    return render_template("books.html",books=books)

@bookmanager_bp.route('/add-book',methods=['POST'])
def add_book():
    print(request.form)
    if request.form:
        title = request.form.get('title')
        author = request.form.get('author')
        publisher = request.form.get('publisher')
        price = request.form.get('price')
        pages = request.form.get('pages')
        isbn = request.form.get('isbn')
        book = Book(title=title,author=author,publisher=publisher,price=price,pages=pages,isbn=isbn)
        commit_to_db(book,'add')
        return redirect(url_for('bookmanager_bp.book_list'))
    return render_template("addbook.html")

@bookmanager_bp.route('/populate-book',methods=('GET','POST'))
def populate_books():
    if request.form:
        no_of_books = request.form.get('noofbooks',type=int)
        book_records = list()
        book_list = PopulateBooks(no_of_books).fetch_books()
        for book_detail in book_list:
            book = Book(title=book_detail['title'], 
                        author=book_detail['author'],
                        publisher=book_detail['publisher'],
                        price=book_detail['price'],
                        pages=book_detail['pages'],
                        isbn=book_detail['isbn'])
            book_records.append(book)
        commit_to_db(book_records,'bulkadd')
        return redirect(url_for('bookmanager_bp.book_list'))
    return render_template("addbook.html")

@bookmanager_bp.route('/delete-book/<id>',methods=('GET','POST'))
def delete_book(id):
    if id:
        book = Book.query.filter_by(id=id)
        commit_to_db(book,'delete')
    return redirect(url_for('bookmanager_bp.book_list'))
    
@bookmanager_bp.route('/update-book/<id>',methods=('GET','POST'))
def update_book(id):
    book = Book.query.get(id)
    if id and not request.form:
        return render_template("updatebook.html",book=book)
    if request.form:
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.publisher = request.form.get('publisher')
        book.price = request.form.get('price')
        book.pages = request.form.get('pages')
        book.isbn = request.form.get('isbn')
        db.session.commit()
    return redirect(url_for('bookmanager_bp.book_list'))

@bookmanager_bp.route('/search-book',methods=['GET'])
def search_book():
    books = []
    if request.args:
        query = request.args.get('query')
        query = "%{}%".format(query)
        books = Book.query.filter(Book.title.like(query) | Book.author.like(query)).all()
    if len(books)>0:
        return render_template("books.html",books=books)
    else:
        return redirect(url_for('bookmanager_bp.book_list'))

