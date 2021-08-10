from flask import Flask, request,jsonify
import json 
from flask_mysqldb import MySQL

#import flask_mysqldb
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
import pyrebase

#local upload or temp
UPLOAD_FOLDER ="./uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg" , "gif"}

#filter mime-types : to check for allowed extensions
def allowed_files(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
#config
app.config["MYSQL_HOST"]= "localhost"
app.config["MYSQL_USER"]= "root"
app.config["MYSQL_PASSWORD"]= ""
app.config["MYSQL_DB"]= "demoposts"
app.config["UPLOAD_FOLDER"]= UPLOAD_FOLDER
mysql = MySQL(app)

CORS(app)



#firebase config

config = {
    "apiKey": "AIzaSyBNezYGilJ9VJ-H9BttDpzJ1RMP-ScvntA",
    "authDomain": "democode-f8c66.firebaseapp.com",
    "projectId": "democode-f8c66",
    "databaseURL": "xxxxxx",
    "storageBucket": "democode-f8c66.appspot.com",
    "messagingSenderId": "987886143360",
    "appId": "1:987886143360:web:5d66113cdd15cb7c0d6365",
    "serviceAccount": "./keyfile.json" #to manage uploads
}

#init firebase app
firebase = pyrebase.initialize_app(config)
#firebase storage
storage=firebase.storage()

# @app.route("/")
# def helloindex():
#     return "Hello World"

@app.route("/api/posts", methods=["GET"])
def index():
    if request.method =="GET" :
        cur=mysql.connection.cursor()
        cur.execute(""" SELECT * FROM demoposts """)
        posts = cur.fetchall()
        # return jsonify({"posts" : posts})
        return jsonify(data = posts )

# @app.route("/api/posts", methods=["GET"])
# def index():
#     if request.method =="GET" :
#         return jsonify(data="posts main response")

# @app.route("/api/addpost", methods=["POST"])
# def index():
#     if request.method =="POST" :
#         return jsonify(data="posts main response")

@app.route("/api/addpost", methods=["POST"])
def addpost():
    if request.method == "POST":
        print(request.form, flush=True)
        title = request.form.get("title")
        content = request.form.get("content")
        cover = request.files["cover"]

        if cover and allowed_files(cover.filename):
            filename = str(uuid.uuid4())
            filename += "."
            filename += cover.filename.split(".")[1]

            #create secure name
            filename_secure = secure_filename(filename)
            #save the file inside the uploads folder
            cover.save(os.path.join(app.config["UPLOAD_FOLDER"], filename_secure))

            #local file
            local_filename = "./uploads/"
            local_filename += filename_secure    

            #firebase filename
            firebase_filename = "uploads/"
            firebase_filename += filename_secure

            #upload the file
            storage.child(firebase_filename).put(local_filename)
            #get the url of the file
            cover_image = storage.child(firebase_filename).get_url(None)
            
            #get cursor to execute the mysql functions
            cur = mysql.connection.cursor()
            cur.execute(""" INSERT INTO demoposts (title, content, cover, covername) VALUES (%s, %s, %s, %s)  """, (title, content, cover_image, filename_secure)
            )

            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename_secure))

            return jsonify(data = "The post was created successfully! ") 

@app.route("/api/post/<id>", methods=["GET"])
def singlepost(id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM demoposts WHERE id = '"+ id +"' ")
    record = cur.fetchone()  
    # record = request.get_json["record"]  
    # print(type(record)) 
    
    return jsonify({"data": record})

@app.route("/api/editfullpost/<id>", methods=["PUT"])
def editfullpost(id):
    if request.method == "PUT":
        print(request.form, flush=True)

        postid = request.form.get("id")
        title = request.form.get("title")
        content = request.form.get("content")
        oldcover = request.form.get("oldcover")
        covername = request.form.get("covername")

        if request.files["cover"]:
            if allowed_files(request.files["cover"].filename):
                cover = request.files["cover"]
                #creating the filename
                filename =str(uuid.uuid4())
                filename +="."
                filename += cover.filename.split(".")[1]

                #create a secure name
                filename_secure = secure_filename(filename)
                #save the file inside the folder specified
                cover.save(os.path.join(app.config["UPLOAD_FOLDER"], filename_secure)) 

                #local file
                local_filename = "./uploads/"
                local_filename += filename_secure

                #firebase file name
                firebase_filename = "uploads/"
                firebase_filename += filename_secure

                #upload the file
                storage.child(firebase_filename).put(local_filename);


                #get the url
                cover_image = storage.child(firebase_filename).get_url(None)
                #get the cursor to exec the mysql functions
                cur = mysql.connection.cursor()

                #update the values
                cur.execute(""" UPDATE demoposts SET title=%s, content=%s, cover=%s, covername=%s WHERE id=%s """,
                (title, content, cover_image, filename_secure, postid))

                #delete the current image
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename_secure))

                #path of the image to delete inside firebase
                firebase_filename_delete = "uploads/"
                firebase_filename_delete += covername 

                storage.delete(firebase_filename_delete)   

                return jsonify(data= "the post was updated successfull")

@app.route("/api/editpost/<id>", methods=["PUT"])
def editpost(id):
    if request.method == "PUT":
       postid = request.form.get("id")
       title = request.form.get("title")
       content = request.form.get("content")

       cur = mysql.connection.cursor()
       cur.execute(""" UPDATE demoposts SET title=%s, content=%s WHERE id=%s  """,
       (title, content, postid))

       return jsonify(data="The post was updated successfully") 

@app.route("/api/deletepost/<id>", methods=["DELETE"])
def deletepost(id):
    postid = request.form["id"]
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM demoposts WHERE id=%s  """ % (postid))
    return jsonify(data = "The post was deleted successfully")

if __name__ == "__main__":
    app.run(debug=True)