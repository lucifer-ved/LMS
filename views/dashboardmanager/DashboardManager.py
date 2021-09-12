from views.base import *
from flask import send_file
dashboardmanager_bp = Blueprint('dashboardmanager_bp',__name__,template_folder="templates/DashboardManager")
from models import MemberTransactions
from sqlalchemy import desc,text
import xlwt,io

POPULAR_BOOK = 'popularBook'
HIGHEST_PAYING_CUSTOMER = 'highestPayingCustomer'

@dashboardmanager_bp.route('/')
def reports():
    memberLabel,memberValues = get_highest_paying_customer_info()
    bookLabel,bookValues = get_popular_book_details()
    return render_template("dashboard.html",memberLabel=memberLabel,memberValues=memberValues,bookLabel=bookLabel,bookValues=bookValues)

@dashboardmanager_bp.route('/downloadreport/<type>',methods=['GET'])
def download_report(type):
    reportObj = getPopularBookObj() if type == POPULAR_BOOK else getHighestPayingCustomerObj()
    return export_to_excel(reportObj)

def get_highest_paying_customer_info():
    transactions = MemberTransactions.query.order_by(desc(MemberTransactions.outStandingBalance)).all()
    memberLabel = [t.memberId for t in transactions]
    memberValues = [t.outStandingBalance for t in transactions]
    #not working in case of string. why !?
    # memberLabel = ['Ved','Lucifer']
    memberLabel = list(set(memberLabel))
    return memberLabel, memberValues

def get_popular_book_details():
    bookIsbnNo = []
    memberCount = []
    sql = text('SELECT bookId,count(memberId) as count from membertransactions group by bookId')
    result = db.engine.execute(sql)
    for row in result:
        bookIsbnNo.append(row[0])
        memberCount.append(row[1])
    return bookIsbnNo,memberCount

def getHighestPayingCustomerObj():
    reportObj = {}
    reportObj['reportName'] = 'Popular Book Report'
    reportObj['headers'] = ['Name','Amount']
    transactions = MemberTransactions.query.order_by(desc(MemberTransactions.outStandingBalance)).all()
    memberName = [t.member.name for t in transactions]
    memberBalance = [t.outStandingBalance for t in transactions]
    reportObj['values'] = list(zip(list(set(memberName)), memberBalance))
    return reportObj

def getPopularBookObj():
    reportObj = {}
    reportObj['reportName'] = 'Highest Paying Buyer Report'
    reportObj['headers'] = ['Name','Buyers']
    sql = text('SELECT title,count(memberId) as count from membertransactions mt inner join books b on mt.bookId = b.isbn group by bookId')
    result = db.engine.execute(sql)
    bookName = []
    totalBuyer = []
    for row in result:
        bookName.append(row[0])
        totalBuyer.append(row[1])
    reportObj['values'] = list(zip(bookName, totalBuyer))
    return reportObj

def export_to_excel(reportObj):
    try:
        op = io.BytesIO()
        xl = xlwt.Workbook()
        sheet = xl.add_sheet(reportObj['reportName'])
        for i,h in enumerate(reportObj['headers']):
            #row,col,label
            sheet.write(0,i,h)
        
        cIndex = 0
        for i,v in enumerate(reportObj['values']):
            sheet.write(cIndex+1,0,v[0])
            sheet.write(cIndex+1,1,v[1])
            cIndex+=1

        xl.save(op)
        op.seek(0)

        return send_file(op, attachment_filename='reports.xlsx',as_attachment=True)
    except Exception as e:
        print(e)