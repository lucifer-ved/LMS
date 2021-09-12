import functools
from flask import request,redirect,url_for,flash
from models import Book,Member

def validate_transaction_request(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        if request.form:
            isbn = request.form.get("isbn")
            memberEmail = request.form.get("memberEmail")
            if isbn :
                bookDetails = Book.query.filter_by(isbn=isbn)
                if bookDetails.count() == 0: 
                    err = 'There is no such book with ISBN No : {} Please provide valid ISBN No'.format(isbn)
                    flash(err)
                    return redirect(url_for('transactionmanager_bp.transactionslist'))
                    
            if memberEmail:
                memberDetails = Member.query.filter_by(email=memberEmail)
                if memberDetails.count() == 0:
                    err = 'Member with email : {} does not exist'.format(memberEmail)
                    flash(err)
                    return redirect(url_for('transactionmanager_bp.transactionslist'))
        return f(*args, **kws)
    return decorated_function