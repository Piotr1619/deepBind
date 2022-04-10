'''
author = @pg

Wed 6 Apr 2022

This is a program for building model for given input dataset.
The regressor is chosen from the top list of training predictions.
'''

import pandas as pd
from rdkit import Chem
import subprocess
import os
import pickle
from sklearn.model_selection import train_test_split
import lazypredict
from lazypredict.Supervised import LazyRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Type a name of your file here:
input = pd.read_excel('inputDataForModel_name_aa_Kd2.xlsx')
input_name = input.Name
input_aa = input['Amino Acid Sequence']

smiles_array = []
for i in input_aa:
    smiles_string = Chem.MolToSmiles(Chem.MolFromFASTA(i))
    smiles_array.append(smiles_string)

Smiles = pd.Series(smiles_array, name='SMILES')

df_smiles = pd.concat([input_name, Smiles], axis=1)
df_smiles.to_excel('inputDataForModel_name_smiles.xlsx')
# df_smiles.to_excel('test2.xlsx')
print('Update: AA seaquences transformed in SMILES string format')
print('Update: SMILES strings saved in the file \'inputDataForModel_name_smiles.xlsx\'')
'''
CALCULATE MOLECULAR DESCRIPTORS
'''
# TO PREDICT

selection = ['SMILES','Name']
df_selection = df_smiles[selection]
df_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)
print('Calculating MFPs. Please wait...')
bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
os.remove('molecule.smi')
output= pd.read_csv('descriptors_output.csv')

# Read output file
descriptor_output= pd.read_csv('descriptors_output.csv')
os.remove('descriptors_output.csv')
# Save it
descriptor_output.to_excel('descriptors_input_for_model.xlsx')
print('Update: MFPs calculated. Saved in file \'descriptors_input_for_model.xlsx\'')

'''
COMPARE THE PERFOMANCE OF ALL MODELS
'''
df = pd.read_excel('inputDataForModel_name_aa_Kd.xlsx') # Used to extract Kd values
X = pd.read_excel('descriptors_input_for_model.xlsx') # fingerprints
df_Kd = df.Kd
pKd = []

for kd in df_Kd:
    molar = kd*(10**-9) # Converts nM to M
    pKd.append(-np.log10(molar))

Y = pKd

# Perform data splittin using 80/20 ratio
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=42)

# Defines and build the lazyclassifier
clf = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
models_train, predictions_train = clf.fit(X_train,X_train,Y_train,Y_train)
models_test, predictions_test = clf.fit(X_train,X_test,Y_train,Y_test)

print('Performance table of the training set (80% subset)')
print(predictions_train)

print('Performance table of the test set (20% subset)')
print(predictions_test)

function_name =predictions_train.index[0] # Choose the best model out of the ranking
print(function_name, ' has been chosen as the best model.')

'''
BUILD A MODEL
'''
# IMPORT ALL LIBRARIES
import sklearn.ensemble as Regressor

df = pd.read_excel('inputDataForModel_name_aa_Kd.xlsx') # Used to extract Kd values
X = pd.read_excel('descriptors_input_for_model.xlsx') # fingerprints
df_Kd = df.Kd
pKd = []
for kd in df_Kd:
    molar = kd*(10**-9) # Converts nM to M
    pKd.append(-np.log10(molar))
Y = pKd

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2)

model  = eval("Regressor." + function_name + "(n_estimators = 100)")
model.fit(X_train, Y_train)
r2 = model.score(X_test, Y_test)
print('This is R2:')
print(r2)
Y_pred = model.predict(X_test)
sns.set(color_codes=True)
sns.set_style('white')
ax  = sns.regplot(Y_test, Y_pred, scatter_kws={'alpha':0.4})
ax.set_xlabel('Experimental pKd', fontsize='large', fontweight='bold')
ax.set_ylabel('Predicted pKd', fontsize='large', fontweight='bold')
plt.show()

pickle.dump(model, open('CollagenBindingProteins_model.pkl', 'wb'))
