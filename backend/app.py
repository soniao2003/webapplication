from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''Soni@O2003''@localhost/webapplication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100))
      description = db.Column(db.String(255))
      isDeleted = db.Column(db.Boolean, default=False)
      creationDate = db.Column(db.DateTime, default = datetime.datetime.now)
      creatorUserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
      imageUrl = db.Column(db.String(255))
      #idcategory???

class Comment(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      productId = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
      description = db.Column(db.String(255))
      creationDate = db.Column(db.DateTime, default = datetime.datetime.now)
      isDeleted = db.Column(db.Boolean, default=False)
      creatorUserId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

      class Category(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(100))
            #idproduct????

@app.route('/bla', methods = ['GET'])
def get_products():
        return jsonify({"hello":"World"})

if __name__ == "__main__":
    app.run(debug=True)