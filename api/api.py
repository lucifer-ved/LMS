import requests,json,random

class PopulateBooks():
    def __init__(self,no_of_books):
        self.endpoint='https://frappe.io/api/method/frappe-library?page={}'
        self.bookCount = no_of_books
        self.pageNo = random.randint(1, 10)

    def fetch_books(self):
        res = requests.get(url=self.endpoint.format(self.pageNo))
        try:
            if res.status_code == 200:
                res = json.loads(res.text)
                res = res['message']
                res = res[:self.bookCount]
                responseObj = self.serialize_result(res)
            return responseObj
        except Exception as e:
            print(e)
        finally:
            pass
        

    def serialize_result(self,res):
        responseList = []
        for book in res:
            bookObj = dict()
            bookObj['title'] = book['title']
            bookObj['author'] = book['authors']
            bookObj['publisher'] = book['publisher']
            bookObj['pages'] = book['  num_pages']
            bookObj['isbn'] = book['isbn']
            bookObj['price'] = random.randint(100, 500)
            responseList.append(bookObj)
        return responseList
