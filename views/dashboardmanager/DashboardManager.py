from views.base import *
from flask import send_file
dashboardmanager_bp = Blueprint('dashboardmanager_bp',__name__,template_folder="templates/DashboardManager")
from models import MemberTransactions
from sqlalchemy import desc,text
import xlwt,io,json

POPULAR_BOOK = 'popularBook'
HIGHEST_PAYING_CUSTOMER = 'highestPayingCustomer'

@dashboardmanager_bp.route('/')
def reports():
    member_label,member_values = get_highest_paying_customer_details()
    book_label,book_values = get_popular_book_details()
    return render_template("dashboard.html",memberLabel=member_label,memberValues=member_values,bookLabel=book_label,bookValues=book_values)

@dashboardmanager_bp.route('/download-report/<type>',methods=['GET'])
def download_report(type):
    report_obj = get_popular_book_obj() if type == POPULAR_BOOK else get_highest_paying_customer_obj()
    return export_to_excel(report_obj)

def get_highest_paying_customer_obj():
    report_obj = {}
    report_obj['report_name'] = 'Popular Book Report'
    report_obj['headers'] = ['Name','Amount']
    member_name, member_balance = get_highest_paying_customer_details()
    report_obj['values'] = list(zip(member_name, member_balance))
    return report_obj

def get_popular_book_obj():
    report_obj = {}
    report_obj['report_name'] = 'Highest Paying Buyer Report'
    report_obj['headers'] = ['Name','Buyers']
    book_name,total_buyer = get_popular_book_details()
    report_obj['values'] = list(zip(book_name, total_buyer))
    return report_obj

def get_popular_book_details():
    sql = text('SELECT title,count(member_id) as count from membertransactions mt inner join books b on mt.book_id = b.isbn where mt.transaction_type="I" group by book_id order by count desc;')
    result = db.engine.execute(sql)
    book_name = []
    total_buyer = []
    for row in result:
        if row[0] not in book_name:book_name.append(row[0])
        total_buyer.append(row[1])
    return book_name,total_buyer

def get_highest_paying_customer_details():
    transactions = MemberTransactions.query.order_by(desc(MemberTransactions.outstanding_balance)).all()
    member_name = {t.member.name for t in transactions}
    member_balance = [t.outstanding_balance for t in transactions]
    return list(member_name),member_balance



def export_to_excel(report_obj):
    try:
        op = io.BytesIO()
        xl = xlwt.Workbook()
        sheet = xl.add_sheet(report_obj['report_name'])
        for i,h in enumerate(report_obj['headers']):
            #row,col,label
            sheet.write(0,i,h)
        
        cIndex = 0
        for i,v in enumerate(report_obj['values']):
            sheet.write(cIndex+1,0,v[0])
            sheet.write(cIndex+1,1,v[1])
            cIndex+=1

        xl.save(op)
        op.seek(0)

        return send_file(op, attachment_filename='reports.xlsx',as_attachment=True)
    except Exception as e:
        print(e)