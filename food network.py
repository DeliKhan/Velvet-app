import requests
from bs4 import BeautifulSoup
import time
import json
from multiprocessing import Pool
from lxml.html import fromstring
import mysql.connector
import itertools
database = []
allergies=""
food = open("ingredients.txt","r")
ingredients_compare = food.readlines()
food.close()
alphabet = ["123","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","xyz"]

def updator(alpha):
    #alpha represents the alphabet letter
    global database
    url ="https://www.foodnetwork.com/recipes/recipes-a-z/%s" % (alpha)
    #scrap the website
    page = requests.get(url)
    page_content = BeautifulSoup(page.content,features="lxml") # get page content
    #analyze to get a list of all recipes that start with that letter
    recipe_list = page_content.find_all("ul",{"class":"m-PromoList o-Capsule__m-PromoList"})
    recipes = {}
    for t in recipe_list:
        alls = t.find_all("li")
        for g in alls:
            recipes[g.text] = g.find("a")["href"]
  
    for recipe in recipes.keys():
        #Get link to each recipe
        try:
            dish = requests.get("http:" + recipes[recipe])
        except:
            try:
                dish = requests.get("http:/" + recipes[recipe])
            except:
                dish = requests.get("http://foodnetwork.com" + recipes[recipe])
        #analyze each of these recipe links for more details (time,ingredients,etc.)
        #IK, alot of try and excepts. That's cause there is no one format for all recipes. Each one may look slightly different, making it
        #difficult to scrap with just one ruleset
        dish_content = BeautifulSoup(dish.content,features="lxml")
        try:
            hardness = dish_content.find("ul",{"class":"o-RecipeInfo__m-Level"}).find("span",{"class":"o-RecipeInfo__a-Description"}).text
        except:
            hardness = ""
        try:
            time = dish_content.find("ul",{"class":"o-RecipeInfo__m-Level"}).find("span",{"class":"o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total"}).text
            prep = dish_content.find("ul",{"class":"o-RecipeInfo__m-Time"}).findAll("span",{"class":"o-RecipeInfo__a-Description"})[0].text
            cook = dish_content.find("ul",{"class":"o-RecipeInfo__m-Time"}).findAll("span",{"class":"o-RecipeInfo__a-Description"})[1].text
        except:
            try:
                time = dish_content.find("ul",{"class":"o-RecipeInfo__m-Time"}).find("span",{"class":"o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total"}).text
            except:
                time = ""
            prep = ""
            cook = ""
        try:
            servings = dish_content.find("ul",{"class":"o-RecipeInfo__m-Yield"}).find("span",{"class":"o-RecipeInfo__a-Description"}).text
            rating = dish_content.find("span",{"class":"gig-rating-stars"})["title"]
        except:
            servings = ""
            rating = ""
        try:
            image = "http:" + dish_content.find("img",{"class":"m-MediaBlock__a-Image a-Image"})["src"]
        except:
            try:
                image = "http:" + dish_content.find("img",{"class":"m-MediaBlock__a-Image a-Image"})["data-src"]
            except:
                image = ""
        ingredients_temp = dish_content.findAll("p",{"class":"o-Ingredients__a-Ingredient"})
        ingredients = []
        for ing in ingredients_temp:
            ingredients.append(ing.text.strip())
        ingredients_list = "?!?@".join(ingredients)
        directions_temp = dish_content.findAll("li",{"class":"o-Method__m-Step"})
        directions = []
        for dirs in directions_temp:
            directions.append(dirs.text.strip())
        #I can't use commas cause the directions have them. So, to ensure proper splitting, I use a random set of letters
        directions_list = "?!?@".join(directions)
        #JSON[recipe] = [hardness,time,prep,cook,servings,rating,image,ingredients,directions]
    #return JSON
        #save each recipe as a tuple in a big list
        database.append((recipe,hardness,time,prep,cook,servings,rating,image,ingredients_list,directions_list))
    return database
if __name__ == '__main__':
    #a thread per alphabet letter to speed things up
    pool = Pool(processes=25)##run 25 seperate threads
    start = time.time()
    record = pool.map(updator, alphabet) ##map out each process's results to a single list
    pool.terminate()
    pool.join()
    final = list(itertools.chain.from_iterable(record)) ##merges all elements of list into single list
    #for parts in record:
    #    final.update(parts) ##join all dictionaries from each process
    #connect to database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="DM29243011",
      database="scrapped"
    )
    #DATABASE INFO
    #name = 100
    #hardness = 20
    #total = 15
    #prep = 10
    #cooking = 10
    #servings = 30
    #rating = 20
    #image = 350
    #ingredients = text
    #directions = text
    mycursor = mydb.cursor()
    #insert into database
    sql = "INSERT INTO foodnetwork (name,hardness,total,prep,cooking,servings,rating,image,ingredients,directions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name),hardness = VALUES(hardness),total = VALUES(total),prep = VALUES(prep),cooking = VALUES(cooking),servings = VALUES(servings),rating = VALUES(rating),image = VALUES(image),ingredients = VALUES(ingredients),directions = VALUES(directions);"
    mycursor.executemany(sql,final)
    mydb.commit()
    end = time.time()
    print(end-start)

#with open("data.json","w") as outfile:
#    json.dump(final, outfile)
#outfile.close()
