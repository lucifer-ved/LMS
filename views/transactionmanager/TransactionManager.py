from views.base import *
transactionmanager_bp = Blueprint('transactionmanager_bp',__name__,template_folder="templates/TransactionsManager")
from models import *
from datetime import date, timedelta

@transactionmanager_bp.route('/')
def transactions_list():
    transactions = MemberTransactions.query.all()
    return render_template("booktransactions.html",transactions=transactions)

@transactionmanager_bp.route('/issue-book',methods=['POST'])
@validate_transaction_request
def issue_book():
    if request.form:
        isbn = request.form.get("isbn")
        member_email = request.form.get("member_email")
        book_details = Book.query.filter_by(isbn=isbn).first()
        member_id = Member.query.filter_by(email=member_email).first().id
        issue_date = date.today()
        expiry_date = date.today()+timedelta(days=14)

        outstanding_balance = get_outstanding_balance(book_details,member_id)

        alreadyIssued = MemberTransactions.query.filter_by(book_id=isbn, member_id=member_id).first()
        if alreadyIssued:
            flash("You have already issued this book.")
            return redirect(url_for('transactionmanager_bp.transactions_list'))

        if outstanding_balance > 500:
            flash("Your outstanding balance amount would be more than Rs 500. Please pay due amount first.")
            return redirect(url_for('transactionmanager_bp.transactions_list'))
        
        transaction = MemberTransactions(book_id=isbn, member_id=member_id,issue_date=issue_date , expected_return_date=expiry_date,outstanding_balance=book_details.price,transaction_type='I')
        commit_to_db(transaction,'add')
    return redirect(url_for('transactionmanager_bp.transactions_list'))

@transactionmanager_bp.route('/return-book',methods=['POST'])
@validate_transaction_request
def return_book():
    if request.form:
        isbn = request.form.get("isbn")
        member_email = request.form.get("member_email")
        member_id = Member.query.filter_by(email=member_email).first().id

        issue_transaction = MemberTransactions.query.filter_by(book_id=isbn,member_id=member_id,transaction_type='I').first()           
        
        if issue_transaction:
            issue_transaction.return_date = date.today()
            issue_transaction.transaction_type = 'R'
            #can compute fine here
            issue_transaction.outstanding_balance = 0
            db.session.commit()
        else:
            flash("No such book is issued by {0}".format(member_email))

    return redirect(url_for('transactionmanager_bp.transactions_list'))

def get_outstanding_balance(book_details,member_id):
    outstanding_balance = 0
    current_book_price = book_details.price
    member = MemberTransactions.query.filter_by(member_id=member_id)
    outstanding_balance = member.first().outstanding_balance + current_book_price if member.count()>0 else current_book_price
    return outstanding_balance