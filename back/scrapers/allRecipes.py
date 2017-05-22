import requests
import sys
import json
from bs4 import BeautifulSoup

def scrape(urlPath):
  # get the html, extract information
  r = requests.get(urlPath)
  soup = BeautifulSoup(r.content, "html.parser")
  ingredientSet = soup.findAll('span', {'itemprop': "ingredients"})
  title = soup.find('meta', {'property': 'og:title'})['content']
  ingredientList = []

  # format each ingredient to item
  for item in ingredientSet:
    if item['data-id'] == "0":
    	continue
    food = item.contents[0]
    ingredientList.append(food)

  thing = dict(recipe=title, ingredients=ingredientList, url=urlPath)
  print(json.dumps(thing))

if __name__ == '__main__':
	scrape(sys.argv[1])
