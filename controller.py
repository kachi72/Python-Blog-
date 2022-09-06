import time
import re
from flask import request
import dbconnect


# #connecting to db
# db = dbconnect.connection()  
# cursor = db.cursor()

#user validation
def checkuser(userid):
    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT USERID FROM USERS'''
    cursor.execute(message)
    userid2 = int(userid)
    result = cursor.fetchall()
    check = any(userid2 in sublist for sublist in result)
    if check:
        return True
    else:
        return False
    
#post validation
def checkpost(postid):
    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT POSTID FROM POSTS'''
    cursor.execute(message)
    postid2 = int(postid)
    result = cursor.fetchall()
    check = any(postid2 in sublist for sublist in result)
    if check:
        return True
    else:
        return False
    
#comment validation
def checkcomment(commentid):
    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT COMMENTID FROM COMMENTS'''
    cursor.execute(message)
    commentid2 = int(commentid)
    result = cursor.fetchall()
    check = any(commentid2 in sublist for sublist in result)
    if check:
        return True
    else:
        return False

#email validation
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def checkmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#creating a user
def CreateUser(request):
    fname = request.form['fname']
    lname = request.form['lname']
    #email validation
    email = request.form['email']
    if checkmail(email) != 1:
        return("Invalid email")
    password = request.form['password']
    gender = request.form['gender']
    number = request.form['number']
    db = dbconnect.connection()  
    cursor = db.cursor()
    userid = 0
    create =  '''INSERT INTO Users VALUES (%s, %s, %s, %s, %s, %s, %s) '''
    vals = (userid,fname,lname,email,password,gender,number)
    message = '''SELECT EMAIL,PASSWORD FROM USERS'''
    cursor.execute(message)
    result = cursor.fetchall()
    #checks if user already exists
    for row in result:
        Email = row[0]
        Password = row[1]
        if ((email.lower() == Email.lower()) & (password.lower() == Password.lower())):
            return ("Error,\n This user already exists")
    #create user
    try:
        cursor.execute(create, vals)
        db.commit()
        return('Successfully created user')
    except:
        db.rollback
        return('Error creating user')



# #creating a post
def CreatePost(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    postid = 0
    userid = request.form['userid']
    title = request.form['title']
    content = request.form['content']
    update = time.asctime(time.localtime(time.time()))
    delete = 0
    if (request.form['image']):
        image = request.form['image']
    else:
        image = 0
    likes = 0
    
    #check if user exists
    if checkuser(userid) != 1:
        return "Error, this user does not exist"

    postcreate = ''' INSERT INTO POSTS VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
    val = (postid,userid,title,content,update,delete,image,likes)

    try:
        cursor.execute(postcreate, val)
        db.commit()
        return("Successfully created a post")
    except:
        db.rollback()
        return("Error creating post")


#creating comments
def CreateComment(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    userid = request.form['userid']
    postid = request.form['postid']

    #check if user exists
    if checkuser(userid) != 1:
        return "Error, this user does not exist"

    #check if post exists
    if checkpost(postid) != 1:
        return "Error, this post does not exist" 
        
    comment = request.form['comment']
    commentid = 0
    date = time.asctime(time.localtime(time.time()))  
    display = ''' INSERT INTO COMMENTS VALUES (%s, %s, %s, %s, %s)  '''
    info = [commentid, userid, postid, comment, date]
    
    try:
        cursor.execute(display,info)
        db.commit()
        return("Comment successfully posted")
    except:
        return("Error, unable to post comment")
    


#display a user profile
def DisplayUser(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    fname = request.form['fname']
    lname = request.form['lname']
    userid = request.form['userid']
    
    #check if user exists
    if checkuser(userid) != 1:
        return "Error, this user does not exist"

    display = '''  SELECT * FROM Users  WHERE FIRSTNAME = %s AND LASTNAME = %s AND USERID = %s'''
    display2 = ''' SELECT CONTENT FROM POSTS WHERE USERID = %s'''
    info = [fname,lname,userid]
    info2 = [userid]
    cursor.execute(display2,info2)
    result2 = cursor.fetchall()
    posts = len(result2)
    try:
        cursor.execute(display,info)
        result = cursor.fetchall()
            
        for row in result:
            UserID = row[0]
            FirstName = row[1]
            LastName = row[2]
            Email = row[3]
            Password = row[4]
            Gender = row[5]
            PhoneNumber = row[6]
            return("User details below:\n\nUserID = %d\nFirstName = %s\nLastName = %s\nEmail = %s\nPassword = %s\nGender = %s\nPhoneNumber = %d\nNumber of Posts = %s\n" % (UserID, FirstName, LastName, Email,Password, Gender, PhoneNumber,posts) );
    except:
        return('Error fetching user information')
    


#display posts
def DisplayPosts():
    db = dbconnect.connection()  
    cursor = db.cursor()
    display = '''SELECT POSTID, TITLE, CONTENT, LIKES FROM POSTS'''
    list = []
    try:
        cursor.execute(display)
        result = cursor.fetchall()
            
        for row in result:
            Postid = row[0]
            Title = row[1]
            Content = row[2]
            Likes = row[3]
            postiddict = {"Postid" : str(Postid)}
            titledict = {"Title" : str(Title)}
            contentdict = {"Content" : str(Content)}
            likesdict = {"Likes" : Likes}
            list.append(postiddict)
            list.append(titledict)
            list.append(contentdict)
            list.append(likesdict)
        return list
    except:
        return('Error fetching posts')

    

#display posts and comments
def DisplayBlog():
    db = dbconnect.connection()  
    cursor = db.cursor()
    
    display = '''SELECT POSTID,USERID,TITLE, CONTENT, LIKES FROM POSTS'''
    display2 = ''' SELECT POSTID,COMMENT FROM COMMENTS'''
    display3 = ''' SELECT FIRSTNAME,LASTNAME FROM USERS WHERE USERID = %s '''
    display4 = '''SELECT POSTID,USERID,TITLE,CONTENT,LIKES FROM '''

    cursor.execute(display)
    result = cursor.fetchall()
    list=[]
            
    for row in result:
        Postid = row[0]
        Userid = row[1]
        Title = row[2]
        Content = row[3]
        Likes = row[4]
        info = [Userid]
        cursor.execute(display3,info)
        result3 = cursor.fetchall()
        for row in result3:
            Fname = result3[0]
        cursor.execute(display2)
        result2 = cursor.fetchall()
        for row in result2:
            postid = row[0]
            comment = row[1]
            if (Postid == postid):
                postiddict = {"Postid" : str(Postid),"Title" : str(Title),"Content" : str(Content),"Author" : str(Fname),"Likes" : Likes}
                commentdict = {"Comment" : str(comment)}
                list.append(postiddict)
                list.append(commentdict)
            else:
                postiddict2 = {"Postid" : str(Postid),"Title" : str(Title),"Content" : str(Content),"Author" : str(Fname),"Likes" : Likes}
                list.append(postiddict2)

    seen = set()
    new_l = []
    for d in list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
        new_l.append(d)        
    return list




#displaying all users of table
def Display():
    db = dbconnect.connection()  
    cursor = db.cursor()
    display = """SELECT * FROM Users """

    try:
        cursor.execute(display)
        results = cursor.fetchall()
        p = len(results)
        i = 0
        for row in results:
            if (i <p):
                UserID = row[i]
                FirstName = row[i+1]
                LastName = row[i+2]
                Email = row[i+3]
                Password = row[i+4]
                Gender = row[i+5]
                PhoneNumber = row[i+6]
                return( "UserID = %d,FirstName = %s,LastName = %s,Email = %s,Password = %s, Gender = %s, PhoneNumber = %d \n" % (UserID, FirstName, LastName, Email,Password, Gender, PhoneNumber) );
    except:
        return('Error fetching data')

    return

    # #another way to print table
    # try:
    #     cursor.execute(sq1);
    #     results = cursor.fetchall()
    #     for row in results:
    #         print(row, "\n");
    # except:
    #     print("Error extracting data");




#delete user
def DeleteUser(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    userid = request.form['userid']
    fname = request.form['fname']
    lname = request.form['lname']

    #check if user exists
    if checkuser(userid) != 1:
        return "Error, this user does not exist"

    display = '''  SELECT * FROM Users  WHERE FIRSTNAME = %s AND LASTNAME = %s AND USERID = %s'''
    info = [fname,lname,userid];
    cursor.execute(display,info);
    result = cursor.fetchall();
    # for row in result:
    #     Userid = row[0];
    #     FirstName = row[1];
    #     LastName = row[2];
    #     Email = row[3];
    #     Gender = row[5];
    #     Number = row[6]
    #     print("UserID: %s\nFirstName: %s\nLastName: %s\nEmail: %s\nGender: %s\nPhoneNumber: %s\n" % (Userid,FirstName,LastName,Email,Gender,Number));
    # answer = input("Do you want to delete this profile, Yes or no:\n")
    # list = [Userid];
    # if answer.lower() == "no":
    #     exit();
    list = [userid]
    try:
        delete = '''DELETE FROM USERS WHERE USERID = %s'''
        cursor.execute(delete,list);
        db.commit();
        return("Successfully deleted user");
    except:
        db.rollback();
        return("Unsuccessfully deleted user");


    return

# deleting posts
def DeletePost(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    userid = request.form['userid']
    post = request.form['postid']

    #check if user exists
    if checkuser(userid) != 1:
        return "Error, this user does not exist"
    #check if post exists
    if checkpost(post) != 1:
        return "Error, this post does not exist"

    display = ''' SELECT * FROM POSTS WHERE POSTID = %s '''
    info = [post]
    cursor.execute(display,info)
    result = cursor.fetchall()
    for row in result:
        Postid = row[0]
        Userid = row[1]
        Title = row[2]
        Content = row[3]
    
    Userid2 = str(Userid)
    #check if user has access to delete post 
    if (userid != Userid2):
        return("You do not have access to delete this post")
    # answer = input("Do you want to delete this post, Yes or no:\n");
    # if answer.lower() == "no":
    #     exit()
    message = ''' DELETE FROM POSTS WHERE POSTID = %s ''';
    try:
        cursor.execute(message,info);
        db.commit();
        return('Post successfully deleted');
    except:
        return("Unsuccessful")

    return

#deleting comments
def DeleteComment(request):
    db = dbconnect.connection()  
    cursor = db.cursor()
    userid = request.form['userid']
    commentid = request.form['commentid']
    info = [commentid]

    #check if user exists
    if checkuser(userid) != 1:  
        return "Error, this user does not exist"
    #check if comment exists
    if checkcomment(commentid) != 1:
        return "Error, this comment does not exist"

    display = '''SELECT * FROM COMMENTS WHERE COMMENTID = %s '''
    cursor.execute(display,info)
    result = cursor.fetchall()
    for row in result:
        commentid = row[0]
        Userid = row[1]
        Postid = row[2]
        Comment = row[3]
        date = row[4]
        
    Userid2 = str(Userid)
    #checks if user have access to delete comment
    if (userid!= Userid2):
        return('You do not have access to delete this comment')

    message = ''' DELETE FROM COMMENTS WHERE COMMENTID = %s ''';
    try:
        cursor.execute(message,info)
        db.commit()
        return('Comment successfully deleted')
    except:
        return("Unsuccessful")

    


#liking a post
def Like(request):
    db = dbconnect.connection()  
    cursor = db.cursor()

    id = request.form['postid']
    message1 = ''' UPDATE POSTS SET LIKES = LIKES + 1 WHERE POSTID = %s '''
    info = [id]
    try:
        cursor.execute(message1,info)
        db.commit()
        return('Post was successfully liked')
    except:
        return("Error in liking this post")
        db.rollback()

    return

#unliking a post
def Unlike(request):
    db = dbconnect.connection()  
    cursor = db.cursor()

    id = request.form['postid']
    message1 = ''' UPDATE POSTS SET LIKES = LIKES - 1 WHERE POSTID = %s '''
    info = [id]
    try:
        cursor.execute(message1,info)
        db.commit()
        return('Post was successfully unliked')
    except:
        return("Error in unliking this post")
        db.rollback()

    return

#like and unlike
def Interactions(request):
    if (request.form['option'].lower()) == 'like':
        return Like(request)
    elif(request.form['option'].lower()) == 'unlike':
        return Unlike(request)
    else:
        return "Invalid input"


#granting access to blog
def Login(request):

    db = dbconnect.connection()  
    cursor = db.cursor()
    loop = True

    while(loop):
        user = request.form['email']
        while(1):
            if checkmail(user) == 1:
                break
            else:
                return ("Invalid email")
        password = request.form['password']
        message = ' SELECT EMAIL,PASSWORD FROM USERS  '

        cursor.execute(message)
        result = cursor.fetchall()
        for row in result:
            User = row[0]
            Password = row[1]
            if (user == User) & (password == Password):
                return("Successfully logged into account")
            
        return "Incorrect email or password"

    
    
