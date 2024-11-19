from flask import Flask, render_template, request
from fuzzyDB import Fuzzy
import pandas as pd
import numpy as np

df = pd.read_csv("dataset/pariwisata.csv")

fuzzy = Fuzzy()
fuzzy.domain_variabel["Harga"] = np.arange(0, 201000, 500)
fuzzy.domain_variabel["Fasilitas"] = np.arange(0, 26, 0.5)
fuzzy.domain_variabel["Objek_Wisata_Berdekatan"] = np.arange(0, 26, 0.5)
fuzzy.domain_variabel["Jarak_dari_Pusat_Kota"] = np.arange(0, 75, 0.1)

fuzzy.himpunan_fuzzy["Harga"] = {
    "Murah": [0, 0, 15000, 20000],
    "Menengah": [15000, 37500, 60000],
    "Mahal": [50000, 60000, 200000, 200000],
}
fuzzy.himpunan_fuzzy["Fasilitas"] = {
    "Sedikit": [0, 0, 3, 5],
    "Sedang": [3, 5, 8],
    "Banyak": [7, 10, 25, 25],
}

fuzzy.himpunan_fuzzy["Objek_Wisata_Berdekatan"] = {
    "Sedikit": [0, 0, 3, 5],
    "Sedang": [3, 5, 8],
    "Banyak": [7, 10, 25, 25],
}

fuzzy.himpunan_fuzzy["Jarak_dari_Pusat_Kota"] = {
    "Dekat": [0, 0, 5, 10],
    "Menengah": [6, 15, 24],
    "Jauh": [20, 30, 40],
    "Sangat_Jauh": [36, 45, 75, 75],
}


def hitung_membership(df=df):
    selection_df = df[
        ["Harga", "Fasilitas", "Objek_Wisata_Berdekatan", "Jarak_dari_Pusat_Kota"]
    ]
    len_sebelum = len(df.columns)
    for i in selection_df.columns:
        for k, v in fuzzy.himpunan_fuzzy[i].items():
            print(i + " " + k.replace("_", " "))
            if len(v) == 4:
                df[i + " " + k.replace("_", " ").strip()] = [
                    fuzzy.trapmf(x, *v) for x in df[i].to_list()
                ]
            else:
                df[i + " " + k.replace("_", " ").strip()] = [
                    fuzzy.trimf(x, *v) for x in df[i].to_list()
                ]
    return df, len_sebelum


def query(
    operator,
    harga,
    fasilitas,
    objek_wisata_berdekatan,
    jarak_dari_pusat_kota,
    df,
    panjang_df_sebelum,
):
    half_df = df[[harga, fasilitas, objek_wisata_berdekatan, jarak_dari_pusat_kota]]
    if operator == "AND":
        df["Nilai_Rekomendasi"] = half_df.min(axis=1).apply(lambda x: round(x, 3))
    elif operator == "OR":
        df["Nilai_Rekomendasi"] = half_df.max(axis=1).apply(lambda x: round(x, 3))
    return df.drop(df.iloc[:, panjang_df_sebelum:-1], axis=1)


app = Flask(__name__)


@app.route("/")
def index():
    # Load the base page with the default 'home' content
    return render_template("index.html")


@app.route("/rekomendasi", methods=["POST", "GET"])
def rekomendasi():
    return render_template(
        "rekomendasi.html",
        items=df,
        variabel=fuzzy.domain_variabel,
        himpunan=fuzzy.himpunan_fuzzy,
    )


@app.route("/rekomendasi/detail/<string:nama_wisata>")
def detail(nama_wisata):
    baris = df.loc[df["Nama_Wisata"] == nama_wisata]
    return render_template("detail.html", data=baris)


@app.route("/rekomendasi/hitung/", methods=["POST", "GET"])
def hitung():
    operator = request.form.get("Operator")
    print(operator)
    harga = request.form.get("Harga")
    fasilitas = request.form.get("Fasilitas")
    objek_wisata_berdekatan = request.form.get("Objek_Wisata_Berdekatan")
    jarak_dari_pusat_kota = request.form.get("Jarak_dari_Pusat_Kota")

    df, panjang_df_sebelum = hitung_membership()
    final_df = query(
        operator,
        harga,
        fasilitas,
        objek_wisata_berdekatan,
        jarak_dari_pusat_kota,
        df,
        panjang_df_sebelum,
    )
    final_df = final_df.sort_values(by="Nilai_Rekomendasi", ascending=False).loc[
        final_df["Nilai_Rekomendasi"] > 0
    ]
    return render_template(
        "hitung.html",
        items=final_df,
        variabel=fuzzy.domain_variabel,
        himpunan=fuzzy.himpunan_fuzzy,
        operator=operator,
        harga=harga,
        fasilitas=fasilitas,
        objek_wisata_berdekatan=objek_wisata_berdekatan,
        jarak_dari_pusat_kota=jarak_dari_pusat_kota,
    )


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)
