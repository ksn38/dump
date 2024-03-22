import matplotlib.pyplot as plt
import matplotlib
import random
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.model_selection import cross_val_score, train_test_split

df = pd.read_csv('train_case2.csv', ';')
df.head(3)

train, X_test, y_train, y_test = train_test_split(df.drop('cardio', 1),
                                                    df['cardio'], random_state=0)

labels = np.array(y_train)[:4000]

# X_train = pd.read_csv('train.csv')
# X_train = X_train.drop('Id', axis=1)
#
# labels = np.array(X_train['choose'])
# X_train = X_train.drop('choose', axis=1)
# X_train = X_train.drop(['chemistry', 'biology', 'english', 'geography', 'history'], axis=1)
train = train.drop(['id'], axis=1)

X_train = np.array(train)[:4000, :]
shape_feat = X_train.shape[1]
print(X_train.shape)

X_ = X_train
# Для начала отмасштабируем выборку
rows, cols = X_.shape

# центрирование - вычитание из каждого значения среднего по столбцу
means = X_.mean(0)
for i in range(rows):

    for j in range(cols):
        X_[i, j] -= means[j]


# деление каждого значения на стандартное отклонение
std = np.std(X_, axis=0)
for i in range(cols):
    for j in range(rows):
        X_[j][i] /= std[i]

# Найдем собственные векторы и собственные значения (англ. Eigenvalues)
covariance_matrix = X_.T.dot(X_)
eig_values, eig_vectors = np.linalg.eig(covariance_matrix)
# сформируем список кортежей (собственное значение, собственный вектор)
eig_pairs = [(np.abs(eig_values[i]), eig_vectors[:, i]) for i in range(len(eig_values))]
# и отсортируем список по убыванию собственных значений
eig_pairs.sort(key=lambda x: x[0], reverse=True)
eig_sum = sum(eig_values)
# Доля дисперсии, описываемая каждой из компонент
var_exp = [(i / eig_sum) * 100 for i in sorted(eig_values, reverse=True)]
# Кумулятивная доля дисперсии по компонентам
cum_var_exp = np.cumsum(var_exp)
print('Кумулятивная доля дисперсии по компонентам', cum_var_exp[2])
# Сформируем вектор весов из собственных векторов, соответствующих первым двум главным компонентам
W = np.hstack((eig_pairs[0][1].reshape(shape_feat, 1), eig_pairs[1][1].reshape(shape_feat, 1), eig_pairs[2][1].reshape(shape_feat, 1)))
# print(f'Матрица весов W:\n', W)
Z = X_.dot(W)
y = labels

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

for c, i, s in zip("yk", [0, 1], [1, 1]):
    ax.scatter(Z[y == i, 0], Z[y == i, 1], Z[y == i, 2], c=c, s=s)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
