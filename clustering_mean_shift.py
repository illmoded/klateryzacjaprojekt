from parse import dane as raw_data_nasze
from parsej import dane  as raw_data_por
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import cycle
from itertools import combinations

from mpl_toolkits.mplot3d import Axes3D

# scikit
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
from sklearn import metrics

tytuly = raw_data_nasze.columns.tolist()
np_dane = np.concatenate((raw_data_nasze.as_matrix(), raw_data_por.as_matrix()), axis=0)

lista = list(range(1, len(tytuly)))
lista.remove(4)
lista.remove(2)
lista.remove(26)
permutacje = list(combinations(lista, 1))

labels_true = np.append(np.zeros([np.shape(raw_data_nasze.as_matrix())[0]]), np.ones([np.shape(raw_data_por.as_matrix())[0]]))

for item in permutacje:
  dane = np.array([ np_dane[:, 2], np_dane[:, item[0]], np_dane[:, 26] ]).transpose()

  X = dane

  # Mean Shift - http://scikit-learn.org/stable/modules/clustering.html#mean-shift\
  bandwidth = estimate_bandwidth(X, quantile=0.2)

  ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
  ms.fit(X)
  labels = ms.labels_
  cluster_centers = ms.cluster_centers_

  labels_unique = np.unique(labels)
  n_clusters_ = len(labels_unique)

  if n_clusters_ > 1:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        ax.plot(X[my_members, 0], X[my_members, 1], X[my_members, 2], col + '.')
        for x in X[my_members]:
            ax.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], [cluster_center[2], x[2]], col)

    ax.set_xlabel(tytuly[2])
    ax.set_ylabel(tytuly[item[0]])
    ax.set_zlabel(tytuly[26])
    plt.title('Clusters: %d\nHomogeneity: %0.3f   Completeness: %0.3f   V-measure: %0.3f\nAdjusted Rand Index: %0.3f   Adjusted Mutual Information: %0.3f\nSilhouette Coefficient: %0.3f' % (n_clusters_, metrics.homogeneity_score(labels_true, labels), metrics.completeness_score(labels_true, labels), metrics.v_measure_score(labels_true, labels), metrics.adjusted_rand_score(labels_true, labels), metrics.adjusted_mutual_info_score(labels_true, labels), metrics.silhouette_score(X, labels)), fontsize=12)
    plt.savefig("plots/mean/mean_shift_" + tytuly[2] + "_vs_" + tytuly[item[0]] + "_vs_" + tytuly[26] + ".png")
    plt.close()
