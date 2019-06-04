from app import app
from flask import Flask,render_template,flash, redirect, render_template,request,url_for
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import mysql.connector
import itertools

socketio = SocketIO(app)
def set_password(username,password):
    #create hash for password
    hash = generate_password_hash(password)
    val = (username,hash)
    #submit to database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="DM29243011",
      database="scrapped"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (username,password) VALUES (%s, %s);"
    mycursor.execute(sql,val)
    mydb.commit()
    return "hi"

def check_password(username,password):
    #get info from database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="DM29243011",
      database="scrapped"
    )
    mycursor = mydb.cursor()
    #fetch the password hash for the username
    mycursor.execute("SELECT password FROM users") #WHERE username = '%s';" % (username)) 
    myresult = mycursor.fetchall()
    for x in myresult:
        #check the hash with the password
        if check_password_hash(str(x[0]),str(password)) == True:
            return redirect(url_for("welcome"))
        else:
            flash('Invalid password provided')
            return redirect(url_for("index"))
            #return render_template("start_screen.html",error='invalid credentials provided')
                    
def quick_search(query):
    #connect to database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="DM29243011",
    database="scrapped"
    )
    #Where the information will be stored
    myresult = []
    #Sends command to mydb
    mycursor = mydb.cursor()
    sql ="SELECT * FROM foodnetwork WHERE MATCH(%s) AGAINST('%s');" % ("name",query["name"])
    #execute the command
    mycursor.execute(sql)
    #fetch results
    myresult=mycursor.fetchall()
    #send to javascript to display
    socketio.emit('results',myresult)
    
def food_guide_checker(userAge,userGender,userVeg,userGrai,userMilk,userMeat):
    #page = requests.get('https://www.canada.ca/en/health-canada/services/canada-food-guide/about/history-food-guide/eating-well-with-canada-food-guide-2007.html')
    #soup = BeautifulSoup(page.text, 'lxml')
    #numList = []
    advList = set()
    #userVeg = 3
    #userGrai = 4
    #userMilk = 5
    #userMeat = 3
    #userAge = int(input("How old are you? "))
    #while userAge < 2 or userAge % 1 != 0:
        #print("Please input a valid age.")
        #userAge = int(input("How old are you? "))
    #print(userAge)
    #userGender = input("What gender were you assigned when you were born? (M/F) ")
    #while userGender != "M" and userGender != "F":
        #print("Please input a valid option.")
        #userGender = input("What gender were you assigned when you were born? (M/F) ")
    #tableData = soup.find(class_='table table-striped table-bordered table-hover table-condensed table-responsive')
    #tableDataNum = tableData.find_all('td')

    #for i in tableDataNum:
    #    num = i.contents[0]
    #    numList.append(num)
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="DM29243011",
      database="scrapped"
    )
    mycursor = mydb.cursor()
    sql = "SELECT work FROM canadianfoodguide"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    numList = myresult[0][0].split(",")
    if userAge == 2 or userAge == 3:
        guideVeg = int(numList[14])
        print(guideVeg)
        guideGrai = int(numList[23])
        print(guideGrai)
        guideMilk = int(numList[48])
        guideMeat = int(numList[42])
        if userVeg < guideVeg:
            advList.add("Get more fruits and vegetables")
        if userGrai < guideGrai:
            advList.add("Get more grains")
        if userMilk < guideMilk:
            advList.add("Get more milk/alternatives")
        if userMeat < guideMeat:
            advList.add("Get more meat/alternatives")

    elif userAge >=4 and userAge <= 8:
        guideVeg = int(numList[15])
        print(guideVeg)
        guideGrai = int(numList[24])
        print(guideGrai)
        guideMilk = int(numList[48])
        guideMeat = int(numList[42])
        if userVeg < guideVeg:
            advList.add("Get more fruits and vegetables")
        if userGrai < guideGrai:
            advList.append("Get more grains")
        if userMilk < guideMilk:
            advList.add("Get more milk/alternatives")
        if userMeat < guideMeat:
            advList.add("Get more meat/alternatives")

    elif userAge >=9 and userAge <= 13:
        guideVeg = int(numList[16])
        print(guideVeg)
        guideGrai = int(numList[16])
        print(guideGrai)
        guideMilkOne = int(numList[36][0])
        guideMilkTwo = int(numList[36][2])
        guideMeatOne = int(numList[43][0])
        guideMeatTwo = int(numList[43][2])
        if userVeg < guideVeg:
            advList.add("Get more fruits and vegetables")
        if userGrai < guideGrai:
            advList.add("Get more grains")
        if userMilk < guideMilkOne:
            advList.add("Get more milk/alternatives")
        if userMeat < guideMeatOne:
            advList.add("Get more meat/alternatives")

    elif userAge >=14 and userAge <= 18:
        if userGender == "F":
            guideVeg = int(numList[17])
            print(guideVeg)
            guideGrai = int(numList[16])
            print(guideGrai)
            guideMilkOne = int(numList[36][0])
            guideMilkTwo = int(numList[36][2])
            guideMeat = int(numList[44])
            if userVeg < guideVeg:
                advList.add("Get more fruits and vegetables")
            if userGrai < guideGrai:
                advList.add("Get more grains")
            if userMilk < guideMilkOne:
                advList.add("Get more milk/alternatives")
            if userMeat < guideMeat:
                advList.add("Get more meat/alternatives")
        else:
            guideVeg = int(numList[18])
            print(guideVeg)
            guideGrai = int(numList[17])
            print(guideGrai)
            guideMilkOne = int(numList[36][0])
            guideMilkTwo = int(numList[36][2])
            guideMeat = int(numList[45])
            if userVeg < guideVeg:
                advList.add("Get more fruits and vegetables")
            if userGrai < guideGrai:
                advList.add("Get more grains")
            if userMilk < guideMilkOne:
                advList.add("Get more milk/alternatives")
            if userMeat < guideMeat:
                advList.add("Get more meat/alternatives")

    elif userAge >=19 and userAge <= 50:
        if userGender == "F":
            guideVegOne = int(numList[19][0])
            guideVegTwo = int(numList[19][2])

            guideGraiOne = int(numList[28][0])
            guideGraiTwo = int(numList[28][2])

            guideMilk = int(numList[44])
            guideMeat = int(numList[44])
            if userVeg < guideVegOne:
                advList.add("Get more fruits and vegetables")
            if userGrai < guideGraiOne:
                advList.add("Get more grains")
            if userMilk < guideMilk:
                advList.add("Get more milk/alternatives")
            if userMeat < guideMeat:
                advList.add("Get more meat/alternatives")
        else:
            guideVegOne = int(numList[20][0])
            guideVegTwo = int(numList[20][2])
            print(guideVeg)
            guideGrai = int(numList[18])
            print(guideGrai)
            guideMilk = int(numList[44])
            guideMeat = int(numList[45])
            if userVeg < guideVegOne:
                advList.add("Get more fruits and vegetables")
            if userGrai < guideGrai:
                advList.add("Get more grains")
            if userMilk < guideMilk:
                advList.add("Get more milk/alternatives")
            if userMeat < guideMeat:
                advList.add("Get more meat/alternatives")

    if userAge >=51:
        if userGender == "F":
            guideVeg = int(numList[17])
            guideGrai = int(numList[16])
            guideMilk = int(numList[45])
            guideMeat = int(numList[44])
            if userVeg < guideVeg:
                advList.add("Get more fruits and vegetables")
            if userGrai < guideGrai:
                advList.add("Get more grains")
            if userMilk < guideMilk:
                advList.add("Get more milk/alternatives")
            if userMeat < guideMeat:
                advList.add("Get more meat/alternatives")
        else:
            guideVeg = int(numList[17])

            guideGrai = int(numList[17])

            guideMilk = int(numList[45])
            guideMeat = int(numList[45])
            if userVeg < guideVeg:
                advList.add("Get more fruits and vegetables")
            if userGrai < guideGrai:
                advList.add("Get more grains")
            if userMilk < guideMilk:
                advList.add("Get more milk/alternatives")
            if userMeat < guideMeat:
                advList.add("Get more meat/alternatives")
    message =  {}
    message["vegetables"] = guideVeg
    message["carbohydrates"] = guideGrai
    #message["milk"] = guideMilk
    message["meat"] = guideMeat
    message["advice"] = ",".join(advList)
    return message
@app.route("/")
def index():
    return render_template("start_screen.html")

    ##If I have time, I will probably include a function for finding the top recipes and also pulling their subscription channels "these are extras for now"
    ##Also maybe favourites
    
#@socketio.on("search_database")
#def search_database(json, methods=['GET','POST']):
#    mydb = mysql.connector.connect(
#      host="localhost",
#      user="root",
#      passwd="",
#      database="scrapped"
#    )
#    return "hi"
@app.route("/welcome")
def welcome():
    return render_template("welcome_page.html")

##Here is where the function for pulling the info about their fridge comes in "Deluckshan"
##Also the function for advising about if the person is getting enough nutrients "Ashwin"

@app.route("/search/")
def search():
#    user = request.args.get('user')
#    query = {"name":"hello"}
#    socketio.emit('results',query)
    return render_template("search.html")
#    endresult = searcher(query)
@socketio.on('searcher')
def handle_searcher(query):
    if len(list(query.keys())) == 1:
            quick_search(query)
    else:
        #connect to database
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="DM29243011",
        database="scrapped"
        )
        #Where the information will be stored
        myresult = []
        #Sends command to mydb
        mycursor = mydb.cursor()
        #weighting of importance in the search
        weight = "(rel1*3)+rel2+(rel3*0.75)+ (rel4*0.5) + (rel5*2)"
        #This will build the sql command, based on whats given
        sql = "SELECT *, "
        for q in query.keys():
            if list(query.keys()).index(q) == len(list(query.keys()))-1:
                sql +="MATCH(%s) AGAINST('%s') AS rel%s " % (q,query[q],list(query.keys()).index(q)+1)
            else:
                sql +="MATCH(%s) AGAINST('%s') AS rel%s, " % (q,query[q],list(query.keys()).index(q)+1)
            #"ALTER TABLE foodnetwork ADD FULLTEXT(ingredients)"
            #"SELECT * FROM foodnetwork WHERE MATCH(ingredients) AGAINST('%s');" % (query)
            #"SELECT ingredients,name FROM foodnetwork" 
        sql += "FROM foodnetwork ORDER BY " + weight + "DESC;"
        #execute the command
        mycursor.execute(sql)
        #fetch results
        myresult=mycursor.fetchall()
        #send to javascript to display
        socketio.emit('results',myresult)

@app.route("/recipe")
def recipe():
    return render_template("recipe.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/fridge")
def fridge():
    return render_template("my_fridge.html")

@app.route("/groceries")
def groceries():
    return render_template("grocery_list.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    username = request.form['uname']
    password = request.form['psw']
    return check_password(username,password)
@socketio.on('message')
def handle_message(message):
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="DM29243011",
      database="scrapped"
    )
    mycursor = mydb.cursor()
    sql = "SELECT grocery,quantity FROM groceries WHERE username =%s"
    username = message
    mycursor.execute(sql,(username, ))
    myresult = mycursor.fetchall()
    socketio.emit('groceries',myresult)

@socketio.on('json')
def handle_json(json):
    val = []
    username = json["username"]
    json.pop("username", None)
    for i in list(json.keys()):
        val.append((username,i,json[i]))
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="DM29243011",
      database="scrapped"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO groceries (username,grocery,quantity) VALUES (%s,%s, %s) ON DUPLICATE KEY UPDATE grocery = VALUES(grocery),quantity = VALUES(quantity);"
    mycursor.executemany(sql,val)
    mydb.commit()
    socketio.emit('notification','hi')
'''
@socketio.on("scan_fridge")
##Here is where the function will go for the google api code "Prabh/Ashwin"

@socketio.on("login")
##Here is where the function for OAuth for logging in using a google account "Ashwin/Prabh"

@app.route("/update")
##This is where the updating database function comes in "Deluckshan"
'''
@socketio.on('fridge_info')
def handle_fridge (msg):
    socketio.emit("message",food_guide_checker(18,"M",3,4,5,3))

if __name__ == "main":
    socketio.run(app)
