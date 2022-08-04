from flask import Flask,render_template, request
from flask import session as PersonalProject
import pyrebase

config= {

  "apiKey": "AIzaSyAsFd6ulyKDUXjThdr3MpLRdoXuDkwbN7s",

  "authDomain": "personalproject-d0644.firebaseapp.com",

  "databaseURL": "https://personalproject-d0644-default-rtdb.europe-west1.firebasedatabase.app",

  "projectId": "personalproject-d0644",

  "storageBucket": "personalproject-d0644.appspot.com",

  "messagingSenderId": "932589039672",

  "appId": "1:932589039672:web:5cbb545961caea84b4b6cd",

  "measurementId": "G-QKMKV808DZ",

  "databaseURL" :"https://personalproject-d0644-default-rtdb.europe-west1.firebasedatabase.app/"


}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

app = Flask (__name__)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			PersonalProject['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('index'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route ('/signup',methods= ['GET','POST'])
def signup():
	error=""
	if request.method=='POST':
		email = request.form['email']
		password= request.form['password']
		newUser = {"full_name":request.form ["full_name"], "address":request.form["address"],"phone_number":request.form["phone_number"]}
	try:
		PersonalProject ['user']= auth.create_user_with_email_and_password (email,password)
		db.child("Users").child(PersonalProject['user']['localId']).set(newUser)
		return redirect (url_for('/signin'))
	except:
		error= "Couldnt Signup"
		return render_template("signup.html")


@app.route ('/',methods= ['GET','POST'])
def index():
	return render_template("index.html")


@app.route('/post',methods= ['GET','POST'])
def post():
	error=""
	if request.method=='POST':
		posts ={"title":request.form["post_title"],"text":request.form["post_text"]}
		try:
			db.child("post").push(posts)
			return redirect (url_for('/post'))
		except :
			print ("Couldnt save post.")
	post = db.child('post').get().val()
	return render_template ("post.html",posts=post)

	




if __name__ == '__main__':
	app.run(debug=True)
	