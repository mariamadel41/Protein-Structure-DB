import pymongo
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint
import csv
import re
from bson.code import Code
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
#     db.Structure.update_one({"structureId": chain["structufrom pymongo import ConnectionreId"]}, {"$push": {"chainId": chain["_id"]}})
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
#print("Find all documents in Structure collection where classidfication is \"DNA-RNA HYBRID" :" ,'\n')
# for document in cursor:
#     pprint(document)
#     print('\n')

# cursor2 = chain_col.find({"chainId": "H"})
#print("Find all documents in Chain collection where chainId is \"H" : ",  '\n')
# for document in cursor2:
#     pprint(document)
#     print('\n')


# cursor3 = experimental_col.find({"resolution": {"$gt" : 2.0}})
#print("Find all documents in Experimental collection where resolution is greater than 2 :" , '\n')
# for document in cursor3:
#     pprint(document)
#     print('\n')

# cursor4 = structure_col.find({"residueCount": {"$gte" : 300}})
#print("Find all documents in Structure collection where residueCount is greater than or equal 300 : " ,'\n')
# for document in cursor4:
#     pprint(document)
#     print('\n')

# cursor5 = structure_col.find({"$and" : [ {"macromoleculeType" : "DNA"} , {"residueCount": {"$lt" : 50}}]})
#print("Find all documents in Structure collection where macromoleculeType is \"DNA" and residueCount is less than  or equal 50 :" , '\n')
# for document in cursor5:
#     pprint(document)
#     print('\n')

# cursor6 = structure_col.find({"publicationYear": {"$gte" : 2001}})
# print("Find all documents in Structure collection where residueCount is greater than or equal 300 : " , '\n')
# for document in cursor6:
#     pprint(document)
#     print('\n')

#Mongodb Projection (inclusion and exclusion) 
# cursor7 = structure_col.find(
#     {"publicationYear": {"$gte": 2005}} ,
#      {"structureId": 0, "densityPercentSol": 0} 
# )
# print("Find all documents in Structure collection where publicationYear is greater than or equal 2005 without display structureId and densityPercentSol: ", '\n')
# for document in cursor7:
#     pprint(document)
#     print('\n')

# cursor8 = experimental_col.find(
#     {"resolution": {"$gt": 2.3}} ,
#      {"experimentalTechnique": 1,"_id" : 0 } 
# )
# print("Find all documents in expiremental collection where resolution is greater 2.3 just display experimentalTechnique: ", '\n')
# for document in cursor8:
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

# #distinct:
# d = structure_col.distinct("classification")
# print("Classification Types:\n")
# count1=0
# for i in d:
#     pprint(i)
#     count1 +=1
# print('\n')
# print("There are", count1, "classes.\n")


# d2 = experimental_col.distinct("experimentalTechnique")
# print("ExperimentalTechnique Types:\n")
# count2 =0 
# for i in d2:
#     pprint(i)
#     count2 +=1
# print('\n')
# print("There are", count2, "ExperimentalTechniques.\n")

# d3 = experimental_col.distinct("crystallizationMethod")
# print("crystallizationMethod Types:\n")
# count3 =0 
# for i in d3:
#     pprint(i)
#     count3 +=1
# print('\n')
# print("There are", count3, "crystallizationMethod.\n")

# d4 = structure_col.distinct("macromoleculeType")
# print("MacromoleculeType :\n")
# count4 =0 
# for i in d4:
#     pprint(i)
#     count4 +=1
# print('\n')
# print("There are", count4, "macromoleculeTypes.\n")

# d5 = structure_col.aggregate( [{"$match" :{"macromoleculeType":"Protein#DNA"} }]) 
# print ("Find The Structure document with macromoleculeType is Protein#DNA : " )
# for i in d5:
#     pprint(i)   
# print('\n') 

# d6 = structure_col.aggregate( [{"$match" :{"macromoleculeType":"DNA#DNA/RNA Hybrid"} } ,{"$sort":{"publicationYear":1}}]) 
# print ("Find The Structure document with macromoleculeType is DNA#DNA/RNA Hybrid sorted ascending with piblication year : " )
# for i in d6:
#     pprint(i)   
# print('\n')


# d7 = experimental_col.aggregate( [{"$match" :{"crystallizationMethod":"VAPOR DIFFUSION"} } ,{"$sort":{"resolution":-1 , "_id" : 1}}]) 
# print ("Find The Experimental document with crystallizationMethod is VAPOR DIFFUSION sorted decending with resolution and _id ascending for uniqeness : " )
# for i in d7:
#     pprint(i)   
# print('\n')

# d7 = structure_col.aggregate([
#     {"$match": {"macromoleculeType": "Protein"}},
#     {"$group": {"_id": "$classification", "AvgpH": {"$avg": "$phValue"}}},
#     {"$sort": {"AvgGpa": 1, "_id": 1}}
# ])

# print("Find the average of phValue for the protein macromoleculeType : ")
# for i in d7:
#     pprint(i)
# print('\n')


# d8 = structure_col.aggregate([
#     {"$match": {"macromoleculeType": "Protein"}},
#     {"$group": {"_id": "$classification", "AvgpH": {"$avg": "$residueCount"}}},
#     {"$sort": {"AvgGpa": 1, "_id": 1}}
# ])

# print("Find the average of residueCount for the protein macromoleculeType : ")
# for i in d8:
#     pprint(i)
# print('\n')

 
# #Reference relation:
# document = structure_col.find_one({"_id": 3})
# print ("The Chain document detail with Structure document id equal 3 : " )
# if document:
#     chain_id = document["chainId"]

#     # Use the chainId to find matching documents in the chain collection
#     address_documents = chain_col.find({"_id": {"$in": chain_id}})
#     for doc in address_documents:
#         pprint(doc)
# else:
#     print("No document found with structure _id equal to 3")

# document2 = structure_col.find_one({"classification": "HYDROLASE(O-GLYCOSYL)"})
# print ("The Chain document detail with Structure document classification is HYDROLASE(O-GLYCOSYL) : " )
# if document2:
#     chain_id = document2["chainId"]
#     address_documents2 = chain_col.find({"_id": {"$in": chain_id}})
#     for doc in address_documents2:
#         pprint(doc)
# else:
#     print("No document found with this chainId!")

# document3 = structure_col.find_one({"structureMolecularWeight": 18030.63 })
# print ("The Chain document detail with Structure document classification is 18030.63 : " )
# if document3:
#     chain_id = document3["chainId"]
#     address_documents3 = chain_col.find({"_id": {"$in": chain_id}})
#     for doc in address_documents3:
#         pprint(doc)
# else:
#     print("No document found with this chainId!")


#indexing:
# print("Display Structure collection according to residueCount index descending: ")
# ind1 = structure_col.create_index([("residueCount", pymongo.DESCENDING)])

# for doc in structure_col.find().hint(ind1):
#     pprint(doc)


# print("Display Structure collection according to publication year  index ascending: ")
# ind2 = structure_col.create_index([("publicationYear", pymongo.ASCENDING),("residueCount" , pymongo.DESCENDING)])
# for doc in structure_col.find().hint(ind2):
#     pprint(doc)

# print("Display experimental collection according to resolution year  index descending: ")
# ind3 = experimental_col.create_index([("resolution", pymongo.DESCENDING)])
# for doc in experimental_col.find().hint(ind3):
#     pprint(doc)