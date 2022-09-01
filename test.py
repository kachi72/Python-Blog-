from __future__ import print_function
from flask import Flask,request
from flask_mysqldb import MySQL
import controller

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kachi'
app.config['MYSQL_PASSWORD'] = 'kachiuser'
app.config['MYSQL_DB'] = 'blog'
mysql = MySQL(app)

@app.route('/createuser', methods=['POST'])
def createuser():
    return controller.CreateUser(request)

@app.route('/createpost', methods=['POST'])
def createpost():
    return controller.CreatePost(request)
    
@app.route('/createcomment', methods=['POST'])
def comment():
    return controller.CreateComment(request)

@app.route('/deleteuser', methods=['DELETE'])
def deleteuser():
    return controller.DeleteUser(request)

@app.route('/deletepost', methods=['DELETE'])
def deletepost():
    return controller.DeletePost(request)

@app.route('/deletecomment', methods=['DELETE'])
def deletecomment():
    return controller.DeleteComment(request)

@app.route('/displayposts', methods=['GET'])
def displayposts():
    return controller.DisplayPosts()

@app.route('/displayuser', methods=['GET'])
def displayuser():
    return controller.DisplayUser(request)

@app.route('/displayblog', methods=['GET'])
def displayblog():
    return controller.DisplayBlog()

@app.route('/interaction', methods=['POST'])
def interaction():
    return controller.Interactions(request)

@app.route('/login',methods=['GET'])
def login():
    return controller.Login(request)

    
if __name__ == '__main__':
    app.run(debug=True,port=8080)

    
