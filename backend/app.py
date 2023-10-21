from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Soni%40O2003@localhost/webapplication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class Product(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100))
      description = db.Column(db.String(255))
      isDeleted = db.Column(db.Boolean, default=False)
      creationDate = db.Column(db.DateTime, default = datetime.now)
      creatorUser = db.Column(db.String(255), db.ForeignKey('user.login'), nullable=False)
      imageUrl = db.Column(db.String(255))
      categoryId = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
      categoryRel = db.relationship('Category', backref='products')
      userRel = db.relationship('User', backref='products')


      #idcategory???

            
class Comment(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      productId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
      description = db.Column(db.String(255))
      creationDate = db.Column(db.DateTime, default = datetime.now)
      isDeleted = db.Column(db.Boolean, default=False)
      creatorUserId = db.Column(db.String(255))
    
class Category(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100))
      productRel = db.relationship('Product', backref='category', lazy=True)
      #idproduct????

class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     login = db.Column(db.String(255))
     password = db.Column(db.String(255))
     role = db.Column(db.Integer)
     productRel = db.relationship('Product', backref='user', lazy=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

product_schema = ProductSchema()
product_schema_many = ProductSchema(many=True)

user_schema = UserSchema()
user_schema_many = UserSchema(many=True)

category_schema = CategorySchema()
category_schema_many = CategorySchema(many=True)

comment_schema = CommentSchema()
comment_schema_many = CommentSchema(many=True)

@app.route('/get', methods = ['GET'])
def get_products():
        all_products = Product.query.all()
        products_results = product_schema_many.dump(all_products)
        return jsonify(products_results)

@app.route('/add', methods = ['POST'])
def add_product():
      title = request.json['title']
      description = request.json['description']
      #isDeleted = request.json['isDeleted']
      creatorUser = request.json['creatorUser']
      imageUrl = request.json['imageUrl']
      categoryId = request.json['categoryId']


      new_product = Product(
        title=title,
        description=description,
        creatorUser=creatorUser,
        imageUrl=imageUrl,
        categoryId=categoryId
    )
      db.session.add(new_product)
      db.session.commit()
      return product_schema.jsonify(new_product)

@app.route('/update/<id>/', methods = ['PUT'])
def update_product(id):
      product = Product.query.get(id)

      title = request.json['title']
      description = request.json['description']
      #isDeleted = request.json['isDeleted']
      creatorUser = request.json['creatorUser']
      imageUrl = request.json['imageUrl']    
     
      product.title = title
      product.description = description
      product.creatorUser = creatorUser
      product.imageUrl = imageUrl

      db.session.commit()
      return product_schema.jsonify(product)

@app.route('/delete/<id>/', methods = ['DELETE'])
def delete_product(id):
     product = Product.query.get(id)
     db.session.delete(product)
     db.session.commit()

     return product_schema.jsonify(product)


@app.route('/getuser', methods = ['GET'])
def get_users():
        all_users = User.query.all()
        users_results = user_schema_many.dump(all_users)
        return jsonify(users_results)

@app.route('/adduser', methods = ['POST'])
def add_user():
      login = request.json['login']
      password = request.json['password']
      role = request.json['role']
      #id = request.json['id']

      new_user = User(
        login=login,
        password=password,
        role=role,
        #id=id
    )
      db.session.add(new_user)
      db.session.commit()
      return product_schema.jsonify(new_user)

@app.route('/updateuser/<id>/', methods = ['PUT'])
def update_user(id):
      user = User.query.get(id)

      login = request.json['login']
      password = request.json['password']
      role = request.json['role']    
     
      user.login = login
      user.password = password
      user.role = role

      db.session.commit()
      return user_schema.jsonify(user)

@app.route('/deleteuser/<id>/', methods = ['DELETE'])
def delete_user(id):
     user = User.query.get(id)
     db.session.delete(user)
     db.session.commit()

     return user_schema.jsonify(user)


@app.route('/getcategory', methods = ['GET'])
def get_categories():
        all_categories = Category.query.all()
        categories_results = categories_schema_many.dump(all_categories)
        return jsonify(categories_results)

@app.route('/addcategory', methods = ['POST'])
def add_category():
      #id = request.json['id']
      name = request.json['name']

      new_category = Category(
        #id=id,
        name=name
    )
      db.session.add(new_category)
      db.session.commit()
      return category_schema.jsonify(new_category)

@app.route('/updatecategory/<id>/', methods = ['PUT'])
def update_category(id):
      category = Category.query.get(id)

      #id = request.json['id']
      name = request.json['name'] 
     
      #category.id = id
      category.name = name

      db.session.commit()
      return category_schema.jsonify(category)

@app.route('/deletecategory/<id>/', methods = ['DELETE'])
def delete_category(id):
     category = Category.query.get(id)
     db.session.delete(category)
     db.session.commit()

     return category_schema.jsonify(category)



@app.route('/getcomment', methods = ['GET'])
def get_comments():
        all_comments = Comment.query.all()
        comments_results = comment_schema_many.dump(all_comments)
        return jsonify(comments_results)

@app.route('/addcomment', methods = ['POST'])
def add_comments():
      #id = request.json['id']
      productId = request.json['productId']
      description = request.json['description']
      isDeleted = request.json['isDeleted']
      creatorUserId = request.json['creatorUserId']

      new_comment = Comment(
        productId=productId,
        description=description,
        creatorUseIdr=creatorUserId,
        isDeleted=isDeleted
    )
      db.session.add(new_comment)
      db.session.commit()
      return comment_schema.jsonify(new_comment)

@app.route('/updatecomment/<id>/', methods = ['PUT'])
def update_comment(id):
      comment = Comment.query.get(id)

      #id = request.json['id']
      productId = request.json['productId']
      description = request.json['description']
      isDeleted = request.json['isDeleted']
      creatorUserId = request.json['creatorUserId']
     
      comment.productId=productId,
      comment.description=description,
      comment.creatorUseIdr=creatorUserId,
      comment.isDeleted=isDeleted

      db.session.commit()
      return comment_schema.jsonify(comment)

@app.route('/deletecomment/<id>/', methods = ['DELETE'])
def delete_comment(id):
     comment = Comment.query.get(id)
     db.session.delete(comment)
     db.session.commit()

     return comment_schema.jsonify(comment)




if __name__ == "__main__":
    # Utwórz kontekst aplikacji przed utworzeniem bazy danych
    with app.app_context():
        # Tworzenie bazy danych
        db.create_all()

    app.run(debug=True, port=5000)