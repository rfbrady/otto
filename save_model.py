import pickle
import fastText as ft 

model = ft.load_model('truncated_model')

filename = 'pickled_model.pkl'


pickle.dump(model, open(filename, 'wb'))