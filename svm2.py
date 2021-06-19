import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random 
import pickle as pkl

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.utils import shuffle
#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

filename = 'dataset_network_simulation_500.pkl'#'simulation_dataset_100.pkl' #'fb_simulation_dataset.pkl'
with open(filename,'rb') as f:
    db = pkl.load(f)

print(db)

x = db.drop("label", axis=1)
y = db["label"]

def make_meshgrid(x, y, h=.02):
    """Create a mesh of points to plot in

    Parameters
    ----------
    x: data to base x-axis meshgrid on
    y: data to base y-axis meshgrid on
    h: stepsize for meshgrid, optional

    Returns
    -------
    xx, yy : ndarray
    """
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy


def plot_contours(ax, clf, xx, yy, **params):
    """Plot the decision boundaries for a classifier.

    Parameters
    ----------
    ax: matplotlib axes object
    clf: a classifier
    xx: meshgrid ndarray
    yy: meshgrid ndarray
    params: dictionary of params to pass to contourf, optional
    """
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out



# Take the first two features. We could avoid this by using a two-dim dataset
# X = x.to_numpy()[:,[1,3]]
X = x.to_numpy()#[:,[1,3]]
y = y.to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# X, y = shuffle(X, y, random_state=0)

# we create an instance of SVM and fit out data. We do not scale our
# data since we want to plot the support vectors
C = 1  # SVM regularization parameter
models = (svm.SVC(kernel='linear', C=C),
          svm.SVC(kernel='rbf', gamma='auto', C=C),
          svm.SVC(kernel='poly', degree=2, gamma='auto', C=C),
          svm.SVC(kernel='poly', degree=3, gamma='auto', C=C))
# models = (clf.fit(X_train, y_train) for clf in models)

models_title = ['SVC with linear kernel']#,
          # 'SVC with RBF kernel',
          # 'SVC with polynomial (degree 2) kernel',
          # 'SVC with polynomial (degree 3) kernel']
# Cross Validation to select the best model
scoring = ['accuracy', 'precision','recall','f1']
scores = [cross_validate(clf, X_train, y_train, scoring=scoring) for clf in (models)]

for k in range (len(scores)):
    print(models_title[k] + '\n' + scores[k] + '\n')

# Results show that we get the best results with SVC with polynomial of degree 2 
# Training our data with the best model
model = svm.SVC(kernel='poly', degree=2, gamma='auto', C=C)
model.fit(X_train, y_train)

# Evaluating our model with the test set
evaluate_model(model)


def evaluate_model(model,X_test,y_pred):
    #Predict the response for test dataset
    y_pred = model.predict(X_test)

    # Model Accuracy: how often is the classifier correct?
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    # Model Precision
    print("Precision:",metrics.precision_score(y_test, y_pred))
    # Model Recall
    print("Recall:",metrics.recall_score(y_test, y_pred))
    # Model F1-Score
    print("F1-Score:",metrics.recall_score(y_test, y_pred))


def plot_svm(X_test,y_test):
    # title for the plots
    titles = ('SVC with linear kernel',
              'SVC with RBF kernel',
              'SVC with polynomial (degree 2) kernel',
              'SVC with polynomial (degree 3) kernel')

    # Set-up 2x2 grid for plotting.
    fig, sub = plt.subplots(2, 2)
    plt.subplots_adjust(wspace=0.4, hspace=0.4)

    X0, X1 = X_test[:, 0], X_test[:, 1]
    xx, yy = make_meshgrid(X0, X1)

    for clf, title, ax in zip(models, titles, sub.flatten()):
        plot_contours(ax, clf, xx, yy,
                      cmap=plt.cm.coolwarm, alpha=0.8)
        scatter = ax.scatter(X0, X1, c=y_test, cmap=plt.cm.coolwarm, s=20, edgecolors='k')#labels={1:'True', '0':False}
        legend1 = ax.legend(*scatter.legend_elements(),
                        loc="upper right", title="Classes" )
        ax.add_artist(legend1)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xlabel('Number of Nodes')
        ax.set_ylabel('Depth')
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title(title)

    plt.show()

# plot_svm(X_test,y_test)

