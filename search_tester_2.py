import mysql.connector
import itertools
import collections
query = {"name":"soup","hardness":"","servings":"","rating":"","ingredients":"milk"}
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="DM29243011",
    database="scrapped"
)
myresult = []
mycursor = mydb.cursor()
weight = "(rel1*2)+rel2+(rel3*0.75)+ (rel4*0.5) + (rel5*2)"
sql = "SELECT *, "
for q in query.keys():
    if list(query.keys()).index(q) == len(list(query.keys()))-1:
        sql +="MATCH(%s) AGAINST('%s') AS rel%s " % (q,query[q],list(query.keys()).index(q)+1)
    else:
        sql +="MATCH(%s) AGAINST('%s') AS rel%s, " % (q,query[q],list(query.keys()).index(q)+1)
    #"ALTER TABLE foodnetwork ADD FULLTEXT(ingredients)"
    #"SELECT * FROM foodnetwork WHERE MATCH(ingredients) AGAINST('%s');" % (query)
    #"SELECT ingredients,name FROM foodnetwork" 
sql += "FROM foodnetwork ORDER BY " + weight "DESC;"
mycursor.execute(sql)
myresult=mycursor.fetchall()
print(myresult)

    
