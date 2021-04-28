from flask import Flask,render_template, redirect, url_for,request
import requests


app = Flask(__name__,template_folder = 'template')

bot = ['my name is doge','really tho','haha name go skrrrtttt']
user = ['no your name is KangBot','yes no cap']

@app.route("/")
def main():
	return render_template("home.html")

@app.route("/sub1")
def sub1():
	return render_template("sub1.html")

@app.route("/tes",methods=['GET', 'POST'])
def tes():
	return render_template("index.html")
	

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/chat")
def chat():
	global chat
	global bot
	global user
	global panjang
	text = request.args.get('jsdata')
	user.append(text)
	bot.append("why tho")
	
	return render_template("chat.html",bot=bot,user=user)

if (__name__ == "__main__"):
	app.run(debug=True)

