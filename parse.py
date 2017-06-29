# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 19:16:33 2016

@author: pawel
"""

import pandas as pd
import numpy as np

dane = pd.read_csv('./Ankieta.csv',skipinitialspace=False, parse_dates=True,skiprows=2,
                                             names=['uczelnia','plec','wiek','miastowies',
                                              'n_rodziny','rodzice_razem','m_wyksz',
                                              'o_wyksz', 'm_br','o_br','powod',
                                              'dojazd', 'nauka','niezdane','dod_zaj_stud',
                                              'dod_zaj_rodz','organizacje',
                                              'internet', 'sex','relacje',
                                              'czas_wolny','czas_znajomi',
                                              'alk_dzien','alk_weekend',
                                              'zdrowie','godziny','oc_sem',
                                              'oc_rok'], na_values=['.'])

dane.uczelnia = dane.uczelnia.str.strip().str.lower().str.replace(' ','')
dane.plec = dane.plec.str.strip().str.lower().str.replace(' ','').replace('mężczyzna',1).replace('kobieta',2)

dane.miastowies = dane.miastowies.replace('Miasto',1).replace('Wieś',2)
dane.powod = dane.powod.replace('ciekawy kierunek',1).replace('reputacja uczelni',2).replace('blisko do domu',3).replace('inne',4)
dane.m_br = dane.m_br.str.strip().str.lower().str.replace(' ','')
dane.o_br = dane.o_br.str.strip().str.lower().str.replace(' ','')
mapa_br = {'służbacywilna(administracja,policjaitp.)': 1, 'szkolnictwo': 2, 'inne' : 4,'służbazdrowia' : 3}
dane = dane.replace({'o_br': mapa_br, 'm_br': mapa_br})
dane.oc_sem = dane.oc_sem.fillna(0)

dane['n_rodziny'] = np.where(dane['n_rodziny'] <= 3, 0, 1)

mapa = {'Tak': 1, 'Nie': 0}
dane = dane.replace({'rodzice_razem': mapa, 'sex': mapa, 'organizacje' : mapa,'dod_zaj_stud' : mapa, 'dod_zaj_rodz' : mapa, 'internet' : mapa})
dane.godziny = pd.to_numeric(dane.godziny,errors='coerce')
dane = dane[(dane.wiek < 30) & (dane.godziny <= 50)]


dane_np = dane.as_matrix()
