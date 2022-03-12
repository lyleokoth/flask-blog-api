from app import db

class Author(db.Document):
    authorname = db.StringField(max_length=20, required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    profilePicture = db.StringField(default='')

    meta = {'collection': 'authors'}

    def to_json(self):
        return {
            "username": self.authorname,
            "email": self.email
            }

class Category(db.Document):
    name = db.StringField(max_length=20, required=True, unique=True)
    description = db.StringField()

    meta = {'collection': 'categories'}

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description
            }

class Post(db.Document):
    title = db.StringField(max_length=20, required=True, unique=True)
    description = db.StringField(required=True, unique=True)
    photo = db.StringField(required=False)
    author = db.ReferenceField(Author)
    categories = db.ListField(db.ReferenceField(Category))

    meta = {'collection': 'posts'}

    def categories_to_json(self):
        return [category.name for category in self.categories]

    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "photo": self.photo,
            "author": self.author.to_json(),
            "categories": self.categories_to_json()
            }

class User(db.Document):
    name = db.StringField()
    email = db.StringField()

    meta = {'collection': 'users'}

    def to_json(self):
        return {"name": self.name,
                "email": self.email}