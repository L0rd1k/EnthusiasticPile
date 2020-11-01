from django.test import TestCase
import requests
# Create your tests here.
def first_test():
    r = requests.get('http://127.0.0.1:8000/movie-shot/')
    a = r.text
