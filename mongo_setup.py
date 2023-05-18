# import pandas as pd
# from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError

# # shrink csv files to 5000 records:
# dups_df = pd.read_csv('data//dups.csv').head(5000)
# seq_df = pd.read_csv('data//seq.csv').head(12000)
# dups_df.to_csv('data//dups_updated.csv', index=False)
# seq_df.to_csv('data//seq_updated.csv', index=False)

# dups_df = pd.read_csv('data//dups_updated.csv')
# seq_df = pd.read_csv('data//seq_updated.csv')


# # Create a new MongoClient and database
# client = MongoClient('127.0.0.1:27017')

# db = client['ProteinStructure']

# # Create the three collections
# structure_col = db['Structure']
# chain_col = db['Chain']
# experimental_col = db['Experimental']

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


# # Update the Structure collection with chainId
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
