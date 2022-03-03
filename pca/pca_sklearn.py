import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

### Fit sklearn PCA (see docs for more details)
# Ref: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
pca = PCA(n_components=2)
pca.fit(X)

print(pca.explained_variance_ratio_)
print(pca.singular_values_)

### Fit sklearn PCA to Iris dataset
# Ref: https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
df = pd.read_csv(url, names=['sepal length','sepal width','petal length','petal width','target'])

features = ['sepal length', 'sepal width', 'petal length', 'petal width']

X = df.loc[:, features].values
y = df.loc[:, ['target']].values

# Standardize the data to scale features to optimise performance (ensure features have same scscale)
# Note: with train/test sets, you would .fit() the StandardScaler on the training data,
# then transform both the train and test sets with the fitted StandardScaler (using .transform())
X_stand = StandardScaler().fit_transform(X)

# Get top 2 principal components (i.e. main dimensions of variation)
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_stand)
principal_df = pd.DataFrame(
	data=principal_components,
	columns=['principal component 1', 'principal component 2']
)
final_df = pd.concat([principal_df, df[['target']]], axis = 1)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = final_df['target'] == target
    ax.scatter(final_df.loc[indicesToKeep, 'principal component 1']
               , final_df.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()
# plt.show()
print(f'Explained variance: {pca.explained_variance_ratio_}')


