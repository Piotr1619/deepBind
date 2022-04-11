'''
author = @pg
Sun 3 Apr 2022

The script allows to predict values from the input in the form of molecular descriptors.
'''

import pandas as pd
import pickle
# Reads in saved regression model
load_model = pickle.load(open('CollagenBindingProteins_ExtraTrees_model.pkl', 'rb'))

# Upload input data to predict
data_to_predict = pd.read_excel('descriptors_input_to_predict.xlsx')
X = data_for_predict.drop(['pKd'], axis=1)
Y = data_for_predict.pKd

load_model.fit(X,Y)
input_data = data_to_predict.drop(['Name'], axis=1)
# Apply model to make predictions
prediction = load_model.predict(input_data)
molecule_name = data_to_predict['Name']
prediction_output = pd.Series(prediction, name='pKd')
df = pd.concat([molecule_name, prediction_output], axis=1)
print('These are predicted pKd values')
print(df)
df.to_excel('prediction_output.xlsx')
