# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 20:01:50 2016

@author: pawel
"""
import numpy as np
import pandas as pd
from parse import dane as dane_pl
from parsej import dane as dane_por

frames = [dane_pl, dane_por]
razem = pd.concat(frames)