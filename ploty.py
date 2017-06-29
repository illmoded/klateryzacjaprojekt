# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 21:09:46 2016

@author: pawel
"""

from parse import dane
from parsej import dane as danej
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from mpl_toolkits.mplot3d import Axes3D


def plot_corr(df,size=20):
#    to sa te korelacje
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation='vertical')
    plt.yticks(range(len(corr.columns)), corr.columns);
    plt.savefig("corr1.png")

def scatter_plt(X,y):
#    scatter 2 dim z regresja liniowa
    plt.xlabel(X.name)
    plt.ylabel(y.name)
    X = pd.DataFrame(X)
    y = pd.DataFrame(y)
    linreg = LinearRegression()
    linreg.fit(X,y)
    y_pred = linreg.predict(X)
#    fig = plt.figure()
    plt.scatter(X,y, color='black', s=200, alpha=.05)
    plt.plot(X,y_pred, color='red')

def histo4d(x,y,z,c = dane.plec,xbin = 5, ybin = 5, zbin = 5):
#    histogram 3d z gestoscia
#   c - kolorowanie - dodatkowy wymiar, domyslnie ze wzgledu na plec
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    mapa = plt.get_cmap('rainbow')
    ax.set_xlabel(x.name)
    ax.set_ylabel(y.name)
    ax.set_zlabel(z.name)
    r = np.column_stack((x,y,z))
    H, edges = np.histogramdd(r, bins = (5, 5, 5))
    ax.scatter(x, y, z, s = H*10, c = c, cmap = mapa)
#    plt.show()
    plt.savefig("radviz_" + x.name + "_vs_" + y.name + "_vs_" + z.name + ".png")


x = dane.o_wyksz;
y = dane.m_wyksz;
c = dane.zdrowie;
z = dane.relacje;

def kolka(wywalmn5 = True, doddowyw = []):
    doddowyw=list(doddowyw)
    #   to sa te kolka
    if (wywalmn5):
        mn5 = [] #mniej niz 5
        for col in dane.columns:
            if len(dane[col].unique()) < 5:
                mn5.append(col)
           # print(col)

    from pandas.tools.plotting import radviz
    exclude = [['godziny','oc_sem','oc_rok','uczelnia']] #wyrzucam wszystkie nie-inty, mozna wyrzucac dodatkowe
    exclude.append(mn5)
    exclude.append(doddowyw)
    exclude = [item for sublist in exclude for item in sublist]

    daneint=dane[dane.columns.difference(exclude)]

    fig = plt.figure(figsize=(10,10))
    for nazwa in daneint.columns:
        plt.title(nazwa)
        radviz(daneint, nazwa)
        plt.savefig("radviz_"+ len(exclude) + "_" + nazwa + ".png") #zapisywanie do pliku
        plt.clf()

#kolka()

#####
#   to jest to duze, niebieskie
#from pandas.tools.plotting import scatter_matrix
#fig = plt.figure(figsize=(40,40))
#scatter_matrix(dane, alpha=0.2, figsize=(40, 40), diagonal='kde')
#plt.savefig("scatter2.png")
#plt.close()
#####

#####
# jesli sie chce zrobic wszystkie ploty 3d, to mamy 3k wykresow
#from itertools import combinations
#trojki = list(combinations(dane.columns,3))
#print(len(trojki))
#####

# plot_corr(danej)

x = dane.o_wyksz;
y = dane.m_wyksz;
c = dane.zdrowie;
z = dane.relacje;

histo4d(x,y,z)
