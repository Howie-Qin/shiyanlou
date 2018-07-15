# -*- coding:utf-8 -*-
import pandas as pd

def quarter_volume():
    data = pd.read_csv('apple.csv', header=0)
    
    s = data.Volume
    s.index = pd.to_datetime(data.Date)

    second_volume = s.resample('Q').sum().sort_values()[-2]

    return second_volume

if __name__ == "__main__":
   print( quarter_volume())
