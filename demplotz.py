# -*- coding: utf-8 -*-

from parse import dane as raw_data_nasze
from parsej import dane  as raw_data_por
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('ggplot')

names=["uczelnia","Płeć","Wiek","Miejsce zamieszkania", "n_rodziny","Rodzice razem?","Matka - wykształcenie", "Ojciec - wykształcenie", "Matka - praca","Ojciec - praca","Wybór uczelni", "Czas dojazdu", "Czas na naukę","Niezdane przedmioty","Dodatkowe zajęcia (studia)", "Dodatkowe zajęcia (rodzina)","Organizacje studenckie", "Internet", "W związku","Relacje z rodziną", "Czas wolny","Czas na znajomych", "Alkohol w dni powszednie","Alkohol w weekend", "Ocena zdrowia","Liczba nieuzasadnionych nieobecności","Ocena - semestr", "Ocena - rok"]

tytuly = raw_data_nasze.columns.tolist()
np_nasze = raw_data_nasze.as_matrix()
np_portu = raw_data_por.as_matrix()
np_razem = np.concatenate((raw_data_nasze.as_matrix(), raw_data_por.as_matrix()), axis=0)

razem = pd.concat([raw_data_nasze, raw_data_por])

# bez uczelni i n_rodziny bo to stringi są
lista = list(range(1, len(tytuly)))
lista.remove(4)

for i in lista:
  print(i)

  a = np_razem[:, i]
  n = len(np.unique(a))
  m = 0

  if (n <= 2):
      m = np.min(a)
      n = m + 3
  else:
      m = int(np.floor(np.min(a)))
      n = m + 6

  his = np.histogram(a, bins = range(m,n))
  fig, ax = plt.subplots()
  offset = 0
  plt.bar(his[1][1:],his[0],align='center')
  ax.set_xticks(his[1][1:] + offset)
  if n < 5:
      ax.set_xticklabels( ('0','I') )
  else:
      ax.set_xticklabels( ('I', 'II', 'III', 'IV' , 'V') )

  # plt.figure()
  # raw_data_nasze[tytuly[i]].plot(kind='hist')
  # # plt.hist(np_nasze[:, i])
  # # plt.xlabel(tytuly[i])
  # # plt.ylabel("Entries")
  # # # plt.title("Nasze: " + names[i])
  # plt.axhline(0, color='k')
  # plt.savefig("plotz/nasze_" + tytuly[i] + ".png")
  # plt.close()

  # plt.figure()
  # raw_data_por[tytuly[i]].plot(kind='hist')
  # # plt.hist(np_portu[:, i])
  # # plt.xlabel(tytuly[i])
  # # plt.ylabel("Entries")
  # # # plt.title("Portugalia: " + names[i])
  # plt.axhline(0, color='k')
  # plt.savefig("plotz/portu_" + tytuly[i] + ".png")
  # plt.close()

  # plt.figure()
  # razem[tytuly[i]].plot(kind='hist')
  # # plt.hist(np_razem[:, i])
  # # plt.xlabel(tytuly[i])
  # # plt.ylabel("Entries")
  # # # plt.title("Razem: " + names[i])
  # plt.axhline(0, color='k')
  plt.savefig("plotz/razem_" + tytuly[i] + ".png")
  plt.close()
