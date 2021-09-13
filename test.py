import unittest,json,database
from models import *
from app import create_app

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('config.Test')
        database.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        Member(name='test',email='test@gmail.com')
        Book(title='My Book',author='I,Me,My Self',publisher='I,Me,My Self',price=400,pages=100,isbn=2345678)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_manage_book_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code,200)
    
    def test_add_book(self):
        data = {
                    'title':'My Book',
                    'author':'I,Me,My Self',
                    'publisher':'I,Me,My Self',
                    'price':400,
                    'pages':100,
                    'isbn':1234567
                }
        res = self.client.post('/book/add_book',data=data,content_type='application/json',follow_redirects=True)
        self.assertEqual(res.status_code,200)

    def test_delete_book(self):
        data = {'id':2345678}
        res = self.client.delete('/book/delete-book/2345678',data=data,follow_redirects=True)
        self.assertEqual(res.status_code,200)

    def test_issue_book(self):
        data = {'isbn':2345678,'email':'test@gmail.com'}
        res = self.client.post('/transactions/issue-book/',data=data,follow_redirects=True)
        self.assertEqual(res.status_code,200)

    def test_return_book(self):
        data = {'isbn':2345678,'email':'test@gmail.com'}
        res = self.client.post('/book/return-book',data=data,follow_redirects=True)
        self.assertEqual(res.status_code,200)

if __name__ == '__main__':
    unittest.main()