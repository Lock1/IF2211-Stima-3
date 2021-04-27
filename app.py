from flask import Flask,render_template, redirect, url_for,request	

app = Flask(__name__,template_folder = 'template')

@app.route("/")
def main():
	return render_template("home.html")

@app.route("/sub1")
def sub1():
	return render_template("sub1.html")

@app.route("/tes", methods=['GET', 'POST'])
def tes():
	if request.method == 'POST' :
		global chat
		chat = request.form["query"]
		return redirect(url_for("tes"))
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")


if (__name__ == "__main__"):
	app.run(debug=True)

