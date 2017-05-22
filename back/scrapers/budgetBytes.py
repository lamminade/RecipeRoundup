import requests
import sys
import json
from bs4 import BeautifulSoup

def scrape(urlPath):
  # get the html, extract information
  r = requests.get(urlPath)
  soup = BeautifulSoup(r.content, "html.parser")
  ingredientSet = soup.findAll('li', {'class': "ingredient"})
  title = soup.find('meta', {'property': 'og:title'})['content']
  ingredientList = []

  # format each ingredient to item
  for item in ingredientSet:
    food = item.contents[0]
    ingredientList.append(food)

  print(json.dumps(dict(recipe=title, ingredients=ingredientList, url=urlPath)))

if __name__ == '__main__':
	scrape(sys.argv[1])
