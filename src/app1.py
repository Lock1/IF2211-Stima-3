from flask import Flask,render_template, redirect, url_for,request
import requests
import Interface

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
	storage.append([1, text])

	evalList = Interface.evaluateString(text)
	if evalList[0] == "add":
		storage.append([2, "Penambahan berhasil " + evalList[1][1]])
	elif evalList[0] == "see-specific":
		storage.append([2, "Hasil Pencarian\n"])
		for taskWord in evalList[1]:
			storage.append([2, taskWord])
	elif evalList[0] == "see":
		storage.append([2, "Hasil Pencarian\n"])
		for taskEntry in evalList[1]:
			storage.append([2, str(taskEntry[0][0]) + "/" + str(taskEntry[0][1]) + "/" + str(taskEntry[0][2]) + " " + taskEntry[1]])
	elif evalList[0] == "update":
		storage.append([2, "Penggantian berhasil " + evalList[1]])
	elif evalList[0] == "done":
		storage.append([2, "Task " + evalList[1] + " telah selesai"])
	elif evalList[0] == "delete":
		storage.append([2, "Penghapusan berhasil " + evalList[1][1]])
	elif evalList[0] == "help":
		storage.append([2, "Keyword tersedia"])
		storage.append([2, "1. deadline"])
		storage.append([2, "2. tambah"])
		storage.append([2, "3. hapus"])
		storage.append([2, "4. selesai"])
		storage.append([2, "5. kapan"])
		storage.append([2, "6. fitur / bantuan"])
	elif evalList[0] == "search-fail":
		if evalList[1] == "see-specific":
			storage.append([2, "Tugas tidak ditemukan"])
		elif evalList[1] == "see":
			storage.append([2, "Database kosong"])
		elif evalList[1] == "update":
			storage.append([2, "Pencarian tugas gagal"])
		elif evalList[1] == "delete":
			storage.append([2, "Penghapusan tugas gagal"])
		elif evalList[1] == "done":
			storage.append([2, "Tugas tidak ditemukan"])
	elif evalList[0] == "recommend":
		storage.append([2, "Kecocokan penuh tidak ditemukan, rekomendasi keyword:"])
		for recWord in evalList[1]:
			storage.append([2, recWord])
	else:
		storage.append([2, "Tidak ada kecocokan"])

	return render_template("chat.html",storage=storage)

if (__name__ == "__main__"):
	app.run(debug=True)
