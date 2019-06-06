import os
import json

fileInput = open(os.getcwd() + '\\' + 'result.txt') #recall results file
mainIn = fileInput.read()

i = 0
x = 0

arr = json.loads(mainIn) #split into array

ingredient = []  #ingredients list
probability = []  #probailties coinciding with ingredients arrays

new = arr["predictions"]

for i in range(len(new)):  #create separate arrays
    bre = new[i]
    inG = bre["tagName"]
    proB = bre["probability"]
    ingredient.append(inG)
    probability.append(proB)

run = len(probability)

probability = [i for i in probability if i>0.2] #filter acceptable probabilities

run2 = len(probability)

runLoo = run - run2 #the number of times the last element should be removed

for x in range(runLoo): #eliminates ingredients that are not in image
    ingredient.pop()
    
uN = ingredient.index('fridge') #removing the fridge characteristic and its probability
probability.pop(uN)
ingredient.remove('fridge')

final = ", ".join(ingredient)

print(final) #print ingredients list       


