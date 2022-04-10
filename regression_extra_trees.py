import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesRegressor
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

# import sklearn.ensemble as Regressor
# function_name = 'ExtraTreesRegressor'

df = pd.read_excel('descriptors_pKd_20proteins_data.xlsx')
X = df.drop('pKd', axis=1)
Y = df.pKd

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2)

# model  = eval("Regressor." + function_name + "(n_estimators = 100)")
model = ExtraTreesRegressor(n_estimators = 100)
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

pickle.dump(model, open('CollagenBindingProteins_ExtraTrees_model.pkl', 'wb'))
