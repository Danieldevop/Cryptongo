import pymongo
from flask import Flask, jsonify, request


def get_db_connection(uri):
    client = pymongo.MongoClient(uri)
    return client.cryptongo


app = Flask(__name__)
db_connection = get_db_connection('mongodb://localhost:27017/')


def get_documents():
    params = {}
    name = request.args.get('name', '')
    limit = int(request.args.get('limit', 0))
    if name:
        params.update({'name': name})
    cursor = db_connection.tickers.find(
        params, {'_id': 0, 'ticker_hash': 0}
    ).limit(limit)
    return list(cursor)


def get_top20():
    params = {}
    name = request.args.get('name', '')
    limit = int(request.args.get('limit', 0))
    if name:
        params.update({'name': name})
    params.update({'rank': {'$lte': 20}})
    cursor = db_connection.tickers.find(
        params, {'_id': 0, 'ticker_hash': 0}
    ).limit(limit)
    return list(cursor)


def remove_currency():
    params = {}
    name = request.args.get('name', '')
    if name:
        params.update({'name': name})
    else:
        return False
    return db_connection.tickers.delete_many(
        params
    ).deleted_count


def update_currency():
    params = {}
    symbol = request.args.get('symbol', '')
    if symbol:
        params.update({'symbol': symbol})
    else:
        return False
    return db_connection.tickers.update_one(params, {'$set': {'name': 'Daniel'}})


@app.route("/", methods=['GET'])
def index():
    return jsonify(
        {
            'name': "Cryptongo API"
        }
    )


@app.route('/tickers', methods=['GET', 'DELETE', 'POST'])
def tickers():
    if request.method == 'GET':
        return jsonify(get_documents())
    elif request.method == 'DELETE':
        result = remove_currency()
        if result > 0:
            return jsonify(
                {
                    'text': 'Documents DELETED'
                }
            ), 204
        else:
            return jsonify({
                'error': 'Document not Found'
            }), 404
    if request.method == 'POST':
        return jsonify(update_currency())


@app.route("/top20", methods=['GET'])
def top20():
    update_currency()
    return jsonify({
      'message': 'Document updated'
    })
