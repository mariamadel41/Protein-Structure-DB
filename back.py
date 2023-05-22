from flask import Flask, render_template, request
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

@app.route('/result', methods=['GET'])
def process_query():
    try:
        collection_name = request.args.get('collection')
        query_type = request.args.get('query_type').lower()
        query_str = request.args.get('query')
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
            conditions = [query]
            sub_condition = {}  # Initialize sub_condition variable
            for sub_query in conditions:
                field = sub_query.get('field')
                value = sub_query.get('value')
                operator = sub_query.get('operator')

                if operator == 'equal':
                    sub_condition = {field: {'$eq': value}}
                elif operator == 'greater_than':
                    sub_condition = {field: {'$gt': value}}
                elif operator == 'greater_than_or_equal':
                    sub_condition = {field: {'$gte': value}}
                elif operator == 'less_than':
                    sub_condition = {field: {'$lt': value}}
                elif operator == 'less_than_or_equal':
                    sub_condition = {field: {'$lte': value}}
                elif operator == 'and':
                    sub_condition = {'$and': value}
                elif operator == 'or':
                    sub_condition = {'$or': value}

                conditions.append(sub_condition)

            query = {"$and": conditions}  # Use "$and" operator for combining conditions
            results = collection.find(query)
            data = '\n'.join([str(r) for r in results])
        elif query_type == 'insert':
            result = collection.insert_one(query)
            data = [{'inserted_id': str(result.inserted_id)}]
        elif query_type == 'update':
            result = collection.update_one(query['filter'], query['update'])
            data = [{'matched_count': result.matched_count, 'modified_count': result.modified_count}]
        elif query_type == 'index':
            index_fields = query['index_fields']
            index_order = query['index_order']
            index_name = collection.create_index([(index_fields, index_order)])
            data = [{'index_name': index_name}]

    # Fetch the collection with the new index
            cursor = collection.find().hint(index_name)
            data = [document for document in cursor]
        elif query_type == 'delete':
            result = collection.delete_one(query)
            data = [{'deleted_count': result.deleted_count}]
        elif query_type == 'aggregate':
             cursor = collection.aggregate(query)
             data = [document for document in cursor]
        else:
            data = [{"EMPTY RESULT"}]
        return render_template('result.html', query_type=query_type, query=query, data=data)
    except Exception as e:
        print(e)
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)