from flask import Flask, render_template, request, redirect, url_for,jsonify
import json
from pymongo import MongoClient


app = Flask(__name__)

# Create a new MongoClient and database
client = MongoClient('127.0.0.1:27017')
db = client['ProteinStructure']

# Get the collections
structure_col = db['Structure']
chain_col = db['Chain']
experimental_col = db['Experimental']

@app.route('/data')
def get_data():
    cursor1 = structure_col.find()
    data1 = [document for document in cursor1]
    cursor2 = chain_col.find()
    data2 = [document for document in cursor2]
    cursor3 = experimental_col.find()
    data3 = [document for document in cursor3]
    return render_template('home.html', data1=data1, data2=data2, data3=data3)

@app.route('/process_query', methods=['POST'])
def process_query():
    try:
        collection_name = request.form['collection']
        query_type = request.form['query_type'].lower()
        query_str = request.form['query']
        query = json.loads(query_str)

        if collection_name == 'Structure':
            collection = structure_col
        elif collection_name == 'Chain':
            collection = chain_col
        elif collection_name == 'Experimental':
            collection = experimental_col
        else:
            return render_template('result.html', query_type=query_type, query=query, data=[])

        if query_type == 'find':
            cursor = collection.find(query)
            data = [document for document in cursor]
        elif query_type == 'insert':
            result = collection.insert_one(query)
            data = [{'inserted_id': str(result.inserted_id)}]
        elif query_type == 'update':
            result = collection.update_one(query['filter'], query['update'])
            data = [{'matched_count': result.matched_count, 'modified_count': result.modified_count}]
        elif query_type == 'delete':
            result = collection.delete_one(query)
            data = [{'deleted_count': result.deleted_count}]
        elif query_type == 'aggregate':
             cursor = collection.aggregate(query)
             data = [document for document in cursor]
        else:
            data = []

        return render_template('result.html', query_type=query_type, query=query, data=data)
    except Exception as e:
        return render_template('error.html')




# ...

# @app.route('/result')
# def show_result():
#     data = request.args.get('data')
#     print(data)  # Add this line to check the value of data
#     result_list = data.split(',') if data else []
#     return render_template('result.html', data=result_list)

@app.route('/result')
def show_result():
    data = request.args.get('data')
    result_list = data.split(',') if data else []
    return render_template('result.html', data=json.dumps(data))




# ...


if __name__ == '__main__':
    app.run(debug=True)