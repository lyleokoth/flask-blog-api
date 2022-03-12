from crypt import methods
from app import app
from app import db
from app.models import Author, Post, Category, User
from flask import Response
import json
from flask import request
from mongoengine.errors import NotUniqueError
import bcrypt


@app.route('/', methods=['GET'])
def index():
    return 'Hello from our flask api'

#Register new Author
@app.route('/api/auth/register', methods=['POST'])
def register_author():
    try:
        record = json.loads(request.data)
        hashedPassword = bcrypt.hashpw(record['password'].encode('utf-8'), app.config['SALT'])
        author = Author(
            authorname = record['name'],
            email = record['email'],
            password = hashedPassword,
            profilePicture = record['photo']
        )
        author.save()
        return author.to_json(), 200
    except NotUniqueError as e:
        return {'error': f"An author with the name {record['name']} already exists"}, 401 
    except Exception as e:
         return Response(str(e), status=201, mimetype='application/json')     

#Login an existing Author
@app.route('/api/auth/login', methods=['POST'])
def login_author():
    try:
        record = json.loads(request.data)
        author = Author.objects(authorname=record['name']).first()
        if not author:
            #Acess denied
            return {'error': 'Wrong credentials'}, 400

        if bcrypt.checkpw(record['password'].encode('utf-8'), author.password.encode('utf-8')):
            return author.to_json(), 200
        else:
            #Acess denied
            return {'error': 'Wrong credentials'}, 400
    except Exception as e:
        return Response(str(e), status=201, mimetype='application/json')

@app.route('/api/author/<string:id>', methods=['GET'])
def get_author(id):
    authors = Author.objects
    for author in authors:
        if(str(author.id) == id):
            return author.to_json()
    #Resource not found
    return {'error': 'No such author'}, 404 

#Update an Author
@app.route('/api/author/<string:id>', methods=['PUT'])
def update_author(id):
    current_author = None
    for author in Author.objects:
        if(str(author.id) == id): 
            current_author = author
    if current_author:
        record = json.loads(request.data)
        if(id == record['id']):
            try:
                if record['password']:
                    hashedPassword = bcrypt.hashpw(record['password'].encode('utf-8'), app.config['SALT'])
                    current_author.password = str(hashedPassword)
                if record['name']:
                    current_author.authorname = record['name']
                if record['email']:
                    current_author.email = record['email']
                if record['profilePicture']:
                    current_author.profilePicture = record['profilePicture']

                current_author.save()

                return current_author.to_json()
            except NotUniqueError as e:
                return {'error': f"An author with the name {record['name']} already exists"}, 401 
            except Exception as e:
                return Response(str(e), status=201, mimetype='application/json')
        else:
            return {'error': 'You can only update your own account.'}, 401
    else:
        #Resource not found
        return {'error': 'No such author'}, 404

##Delete an Author
@app.route('/api/author/<id>', methods=['DELETE'])
def delete_author(id):
    current_author = None
    for author in Author.objects:
        if(str(author.id) == id): 
            current_author = author
    if current_author:
        record = json.loads(request.data)
        if(id == record['id']):
            try:
                #find and delete authors posts
                try:
                    Post.objects(author=current_author).delete()
                    current_author.delete()
                    return current_author.to_json()
                except Exception as e:
                    return Response(str(e), status=201, mimetype='application/json')

            except Exception as e:
                return Response(str(e), status=201, mimetype='application/json')
        else:
            #Request/Access denied
            return {'error': 'You can only delete your own account.'}, 401
    else:
        #Resource not found
        return {'error': 'No such author'}, 404

#Create a new post
@app.route('/api/post', methods=['POST'])
def create_post():
    try:
        record = json.loads(request.data)

        #Save categories to the database
        for category in record['post categories']:
            try:
                new_category = Category(name=category)
                new_category.save()
            except NotUniqueError as e:
                pass
            except Exception as e:
                return {'Error in saving category': str(e)}

        post_categories = []
        for category in record['post categories']:
            post_categories.append(Category.objects(name=category).first())

        post_author = Author.objects(authorname=record['author name']).first()
        if post_author:
            new_post = Post(
                title = record['post title'],
                description = record['post description'],
                author = post_author,
                photo = record['post photo'],
                categories = post_categories
            )
            new_post.save()
            return new_post.to_json(), 200
        else:
            return {'error': f"An author with the name {record['author name']} does not exist"}, 401
    except NotUniqueError as e:
        return {'error': f"A Post with the title '{record['post title']}' or description '{record['post description']}' already exists"}, 401 
    except Exception as e:
         return Response(str(e), status=201, mimetype='application/json')     

""" #Get a single post
@app.route('/api/author/<string:id>', methods=['GET'])
def get_author(id):
    authors = Author.objects
    for author in authors:
        if(str(author.id) == id):
            return author.to_json()
    #Resource not found
    return {'error': 'No such author'}, 404 

#Update a Post
@app.route('/api/author/<string:id>', methods=['PUT'])
def update_author(id):
    current_author = None
    for author in Author.objects:
        if(str(author.id) == id): 
            current_author = author
    if current_author:
        record = json.loads(request.data)
        if(id == record['id']):
            try:
                if record['password']:
                    hashedPassword = bcrypt.hashpw(record['password'].encode('utf-8'), app.config['SALT'])
                    current_author.password = str(hashedPassword)
                if record['name']:
                    current_author.authorname = record['name']
                if record['email']:
                    current_author.email = record['email']
                if record['profilePicture']:
                    current_author.profilePicture = record['profilePicture']

                current_author.save()

                return current_author.to_json()
            except NotUniqueError as e:
                return {'error': f"An author with the name {record['name']} already exists"}, 401 
            except Exception as e:
                return Response(str(e), status=201, mimetype='application/json')
        else:
            return {'error': 'You can only update your own account.'}, 401
    else:
        #Resource not found
        return {'error': 'No such author'}, 404

##Delete a Post
@app.route('/api/author/<id>', methods=['DELETE'])
def delete_author(id):
    current_author = None
    for author in Author.objects:
        if(str(author.id) == id): 
            current_author = author
    if current_author:
        record = json.loads(request.data)
        if(id == record['id']):
            try:
                #find and delete authors posts
                try:
                    Post.objects(author=current_author).delete()
                    current_author.delete()
                    return current_author.to_json()
                except Exception as e:
                    return Response(str(e), status=201, mimetype='application/json')

            except Exception as e:
                return Response(str(e), status=201, mimetype='application/json')
        else:
            #Request/Access denied
            return {'error': 'You can only delete your own account.'}, 401
    else:
        #Resource not found
        return {'error': 'No such author'}, 404 """