from database import db
import enum

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Integer(),nullable=False)
    publisher = db.Column(db.String(80),nullable=False)
    pages = db.Column(db.Integer())
    isbn = db.Column(db.Integer(),nullable=False)
 

class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False)


class TransactionType(enum.Enum):
    I = 'I'
    R = 'R'

class MemberTransactions(db.Model):
    __tablename__ = "membertransactions"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer,db.ForeignKey("books.isbn"), nullable=False)
    member_id = db.Column(db.Integer,db.ForeignKey("member.id"), nullable=False)
    book = db.relationship("Book", backref="book")
    member = db.relationship("Member", backref="member")
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    expected_return_date  = db.Column(db.Date, nullable=False)
    outstanding_balance = db.Column(db.Integer,nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType))



