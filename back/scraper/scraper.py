import re
import requests
import sys
import json
import unicodedata
from bs4 import BeautifulSoup

prepWords = [
  "cubed", "diced", "melted", "deveined", "boned", "peeled", "beaten",
  "washed", "minced", "shredded", "chopped", "mashed", "seeded",
  "drained", "cut into chunks", "sliced", "prepared", "coarsely", "finely",
  "freshly", "crushed", "medium", "large", "small", "rinsed", "undrained", "optional", "(optional)"
]
extraWords = [
  "or to taste", "to taste", "for frying", "plus more as needed", "as needed", 
]
unitWords = [
  "tablespoon", "tablespoons", "teaspoon", "teaspoons", "cup", "cups", 
  "pounds", "pound", "clove", "cloves", "quart", "quarts", "pint", "pints",
  "ounce", "ounces", "dessert spoon", "dessert spoons", "kilogram", "kilograms",
  "gram", "grams", "package", "packages", "container", "containers", "pinch", "pinches",
  "bunch", "can", "cans", "stalk", "stalks", "bag", "bags", "liter", "liters", "litre", "litres", "milliliter",
  "milliliters", "fluid ounces", "fluid ounce", "deciliter", "deciliters", "gallon", "gallons",
  "barrel", "barrels"
]


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
    food = ingredientFormat((item.contents[0]).split())
    ingredientList.append(food)

  thing = dict(recipe=title, ingredients=ingredientList, url=urlPath)
  #return dict(recipe=title, ingredients=ingredientList, url=urlPath)
  print(json.dumps(thing))

# Returns dictionary item of ingredient with name, amount, and unit
def ingredientFormat(info):
  amt = info[0]
  if info[1] in unitWords:
    units = info[1]
    for word in info[1:]:
      if word in prepWords :
        info.remove(word)
    if info[-1] == 'and':
      del info[-1]
      title = (' '.join(info[2:]))
    else:
      title = (' '.join(info[2:]))
  else:
    units = "none"
    for word in info[1:]:
      if word in prepWords :
        info.remove(word)
    if info[-1] == 'and': 
      del info[-1]
      title = (' '.join(info[1:]))
    else:
      title = (' '.join(info[1:]))
  return dict(name=(remove_punctuation(title)).strip(None), amount=amt, unit=units)


# Force remove punctuation function
tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))
def remove_punctuation(text):
    return text.translate(tbl)

if __name__ == '__main__':
	scrape(sys.argv[1])
