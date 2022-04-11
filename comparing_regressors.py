'''
author = @pg
Sun 3 Apr 2022

Comparing several ML algorithms for build regression models.
'''
import pandas as pd
from sklearn.model_selection import train_test_split
import lazypredict
from lazypredict.Supervised import LazyRegressor
import matplotlib.pyplot as plt
import seaborn as sns


# That's what should be - at the end
df = pd.read_excel('descriptors_input_to_predict.xlsx')
# df = pd.read_excel('descriptors_pKd_20proteins_data.xlsx')
X = df.drop('pKd', axis=1)
Y = df.pKd

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

my_goal =predictions_train.index[0]
print(type(my_goal))
