from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request



app = Flask(__name__)

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
    if not request.json or not 'name' in request.json:
        abort(400)
    product = {
        'id': products[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'count': request.json['count']
    }
    products.append(product)
    return jsonify({'product': product}), 201

@app.route('/products/<int:prod_id>', methods=['PUT'])
def update_task(prod_id):
    product = [product for product in products if product['id'] == prod_id]
    if len(product) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #if 'name' in request.json and type(request.json['name']) != json:
        #abort(400)
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