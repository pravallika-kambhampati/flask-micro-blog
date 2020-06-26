from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import time

engine = create_engine('postgresql:///mydatabase')
Session = sessionmaker(bind=engine)

#from . import models

app = Flask(__name__)
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *
from app import db
from sqlalchemy.engine import create_engine
from flask.helpers import make_response
from sqlalchemy.orm.scoping import scoped_session


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
    
    if User.query.filter_by(email=email1).count():
        return render_template('already_hehe.html')
    else:
        me = User(email1,username,pwd)
        db.session.add(me)
        db.session.commit()
        return render_template('login.html')     


@app.route("/after_loggin",methods=["GET","POST"])
def after_login():
    data = request.form
    u = data["username"]
    pwd = data["pwd"]
    
    session = Session()
    result = session.query(User.password).filter(User.username == u)
    
    for row in result:
        if(pwd==row.password):
                ts = time.gmtime()
                timestamp = time.strftime("%x", ts)
                db = scoped_session(sessionmaker(bind=engine))
                
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
    
    record = Blog(x,blog_text,timestamp)
    db.session.add(record)
    db.session.commit()

    message = True
    message2 = False
        
    return render_template('empty.html',message=message,message2=message2)

@app.route("/feed")
def feed():
    Session = sessionmaker(bind = engine)
    session = Session()
    result = session.query(Blog).all()    
    for row in result:
        print("Username: ",row.username, "Blog:",row.text, "Created_date:",row.created_date)
    return render_template('posts.html',result=result)    


@app.route("/home")
def home_after_login():
    u = request.cookies.get('username')
    ts = time.gmtime()
    timestamp = time.strftime("%x", ts)
    db = scoped_session(sessionmaker(bind=engine))
                
    mybool = db.execute("SELECT * FROM blogs WHERE username=:u AND created_date=:timestamp",{"u":u,"timestamp":timestamp}).rowcount > 0
    print(mybool)
    if(mybool):
        display = False
        return render_template('feed.html',display=display)

    else:        
        display = True    
        return render_template('feed.html',display=display) 





if __name__ == "__main__":
    app.run()    

