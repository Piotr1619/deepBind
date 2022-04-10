'''
author = @pg
Sun 3 April 2022

Fingerprint calculator - generates a binary structure fingerprint for chemical structure of your interest.

input - your protein in SMILES string format
output -  ~880 length binary code/ protein
'''
import pandas as pd
import subprocess
import os


# Upload SMILES strings of the proteins of interest:
df = pd.read_excel('proteinToPredict_name_smiles.xlsx')
selection = ['Smiles','Name']
df_selection = df[selection]
df_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
os.remove('molecule.smi')

# Read output file
dataset= pd.read_csv('descriptors_output.csv')
# Save it
dataset.to_excel('descriptors_input_to_predict.xlsx')
