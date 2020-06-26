import os
import requests
import time
from flask import Flask, session,render_template,request,redirect,url_for,flash,make_response,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def log_in():
    return render_template('login.html')

@app.route("/handle_data", methods=['POST'])
def handle_data():

    data = request.form
    email1 = data["email"]
    pwd = data["pass"]
    username = data["username"]
    
    if db.execute("SELECT * from users WHERE username= :u AND password= :p",{"u":username,"p":pwd}).rowcount == 1 :
        return render_template('already_hehe.html')
    else:
        db.execute("INSERT INTO users (email,username,password) VALUES (:e,:u,:p)",{"e":email1,"u":username,"p":pwd})
        db.commit()
        return render_template('login.html')     


@app.route("/after_loggin",methods=["GET","POST"])
def after_login():
    data = request.form
    u = data["username"]
    pwd = data["pwd"]
    
    result = db.execute("SELECT * from users WHERE username=:u AND password=:p",{"u":u,"p":pwd}).fetchall()
    for row in result:
        if(pwd==row.password):
                ts = time.gmtime()
                timestamp = time.strftime("%x", ts)
                mybool = db.execute("SELECT * FROM blogs WHERE username=:u AND created_date=:timestamp",{"u":u,"timestamp":timestamp}).rowcount > 0
                print(mybool)
                if(mybool):
                    display = False
                    resp = make_response(render_template('feed.html',u=u,display=display))  
                    resp.set_cookie('username',u)  
                    return resp

                else:        
                    display = True    
                    resp = make_response(render_template('feed.html',u=u,display=display))  
                    resp.set_cookie('username',u)  
                    return resp  
            
        else:
            message2 = True
            message = False
            return render_template('empty.html',message=message,message2=message2)

@app.route("/after_submit",methods=["POST"])
def after_submit():
    data = request.form
    blog_text = data["blog-text"]
    x = request.cookies.get('username') 
    
    ts = time.gmtime()
    timestamp = time.strftime("%x", ts)
    
    db.execute("INSERT INTO blogs (username,text,created_date) VALUES (:u,:t,:c)",{"u":x,"t":blog_text,"c":timestamp})
    db.commit()

    message = True
    message2 = False
        
    return render_template('empty.html',message=message,message2=message2)

@app.route("/feed")
def feed():
    result=db.execute("SELECT * from blogs").fetchall()   
    for row in result:
        print("Username: ",row.username, "Blog:",row.text, "Created_date:",row.created_date)
    return render_template('posts.html',result=result)    


@app.route("/home")
def home_after_login():
    u = request.cookies.get('username')
    ts = time.gmtime()
    timestamp = time.strftime("%x", ts)
                
    mybool = db.execute("SELECT * FROM blogs WHERE username=:u AND created_date=:timestamp",{"u":u,"timestamp":timestamp}).rowcount > 0
    print(mybool)
    if(mybool):
        display = False
        return render_template('feed.html',display=display)

    else:        
        display = True    
        return render_template('feed.html',display=display) 