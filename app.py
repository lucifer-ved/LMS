from flask import Flask, render_template
import database
from views.bookmanager.BookManager import bookmanager_bp
from views.membermanager.MemberManager import membermanager_bp
from views.transactionmanager.TransactionManager import transactionmanager_bp
from views.dashboardmanager.DashboardManager import dashboardmanager_bp

def create_app():
    app = Flask(__name__,static_url_path='')
    #setup from config
    app.config.from_object('config.Dev')
    #setup from DB
    database.init_app(app)
    #for flash message
    app.secret_key = b'_5#y2RB"F4Q8z\n\xec]/'
    @app.route('/',defaults={'path1':''})
    def index():
        return render_template('index.html')
    app.add_url_rule('/',endpoint='index')

    @app.route('/login')
    def admin_login():
        return render_template('login.html')
    app.add_url_rule('/login',endpoint='admin_login')

    #register blueprint
    app.register_blueprint(bookmanager_bp,url_prefix='/book')
    app.register_blueprint(membermanager_bp,url_prefix='/member')
    app.register_blueprint(transactionmanager_bp,url_prefix='/transactions')
    app.register_blueprint(dashboardmanager_bp,url_prefix='/reports')
    
    return app

if __name__ == "__main__":
    create_app().run()
