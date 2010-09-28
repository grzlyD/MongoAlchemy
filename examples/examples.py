from pprint import pprint
from mongoalchemy.session import Session
from mongoalchemy.document import Document, Index, DocumentField
from mongoalchemy.fields import *

def main():
    s = Session.connect('mongoalchemy')
    
    class Address(Document):
        street_address = StringField()
        city = StringField()
        state_province = StringField()
        country = StringField()
    
    class User(Document):
        
        name_index = Index().ascending('name').unique()
        
        name = StringField()
        email = StringField()
        
        address = DocumentField(Address)
        
        def __str__(self):
            return '%s (%s)' % (self.name, self.email)
    
    s.clear_collection(User)
    
    a = Address(street_address='123 4th ave', city='NY', state_province='NY', country='USA')
    u = User(name='jeff', email='jeff@qcircles.net', address=a)
    s.insert(u)
    print u._id
    def print_all():
        for u in s.query(User).filter(User.f.address.country == 'USA' ):
            print u
    
    query = User.f.address.country == 'USA'
    
    print_all()
    
    update = s.query(User).filter(User.f.name > 'ivan', User.f.name < 'katie' ).set(User.f.email, 'jeff2@qcircles.net')
    update.execute()
    print_all()


if __name__ == '__main__':
    main()