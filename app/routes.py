from app import app
from app import db
from app.models import User

@app.route('/', methods=['GET'])
def index():
    return 'Hello from our flask api'

@app.route('/user', methods=['GET'])
def create_record():
    user = User(name='lyle',
                email='lyle@gmail.com')
    user.save()
    return user.to_json()