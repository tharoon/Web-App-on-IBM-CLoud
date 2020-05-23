import os
from flask import Flask, redirect, render_template, request
import json
import ibm_db
# from flask_db2 import DB2

app = Flask(__name__, static_url_path='')

# Python Code for Database Connection
# Get the HOSTNAME, USERID, PASSWORD FROM SERVICE CREDENTIALS ON IBM CLOUD DB2
conn = ibm_db.connect("DATABASE=;HOSTNAME=;PORT=;PROTOCOL=TCPIP;UID=;PWD=;", "", "")
print("Connected to db")
if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB For Transactions'][0]
    db2cred = db2info["credentials"]

else:
    raise ValueError('Expected cloud environment')

@app.route("/", methods=["POST", "GET"])
def displaytable():
    tablecontents = []
    query = "SELECT * FROM PEOPLE"
    stmt = ibm_db.exec_immediate(conn, query)
    result = ibm_db.fetch_both(stmt)
    while result:
        tablecontents.append(result)
        result = ibm_db.fetch_both(stmt)

    return render_template('index.html', table=tablecontents, title='Home')


@app.route("/update", methods=["POST", "GET"])
def update():
    kword = request.form.get("keywords")
    name = request.form.get("name")
    kword_data = []
    query1 = "UPDATE PEOPLE SET KEYWORDS = '" + str(kword) + "' WHERE NAME = '"+ str(name)+ "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    print("update: ", stmt1)
    query2 = "SELECT * FROM PEOPLE"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        kword_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('update.html', table=kword_data, title='Update')

@app.route("/show", methods=["POST", "GET"])
def show():
    name = request.form.get("name")
    query = "SELECT PIC FROM PEOPLE WHERE NAME = '" + str(name) + "'"
    stmt = ibm_db.exec_immediate(conn, query)
    result = ibm_db.fetch_both(stmt)
    while result:
        photo = result[0]
        result = ibm_db.fetch_both(stmt)


    return render_template('show.html', imagename=photo, name=name, title='Display Image')

@app.route("/insert", methods=["POST", "GET"])
def insert():
    name = request.form.get("name")
    file = request.form.get("file")
    query2 = "SELECT PICTURE FROM PEOPLE WHERE NAME = '" + str(name) + "'"
    stmt2 =  ibm_db.exec_immediate(conn, query2)
    result2 = ibm_db.fetch_both(stmt2)
    while result2:
        photo = result2[0]
        result2 = ibm_db.fetch_both(stmt2)
        if photo == file:
            return render_template('duplicateImage.html', title='Duplicate Image')
        else:
            query1 = "UPDATE PEOPLE SET PICTURE = '" + str(file) + "' WHERE NAME = '" + str(name) + "'"
            stmt1 = ibm_db.exec_immediate(conn, query1)
            print(stmt1)

            return render_template('insert.html', filename=file, title='Add/Insert')

@app.route("/updateImage", methods=["POST", "GET"])
def updateImage():
    name = request.form.get("name")
    image = request.form.get("image")
    image_data = []
    query1 = "UPDATE PEOPLE SET PIC = '" + str(image) + "' WHERE NAME = '"+ str(name)+ "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    print("update: ", stmt1)
    query2 = "SELECT * FROM PEOPLE"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        image_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('updateSalary.html', table=image_data, title='Update Image')





@app.route("/delete", methods=["POST", "GET"])
def delete():
    name = request.form.get("dname")
    deleted_data = []
    query1 = "DELETE FROM PEOPLE WHERE NAME = '" + str(name)+"'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    # result = ibm_db.fetch_both(stmt1)
    query2 = "SELECT * FROM PEOPLE"
    stmt2 = ibm_db.exec_immediate(conn, query2)
    result = ibm_db.fetch_both(stmt2)
    while result:
        deleted_data.append(result)
        result = ibm_db.fetch_both(stmt2)

    return render_template('delete.html', table=deleted_data, title='Delete')


@app.route("/withinrange", methods=["POST", "GET"])
def withinrange():
    range1 = request.form.get("from")
    range2 = request.form.get("to")
    range_data = []
    query1 = "SELECT PIC, NAME FROM PEOPLE WHERE OWNER BETWEEN '" + str(range1) + "' AND '" + str(range2)+"'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        range_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('withinrange.html', table=range_data, title='Salary Range')


@app.route("/greaterthan", methods=["POST", "GET"])
def salarygreaterthan():
    range1 = request.form.get("range1")
    greater_data = []
    query1 = "SELECT * FROM PEOPLE WHERE SALARY > '" + str(range1) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        greater_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('greaterthan.html', table=greater_data, title=' Salary greater Than')


@app.route("/lessthan", methods=["POST", "GET"])
def salarylessthan():
    range1 = request.form.get("range1")
    less_data = []
    query1 = "SELECT * FROM PEOPLE WHERE SALARY < '" + str(range1) + "'"
    stmt1 = ibm_db.exec_immediate(conn, query1)
    result = ibm_db.fetch_both(stmt1)
    while result:
        less_data.append(result)
        result = ibm_db.fetch_both(stmt1)

    return render_template('lessthan.html', table=less_data, title='Less Than')

@app.route("/readFile", methods=["POST", "GET"])
def readFile():
    file = request.form.get("file")
    return render_template('readFile.html', title='Read File')





port = os.getenv('PORT', '5000')

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=int(port))
    app.run(host='0.0.0.0', port=int(port))
