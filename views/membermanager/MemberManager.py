from views.base import *
membermanager_bp = Blueprint('membermanager_bp',__name__,template_folder="templates/MemberManager")
from models import Member

@membermanager_bp.route("/")
def member_list():
    members = Member.query.all()
    return render_template("members.html",members=members)

@membermanager_bp.route('/add-member',methods=('GET','POST'))
@validate_member
def add_member():
    if request.form:
        name = request.form.get('name')
        email = request.form.get('email')
        member = Member(name=name,email=email)
        commit_to_db(member,'add')
        return redirect(url_for('membermanager_bp.member_list'))
    return render_template("addmember.html")

@membermanager_bp.route('/delete-member/<id>',methods=('GET','POST'))
def delete_member(id):
    if id:
        member = Member.query.filter_by(id=id)
        commit_to_db(member,'delete')
    return redirect(url_for('membermanager_bp.member_list'))


@membermanager_bp.route('/search-member',methods=['GET'])
def search_member():
    members = []
    if request.args:
        query = request.args.get('query')
        query = "%{}%".format(query)
        members = Member.query.filter(Member.name.like(query) | Member.email.like(query)).all()
    if members:
        return render_template("members.html",members=members)
    else:
        return redirect(url_for('membermanager_bp.member_list'))

