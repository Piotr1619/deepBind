'''
author = @pg
Sun 3 April 2022

Predict In One Go - the program allows you to:
- convert aa sequence into SMILES
- calculate Molecular fingerprints
- use the built model to fit the input into it and give prediction values (in pKd units)
'''

import pandas as pd
from rdkit import Chem
import subprocess
import os
import pickle

input = pd.read_excel('inputDataToPredict_name_aa.xlsx')
input_name = input.Name
input_aa = input['Amino Acid Sequence']

smiles_array = []
for i in input_aa:
    smiles_string = Chem.MolToSmiles(Chem.MolFromFASTA(i))
    smiles_array.append(smiles_string)

Smiles = pd.Series(smiles_array, name='SMILES')

df_smiles = pd.concat([input_name, Smiles], axis=1)
df_smiles.to_excel('inputDataToPredict_name_smiles.xlsx')

'''
CALCULATE MOLECULAR DESCRIPTORS
'''
# TO PREDICT
selection = ['SMILES','Name']
df_selection = df_smiles[selection]
df_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
os.remove('molecule.smi')

# Read output file
dataset_to_predict= pd.read_csv('descriptors_output.csv')
# Save it
dataset_to_predict.to_excel('descriptors_input_to_predict.xlsx')


'''
LOADING MODEL
'''
dataset_to_predict = pd.read_excel('descriptors_input_to_predict.xlsx')
# Reads in saved regression model
load_model = pickle.load(open('CollagenBindingProteins_ExtraTrees_model.pkl', 'rb'))

# Upload input data for prediction
data_for_predict = pd.read_excel('descriptors_input_for_model.xlsx')
X = data_for_predict.drop(['pKd'], axis=1)
Y = data_for_predict.pKd

load_model.fit(X,Y)
input_data = dataset_to_predict.drop(['Name'], axis=1)
# Apply model to make predictions
prediction = load_model.predict(input_data)
molecule_name = dataset_to_predict['Name']
prediction_output = pd.Series(prediction, name='pKd')
df = pd.concat([molecule_name, prediction_output], axis=1)
print('These are predicted pKd values')
print(df)
df.to_excel('prediction_output_data.xlsx')
