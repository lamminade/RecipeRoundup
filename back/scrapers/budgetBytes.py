import requests
import sys
import json
import string
from bs4 import BeautifulSoup

def scrape(urlPath):
  # get the html, extract information
  try:
  	r = requests.get(urlPath)
  	soup = BeautifulSoup(r.content, "html.parser")
  except:
  	print("URL error")
  	sys.exit(-1)	
  ingredientSet = soup.findAll('span', {'class': "wprm-recipe-ingredient-name"})
  title = soup.find('meta', {'property': 'og:title'})['content']
  ingredientList = []

  # format each ingredient to item
  for item in ingredientSet:
    food = item.contents[0]
    ingredientList.append(food)

  noNoWords = open("nonowords.txt", 'r')
  noNoWords = noNoWords.read().split(" ")

  # edit ingredients
  finalIngredients = []
  for ingredient in ingredientList:
   	t1 = str.maketrans('', '', string.punctuation)
   	if isinstance(ingredient, str):
	   	ingredient = ingredient.lower().translate(t1)
   		ingredient = ingredient.split(" ")
   	else:
   		ingredient = ingredient.string.lower().translate(t1)
   		ingredient = ingredient.split(" ")
   	# remove useless / weird words
   	badWords = []
   	for word in ingredient:
   		if word in noNoWords:
   			badWords.append(word)
   		if (word == ""):
   			ingredient.remove(word)
   	for word in badWords:
   		ingredient.remove(word)

   	# put edited string back together
   	finalIngredients.append(' '.join(ingredient))

  # put edited ingredients into json for database
  print(json.dumps(dict(recipe=title, ingredients=finalIngredients, url=urlPath)))

if __name__ == '__main__':
	if (len(sys.argv) < 2):
		print("No recipe supplied")
		sys.exit(-1)
	elif (len(sys.argv) > 2):
		print("Too many arguments supplied")
		sys.exit(-1)
	else:
		scrape(sys.argv[1])


#t2 = str.maketrans('', '', " ")