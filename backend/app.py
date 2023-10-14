from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/bla', methods = ['GET'])
def get_products():
        return jsonify({"hello":"World"})

if __name__ == "__main__":
    app.run(debug=True)