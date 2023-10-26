from faker import Faker 
from app import app
from models import User, db


fake= Faker()
with app.app_context():
    User.query.delete()
    users=[]
    for n in range(20):
        user = User(name=fake.name())
        users.append(user)
    db.session.add_all(users)
    db.session.commit()