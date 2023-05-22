import pandas as pd
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint
import csv
import re
# # shrink csv files to 5000 records:
# dups_df = pd.read_csv('data//dups.csv').head(5000)
# seq_df = pd.read_csv('data//seq.csv').head(12000)
# dups_df.to_csv('data//dups_updated.csv', index=False)
# seq_df.to_csv('data//seq_updated.csv', index=False)

# dups_df = pd.read_csv('data//dups_updated.csv')
# seq_df = pd.read_csv('data//seq_updated.csv')


# Create a new MongoClient and database
client = MongoClient('127.0.0.1:27017')

db = client['ProteinStructure']

# Create the three collections
structure_col = db['Structure']
chain_col = db['Chain']
experimental_col = db['Experimental']



# # Loop through the rows of dups_df and insert each row as a document in the structure_col collection
# for index, row in dups_df.iterrows():
#     document = {
#         '_id': index + 1,  # add 1 to index to start _id values from 1
#         'structureId': row['structureId'],
#         'classification': row['classification'],
#         'macromoleculeType': row['macromoleculeType'],
#         'residueCount': row['residueCount'],
#         'structureMolecularWeight': row['structureMolecularWeight'],
#         'densityMatthews': row['densityMatthews'],
#         'densityPercentSol': row['densityPercentSol'],
#         'pdbxDetails': row['pdbxDetails'],
#         'phValue': row['phValue'],
#         'publicationYear': row['publicationYear'] 
#     }
#     try:
#         structure_col.insert_one(document)
#     except DuplicateKeyError:
#         pass  # ignore duplicate key errors

# # Loop through the rows of seq_df and insert each row as a document in the chain_col collection
# for index, row in seq_df.iterrows():
#     document = {
#         '_id': index + 1,  # add 1 to index to start _id values from 1
#         'structureId': row['structureId'],
#         'chainId': row['chainId'],
#         'sequence': row['sequence']
#     }
#     try:
#         chain_col.insert_one(document)
#     except DuplicateKeyError:
#         pass  # ignore duplicate key errors

# # Loop through the rows of dups_df again and insert each row as a document in the experimental_col collection
# for index, row in dups_df.iterrows():
#     document = {
#         '_id': index,
#         'structureId': row['structureId'],
#         'experimentalTechnique': row['experimentalTechnique'],
#         'resolution': row['resolution'],
#         'crystallizationMethod': row['crystallizationMethod'],
#         'crystallizationTempK': row['crystallizationTempK']
#     }
#     experimental_col.insert_one(document)


# # Update the Structure collection with chainId to make (Reference Relation)
# updated_count = db.Structure.update_many({}, {"$set": {"chainId": []}}).modified_count
# print(f"Updated {updated_count} documents in Structure collection with empty chainId")
# # Iterate over the Chain collection and add the chainId to the corresponding Structure documents
# count = 0
# for chain in db.Chain.find():
#     db.Structure.update_one({"structureId": chain["structureId"]}, {"$push": {"chainId": chain["_id"]}})
#     count += 1
#     print(f"Iteration {count} completed")


# # Save the three collections as csv files
# structure_df = pd.DataFrame(list(structure_col.find()))
# structure_df.to_csv('data//structure.csv', index=False)

# chain_df = pd.DataFrame(list(chain_col.find()))
# chain_df.to_csv('data//chain.csv', index=False)

# experimental_df = pd.DataFrame(list(experimental_col.find()))
# experimental_df.to_csv('data//experemintal.csv', index=False)


# #Find Query:
# cursor = structure_col.find({"classification": "DNA-RNA HYBRID"})
# for document in cursor:
#     pprint(document)
#     print('\n')

# cursor2 = chain_col.find({"chainId": "H"})
# for document in cursor2:
#     pprint(document)
#     print('\n')


# cursor3 = experimental_col.find({"resolution": {"$gt" : 2.0}})
# for document in cursor3:
#     pprint(document)
#     print('\n')

# cursor4 = structure_col.find({"residueCount": {"$gte" : 300}})
# for document in cursor4:
#     pprint(document)
#     print('\n')

# cursor5 = structure_col.find({"$and" : [ {"macromoleculeType" : "DNA"} , {"residueCount": {"$lt" : 50}}]})
# for document in cursor5:
#     pprint(document)
#     print('\n')


# # Updating the records
# result = experimental_col.update_many(
#     {"crystallizationMethod": {"$regex": re.compile(r'^\s*$', re.IGNORECASE)}},
#     {"$set": {"crystallizationMethod": "nan"}}
# )

# print(f"Number of documents matched: {result.matched_count}")
# print(f"Number of documents updated: {result.modified_count}")

# # Retrieve documents from the collection
# documents = list(experimental_col.find())

# # Define the fieldnames for the CSV file
# fieldnames = ['_id', 'structureId', 'experimentalTechnique', 'resolution', 'crystallizationMethod', 'crystallizationTempK']

# # Save documents to a CSV file
# with open('/home/mariam/Downloads/Protein/data/experemintal.csv', 'w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(documents)

# print("Collection saved to experimental.csv successfully.")


# # Delete the pdbxDetails field from all documents on Structure collection
# structure_col.update_many({}, {"$unset": {"pdbxDetails": ""}})
# print("pdbxDetails field deleted from all documents in the structure collection.")
# structure_deleted_df = pd.DataFrame(list(structure_col.find()))
# structure_deleted_df.to_csv('data//structure_after_delete.csv', index=False)

#Aggregation Queries

#distinct:
d = structure_col.distinct("classification")
print("Classification Types:\n")
count1=0
for i in d:
    pprint(i)
    count1 +=1
print('\n')
print("There are", count1, "classes.\n")


d2 = experimental_col.distinct("experimentalTechnique")
print("ExperimentalTechnique Types:\n")
count2 =0 
for i in d2:
    pprint(i)
    count2 +=1
print('\n')
print("There are", count2, "ExperimentalTechniques.\n")

