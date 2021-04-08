import tensorflow as tf
import numpy as np
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
import random 
import pickle as pkl

# Load Data
# x=[]
# for i in range(100):
#     x.append([random.randint(0,1),random.randint(0,1)])

filename = 'simulation_dataset.pkl'
with open(filename,'rb') as f:
	db = pkl.load(f)
print(db.head())
x = db.drop("label", axis=1)
y = db["label"]


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=True)


# X=tf.convert_to_tensor(x,dtype=np.float64)
# y = [(X[i][0]+X[i][1])%2 for i in range(100)]

# Change labels to +1 and -1 
# y = np.where(y==1, y, -1)
x_train=x_train.astype(np.float64)
x_test=x_test.astype(np.float64)
y_train = y_train.astype(np.float64)
y_test = y_test.astype(np.float64)

# Linear Model with L2 regularization
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(1, activation='linear', kernel_regularizer=tf.keras.regularizers.l2()))

# Hinge loss
def hinge_loss(y_true, y_pred):    
    return tf.maximum(0., 1- y_true*y_pred)

# Train the model
model.compile(optimizer='adam', loss=hinge_loss)
model.fit(x_train, y_train,  epochs=30)
# # Plot the learned decision boundary 
# x_min, x_max = X[:, 0].numpy().min() - 1, X[:, 0].numpy().max() + 1
# y_min, y_max = X[:, 1].numpy().min() - 1, X[:, 1].numpy().max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),np.arange(y_min, y_max, 0.01))
# Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
# Z = Z.reshape(xx.shape)
# cs = plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
# plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Set1)
# plt.show()