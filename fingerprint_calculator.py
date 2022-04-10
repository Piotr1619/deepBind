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
df = pd.read_excel('abc.xlsx')
selection = ['Smiles','Name']
# df = pd.read_excel('abcd.xlsx')
# selection = ['canonical_smiles','molecule_chembl_id']
df_selection = df[selection]
df_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
os.remove('molecule.smi')

# Read output file
df2 = pd.read_csv('descriptors_output.csv')
df2_X = df2.drop(columns=['Name'])
df2_Y = df['pKd']

#Combine fingerprint and pKd together
dataset = pd.concat([df2_X,df2_Y], axis=1)
# Save it
dataset.to_excel('CollagenBindingProteins_data_pKd_PubChem_fp.xlsx')
