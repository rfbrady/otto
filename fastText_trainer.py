import fastText as ft
import os 

training_data = os.getcwd() + '/cooking.train'
testing_data = str(os.getcwd() + '/data/truncated_valid.txt')

td_token = ft.tokenize(training_data)


training_model = ft.load_model(training_data)

output_model = ft.train_supervised(input=training_data)


print(output_model)

