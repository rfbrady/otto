from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
	template = loader.get_template('autocoder/index.html')
	return HttpResponse(template.render())


def upload_dataset(request, rowid):
	return HttpResponse('You are looking at record with title: {}'.format(rowid))

def view_database(request, title, short_description, long_description, sdg_code):
	response = 'request: {} title: {} short: {} long: {}'.format(title, short_description, long_description, sdg_code)
	return HttpResponse(response)
