import StringMatching
import DateRegex

keyword = ["hapus", "deadline", "selesai"]
kataPenting = ["kelompok", "meet", "mata kuliah"]
kataDurasi = ["bulan", "minggu", "hari"]
kataTugas = ["kuis", "ujian", "tucil", "tubes", "praktikum", "laporan"]
kataTidakPenting = ["pada", "tentang", "ke"]


    # addTask -> kT + date - kTP, tambah + kT + date
    # seeTask -> deadline, deadline + kD, deadline + "hari" + "ini", deadline + kT, deadline + date + date
    # seeSpecific -> deadline + databaseKeyword + "kapan"
    # updateTask -> deadline + databaseKeyword + date
    # solvedTask -> selesai + databaseKeyword
    # help -> give all
    # deleteTask -> hapus + databaseKeyword
