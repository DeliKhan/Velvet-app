import mysql.connector
import itertools
import collections
query = {"name":"corn","hardness":"easy","ingredients":"milk"}
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="DM29243011",
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
info = {}
for num in range(0,len(query.keys())):
    for element in myresult[num]:
        if element[0] in matches.keys():
            matches[element[0]] += len(myresult[num])-myresult[num].index(element) 
        else:
            try:
                matches[element[0]] = len(myresult[num])-myresult[num].index(element)
                info[element[0]] = myresult[num][myresult[num].index(element)]
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
another = sorted(info.items(), key=lambda x: endresult.index(x[0]))

print(endresult)
print(another)


    
