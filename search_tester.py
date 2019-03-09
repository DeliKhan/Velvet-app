import mysql.connector
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import itertools
query = {"name":"Kale","ingredients":"milk,kale"}
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="scrapped"
)
myresult = []
mycursor = mydb.cursor()
for q in query.keys():
    sql ="SELECT * FROM foodnetwork WHERE MATCH(%s) AGAINST('%s');" % (q,query[q])
    #"ALTER TABLE foodnetwork ADD FULLTEXT(ingredients)"
    #"SELECT * FROM foodnetwork WHERE MATCH(ingredients) AGAINST('%s');" % (query)
    #"SELECT ingredients,name FROM foodnetwork" 
    mycursor.execute(sql)
    myresult.append(mycursor.fetchall())

matches = {}
for element in myresult[0]:
    for num in range(1,len(query.keys())):
        if element[0] in matches.keys():
            matches[element[0]] += len(myresult[num])-myresult[num].index(element)
        else:
            try:
                matches[element[0]] = len(myresult[num])-myresult[num].index(element)
            except:
                pass
#        try:
#            myresult[num].remove(element)
#        except:
#            pass
##append the rest of the recipes that don't match into it
#for i in myresult:
#    for t in i:
#        matches[t[0]] = 0
                
endresult = sorted(matches, key=lambda k: matches[k])
endresult.reverse()



    
