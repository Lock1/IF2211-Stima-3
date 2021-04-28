from flask import Flask,render_template, redirect, url_for,request
import requests
import Interface

app = Flask(__name__,template_folder = 'template')

bot = []
user = []

@app.route("/")
def main():
	return render_template("home.html")

@app.route("/sub1")
def sub1():
	return render_template("sub1.html")

@app.route("/tes")
def tes():
	global reset
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
	evalList = Interface.evaluateString(text)
	if evalList[0] == "add":
		bot.append("Penambahan berhasil " + evalList[1][1])
	elif evalList[0] == "see-specific":
		resultQuery = "Hasil Pencarian\n"
		for taskWord in evalList[1]:
			resultQuery = resultQuery + taskWord + "\n"
		bot.append(resultQuery)
	elif evalList[0] == "see":
		resultQuery = "Hasil Pencarian\n"
		for taskEntry in evalList[1]:
			resultQuery = resultQuery + taskEntry[1] + "\n"
		bot.append(resultQuery)
	elif evalList[0] == "update":
		bot.append("Penggantian berhasil " + evalList[1][1])
	elif evalList[0] == "done":
		bot.append("Task " + evalList[1] + " telah selesai")
	elif evalList[0] == "delete":
		bot.append("Penghapusan berhasil " + evalList[1][1])
	elif evalList[0] == "help":
		helpString = "Keyword tersedia\n"
		helpString += "1. deadline\n"
		helpString += "2. tambah\n"
		helpString += "3. hapus\n"
		helpString += "4. selesai\n"
		helpString += "5. kapan\n"
		helpString += "6. fitur / bantuan\n"
		bot.append(helpString)
	elif evalList[0] == "search-fail":
		if evalList[1] == "see-specific":
			bot.append("Tugas tidak ditemukan")
		elif evalList[1] == "see":
			bot.append("Database kosong")
		elif evalList[1] == "update":
			bot.append("Pencarian tugas gagal")
		elif evalList[1] == "delete":
			bot.append("Penghapusan tugas gagal")
		elif evalList[1] == "done":
			bot.append("Tugas tidak ditemukan")
	elif evalList[0] == "recommend":
		baseString = "Kecocokan penuh tidak ditemukan, rekomendasi "
		for recWord in evalList[1]:
			baseString = baseString + recWord + " "
		bot.append(baseString)
	else:
		bot.append("Tidak ada kecocokan")

	return render_template("chat.html",bot=bot,user=user)

if (__name__ == "__main__"):
	app.run(debug=True)
