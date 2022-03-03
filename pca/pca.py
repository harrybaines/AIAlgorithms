import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd

def pca(X, n_components):
	# Subtract mean of each variable from each value
	X_centered = X - np.mean(X, axis=0)
	
	# Calculate covariance matrix of mean-centered data
	cov_mat = np.cov(X_centered, rowvar=False)

	# Compute Eigenvalue and Eigenvectors of the covariance matrix
	eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)

	# Sort Eigenvalues in descending values
	sorted_index = np.argsort(eigen_values)[::-1]
	sorted_eigenvalue = eigen_values[sorted_index]
	sorted_eigenvectors = eigen_vectors[:, sorted_index]

	# Select the first n Eigenvectors (i.e. number of desired dimensions)
	eigenvector_subset = sorted_eigenvectors[:, 0:n_components]

	# Transform the original data
	X_reduced = np.dot(eigenvector_subset.transpose(), X_centered.transpose()).transpose()

	return X_reduced

if __name__ == "__main__":
	url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
	data = pd.read_csv(url, names=['sepal length','sepal width','petal length','petal width','target']) 

	X = data.iloc[:, 0:4]
	y = data.iloc[:, 4]
	mat_reduced = pca(X, 2)

	principal_df = pd.DataFrame(mat_reduced, columns = ['PC1','PC2'])
	principal_df = pd.concat([principal_df , pd.DataFrame(y)] , axis = 1)

	plt.figure(figsize = (6,6))
	sb.scatterplot(data = principal_df , x = 'PC1',y = 'PC2' , hue = 'target' , s = 60 , palette= 'icefire')
	plt.show()	
	
