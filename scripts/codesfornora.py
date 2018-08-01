import os
import numpy as np 
import fastText as ft 
import pandas as pd 

model1 = ft.load_model('sdg_unique_cleaned_model')
print('model loaded')

for 