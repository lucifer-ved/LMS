from views.base import *
membermanager_bp = Blueprint('membermanager_bp',__name__,template_folder="templates/MemberManager")
from models import Member

@membermanager_bp.route("/")
def memberlist():
    members = Member.query.all()
    return render_template("members.html",members=members)

@membermanager_bp.route('/addmember',methods=('GET','POST'))
def add_member():
    if request.form:
        name = request.form.get('name')
        email = request.form.get('email')
        member = Member(name=name,email=email)
        commit_to_db(member,'add')
        return redirect(url_for('membermanager_bp.memberlist'))
    return render_template("addmember.html")

@membermanager_bp.route('/deleteb/<id>',methods=('GET','POST'))
def delete_member(id):
    if id:
        member = Member.query.filter_by(id=id)
        commit_to_db(member,'delete')
    return redirect(url_for('membermanager_bp.memberlist'))


@membermanager_bp.route('/search',methods=['GET'])
def search_member():
    members = []
    if request.args:
        query = request.args.get('query')
        query = "%{}%".format(query)
        members = Member.query.filter(Member.name.like(query) | Member.email.like(query)).all()
    if members:
        return render_template("members.html",members=members)
    else:
        return redirect(url_for('membermanager_bp.memberlist'))

