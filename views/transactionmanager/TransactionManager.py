from views.base import *
transactionmanager_bp = Blueprint('transactionmanager_bp',__name__,template_folder="templates/TransactionsManager")
from models import *
from datetime import date, timedelta

@transactionmanager_bp.route('/')
def transactionslist():
    transactions = MemberTransactions.query.all()
    return render_template("booktransactions.html",transactions=transactions)

@transactionmanager_bp.route('/issue',methods=['POST'])
@validate_transaction_request
def issue_book():
    if request.form:
        isbn = request.form.get("isbn")
        memberEmail = request.form.get("memberEmail")
        bookDetails = Book.query.filter_by(isbn=isbn).first()
        memberId = Member.query.filter_by(email=memberEmail).first().id
        issueDate = date.today()
        expiryDate = date.today()+timedelta(days=14)

        outStandingBalance = get_outstanding_balance(bookDetails,memberId)

        if outStandingBalance > 500:
            flash("Your outstanding balance amount would be more than Rs 500. Please pay due amount first.")
            return redirect(url_for('transactionmanager_bp.transactionslist'))

        alreadyIssued = MemberTransactions(bookId=isbn, memberId=memberId)
        if alreadyIssued.count()>0:
            flash("You have already issued this book.")
            return redirect(url_for('transactionmanager_bp.transactionslist'))
        else:
            transaction = MemberTransactions(bookId=isbn, memberId=memberId,issueDate=issueDate , expReturnDate=expiryDate,outStandingBalance=bookDetails.price,transactiontype='I')
            commit_to_db(transaction,'add')
    return redirect(url_for('transactionmanager_bp.transactionslist'))

@transactionmanager_bp.route('/return',methods=['POST'])
@validate_transaction_request
def return_book():
    if request.form:
        isbn = request.form.get("isbn")
        memberEmail = request.form.get("memberEmail")
        memberId = Member.query.filter_by(email=memberEmail).first().id

        issueTransaction = MemberTransactions.query.filter_by(bookId=isbn,memberId=memberId,transactiontype='I').first()           
        if issueTransaction:
            issueTransaction.returnDate = date.today()
            issueTransaction.transactiontype = 'R'
            #can compute fine here
            issueTransaction.outStandingBalance = 0
            db.session.commit()

    return redirect(url_for('transactionmanager_bp.transactionslist'))

def get_outstanding_balance(bookDetails,memberId):
    outStandingBalance = 0
    currentBookPrice = bookDetails.price
    member = MemberTransactions.query.filter_by(memberId=memberId)
    outStandingBalance = member.first().outStandingBalance + currentBookPrice if member.count()>0 else currentBookPrice
    return outStandingBalance