# -*- coding: utf-8 -*-
"""
Created on Fri Dec  11 23:16:33 2016

@author: Justyna
"""

import pandas as pd

dane = pd.read_csv('./portugalia.csv',skipinitialspace=False, parse_dates=True,skiprows=2,
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
dane.plec = dane.plec.str.strip().str.lower().str.replace(' ','').replace('m',1).replace('f',2)

dane.miastowies = dane.miastowies.replace('U',1).replace('R',2)
dane.powod = dane.powod.replace('course',1).replace('reputation',2).replace('home',3).replace('other',4)
dane.m_br = dane.m_br.str.strip().str.lower().str.replace(' ','')
dane.o_br = dane.o_br.str.strip().str.lower().str.replace(' ','')
mapa_br = {'services': 1, 'teacher': 2, 'other' : 4,'health' : 3, 'at_home' : 4}
dane = dane.replace({'o_br': mapa_br, 'm_br': mapa_br})
dane.oc_sem = dane.oc_sem.fillna(0)
dane.oc_sem = dane.oc_sem/4
dane.oc_rok = dane.oc_rok/4
dane.rodzice_razem = dane.rodzice_razem.replace('A',0).replace('T',1)
dane.godziny = pd.to_numeric(dane.godziny,errors='coerce')
dane = dane[(dane.wiek < 30) & (dane.godziny <= 50)]

mapa = {'yes': 1, 'no': 0}
dane = dane.replace({ 'sex': mapa, 'organizacje' : mapa,'dod_zaj_stud' : mapa, 'dod_zaj_rodz' : mapa, 'internet' : mapa})

dane_np = dane.as_matrix()
