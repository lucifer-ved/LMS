import functools
from flask import request,redirect,url_for,flash
from models import Book,Member

def validate_transaction_request(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        if request.form:
            isbn = request.form.get("isbn")
            member_email = request.form.get("member_email")
            if isbn :
                book_details = Book.query.filter_by(isbn=isbn).first()
                if not book_details: 
                    err = 'There is no such book with ISBN No : {} Please provide valid ISBN No'.format(isbn)
                    flash(err)
                    return redirect(url_for('transactionmanager_bp.transactions_list'))
                    
            if member_email:
                memberDetails = Member.query.filter_by(email=member_email).first()
                if not memberDetails:
                    err = 'Member with email : {} does not exist'.format(member_email)
                    flash(err)
                    return redirect(url_for('transactionmanager_bp.transactions_list'))
        return f(*args, **kws)
    return decorated_function

def validate_member(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        if request.form:
            member_email = request.form.get("email")
                    
            if member_email:
                member_exist = Member.query.filter_by(email=member_email).first()
                if member_exist:
                    err = 'Member with email : {} already exist.'.format(member_email)
                    flash(err)
                    return redirect(url_for('membermanager_bp.add_member'))
                    
        return f(*args, **kws)
    return decorated_function