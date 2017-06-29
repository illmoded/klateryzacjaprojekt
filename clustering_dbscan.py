from parse import dane as raw_data_nasze
from parsej import dane  as raw_data_por
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import combinations

from mpl_toolkits.mplot3d import Axes3D

# scikit
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

tytuly = raw_data_nasze.columns.tolist()
np_dane = np.concatenate((raw_data_nasze.as_matrix(), raw_data_por.as_matrix()), axis=0)

# print(tytuly)
# ['uczelnia', 'plec', 'wiek', 'miastowies', 'n_rodziny', 'rodzice_razem', 'm_wyksz', 'o_wyksz', 'm_br', 'o_br', 'powod', 'dojazd', 'nauka', 'niezdane', 'dod_zaj_stud', 'dod_zaj_rodz', 'organizacje', 'internet', 'sex', 'relacje', 'czas_wolny', 'czas_znajomi', 'alk_dzien', 'alk_weekend', 'zdrowie', 'godziny', 'oc_sem', 'oc_rok']

# pętla wszystko ze wszystkimi, bo czemu nie? #hehe
lista = list(range(1, len(tytuly)))
lista.remove(4)
permutacje = list(combinations(lista, 3))

labels_true = np.append(np.zeros([np.shape(raw_data_nasze.as_matrix())[0]]), np.ones([np.shape(raw_data_por.as_matrix())[0]]))

for item in permutacje:
  dane = np.array([ np_dane[:, item[0]], np_dane[:, item[1]], np_dane[:, item[2]] ]).transpose()

  X = dane

  # DBSCAN - http://scikit-learn.org/stable/modules/clustering.html#dbscan
  db = DBSCAN(eps=1, min_samples=20, algorithm='kd_tree').fit(X)
  core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
  core_samples_mask[db.core_sample_indices_] = True
  labels = db.labels_

  n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

  # Ploty
  if n_clusters_ > 1:
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for k, col in zip(unique_labels, colors):
      if k == -1:
        # Black used for noise.
        col = 'k'

      class_member_mask = (labels == k)

      xy = X[class_member_mask & core_samples_mask]
      ax.plot(xy[:, 0], xy[:, 1], xy[:, 2], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)

      xy = X[class_member_mask & ~core_samples_mask]
      ax.plot(xy[:, 0], xy[:, 1], xy[:, 2], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=6)

    ax.set_xlabel(tytuly[item[0]])
    ax.set_ylabel(tytuly[item[1]])
    ax.set_zlabel(tytuly[item[2]])

    plt.title('Clusters: %d\nHomogeneity: %0.3f   Completeness: %0.3f   V-measure: %0.3f\nAdjusted Rand Index: %0.3f   Adjusted Mutual Information: %0.3f\nSilhouette Coefficient: %0.3f' % (n_clusters_, metrics.homogeneity_score(labels_true, labels), metrics.completeness_score(labels_true, labels), metrics.v_measure_score(labels_true, labels), metrics.adjusted_rand_score(labels_true, labels), metrics.adjusted_mutual_info_score(labels_true, labels), metrics.silhouette_score(X, labels)), fontsize=12)
    plt.savefig("plots/dbscan/dbscan_" + tytuly[item[0]] + "_vs_" + tytuly[item[1]] + "_vs_" + tytuly[item[2]] + ".png")
    plt.close()
