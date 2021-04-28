from flask import Flask,render_template, redirect, url_for,request
import requests


app = Flask(__name__,template_folder = 'template')

storage = []

@app.route("/")
def main():
	return render_template("index.html")
	

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/chat")
def chat():
	global storage
	text = request.args.get('jsdata')
	storage.append(text)
	
	return render_template("chat.html",storage=storage)

if (__name__ == "__main__"):
	app.run(debug=True)

