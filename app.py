from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

UPLOAD_FOLDER = 'V:\Flask_Python POC'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

products = [
    {
        'id': 1,
        'name': 'Shirt',
        'description': 'Cotton shirt of size M', 
        'count': 5
    },
    {
        'id': 2,
        'name': 'Headphones',
        'description': 'Boat Headphones of Black colour', 
        'count': 6
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/products', methods=['GET'])
def get_tasks():
    return jsonify({'products': products})

@app.route('/products/<int:prod_id>', methods=['GET'])
def get_task(prod_id):
    product = [product for product in products if product['id'] == prod_id]
    if len(product) == 0:
        abort(404)
    return jsonify({'product': product[0]})


@app.route('/products', methods=['POST'])
def create_task():
   
    name1=request.form.get("name")
    description1= request.form.get("description")
    count1= request.form.get("count")
    id1= products[-1]['id'] + 1,
    print(name1)
    product = {
        'id': products[-1]['id'] + 1,
        'name': name1,
        'description': description1,
        'count': count1
    }
    image=request.files['image']
    filename=str(id1)+name1
    #filename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    products.append(product)
    return jsonify({'product': product}), 201

@app.route('/products/<int:prod_id>', methods=['PUT'])
def update_task(prod_id):
    product = [product for product in products if product['id'] == prod_id]
    if len(product) == 0:
        abort(404)
    if not request.json:
        abort(400)
    
    product[0]['name'] = request.json.get('name', product[0]['name'])
    product[0]['description'] = request.json.get('description', product[0]['description'])
    product[0]['count'] = request.json.get('count', product[0]['count'])
    
    return jsonify({'product': product[0]})

@app.route('/products/<int:prod_id>', methods=['DELETE'])
def delete_task(prod_id):
    product = [product for product in products if product['id'] == prod_id]
    if len(product) == 0:
        abort(404)
    products.remove(product[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)