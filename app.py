from flask import Flask, render_template, request, redirect

import sqlite3 as sql
import datetime

app = Flask(__name__)

con = sql.connect('new_database.db')
con.execute('CREATE TABLE IF NOT EXISTS "gst_items" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "Item" VARCHAR,'
            '"Price" REAL, "Slab" INTEGER, "GST_Price" REAL, "Added_at" TIMESTAMP)')

@app.route('/')
def home():
    return render_template("home.html")



@app.route('/calculate', methods = ['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        things = request.form
        item = things['item']
        price = things['price']
        slab = things['slab']

        if (price.isnumeric()) == True:
            gst_price = ((int(slab)/100)*float(price)) + float(price)
            gst_price = float("{:.2f}".format(gst_price))
        else:
            return redirect("/calculate")

        con = sql.connect("new_database.db")
        cur = con.cursor()

        cur.execute("INSERT INTO gst_items(Item,Price,Slab,GST_Price,Added_at) VALUES(?, ?, ?, ?, ?)", (item, price, slab, gst_price, datetime.datetime.now()))

        con.commit()
        con.close()
        return redirect('/itemdetails')
    return render_template("calculate.html")


@app.route('/itemdetails')
def itemdetails():
    con = sql.connect("new_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM gst_items ORDER BY ID DESC LIMIT 1")
    output = cur.fetchall()
    return render_template("itemdetails.html", output=output)


@app.route('/table')
def table():
    con = sql.connect("new_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM gst_items ORDER BY ID DESC ")
    output = cur.fetchall()
    return render_template("table.html", output = output)

@app.route('/chart')
def chart():
    con = sql.connect("new_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM gst_items WHERE Slab ='5'")
    slab1 = len(cur.fetchall())
    cur.execute("SELECT * FROM gst_items WHERE Slab ='12'")
    slab2 = len(cur.fetchall())
    cur.execute("SELECT * FROM gst_items WHERE Slab ='18'")
    slab3 = len(cur.fetchall())
    cur.execute("SELECT * FROM gst_items WHERE Slab ='28'")
    slab4 = len(cur.fetchall())

    return render_template("chart.html", **locals())

if __name__ == "__main__":
    app.run(debug=True)