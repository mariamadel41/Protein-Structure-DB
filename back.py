from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/result')
def show_result():
    result = request.args.get('result')
    return render_template('result.html', result=result)


@app.route('/data', methods=['GET', 'POST'])
def get_data_route():
    if request.method == 'POST':
        # Get the submitted data from the form
        collection = request.form.get('collection')
        query_type = request.form.get('query_type')
        query = request.form.get('query')

        # Convert the query string to a JSON object
        query_object = json.loads(query)

        # Perform the query on the specified collection based on the query type
        if collection == 'Structure':
            if query_type == 'Find':
                result = structure_col.find(query_object)
            elif query_type == 'Insert':
                structure_col.insert_one(query_object)
                result = "Data inserted successfully"
            elif query_type == 'Update':
                # Update operation
                update_data = json.loads(request.form['update_data'])
                result = collection.update_many(query, {'$set': update_data})
                result = f'Updated {result.modified_count} documents'
            elif query_type == 'Delete':
                # delete operation
                result = collection.delete_many(query)
                result = f'Deleted {result.deleted_count} documents'
            else:
                result = None

        elif collection == 'Chain':
            if query_type == 'Find':
                result = chain_col.find(query_object)
            elif query_type == 'Insert':
                chain_col.insert_one(query_object)
                result = "Data inserted successfully"
            elif query_type == 'Update':
                # Update operation
                update_data = json.loads(request.form['update_data'])
                result = collection.update_many(query, {'$set': update_data})
                result = f'Updated {result.modified_count} documents'
            elif query_type == 'Delete':
                result = collection.delete_many(query)
                result = f'Deleted {result.deleted_count} documents'
            else:
                result = None

        elif collection == 'Experimental':
            if query_type == 'Find':
                result = experimental_col.find(query_object)
            elif query_type == 'Insert':
                experimental_col.insert_one(query_object)
                result = "Data inserted successfully"
            elif query_type == 'Update':
                # Update operation
                update_data = json.loads(request.form['update_data'])
                result = collection.update_many(query, {'$set': update_data})
                result = f'Updated {result.modified_count} documents'
            elif query_type == 'Delete':
                # delete operation
                result = collection.delete_many(query)
                result = f'Deleted {result.deleted_count} documents'
            else:
                result = None

        # Redirect to the result page after processing the form data
        return redirect(url_for('show_result', result=result))

    return render_template('result.html')


if __name__ == '__main__':
    app.run()