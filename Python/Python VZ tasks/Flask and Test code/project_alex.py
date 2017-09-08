# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import json
import requests
import base64
import sqlite3
from sqlite3 import Error

# create the application object
my_service = Flask(__name__)

# use decorators to link the function to a url


@my_service.route('/')
def home():
    #return render_template("example.html")
    return "Frontend API with one API (GET: /getPicture)"


@my_service.route('/getPicture', methods=['GET'])
def call_get_picture():

    # specify url
    base_url = 'http://crappycode.herokuapp.com/task'
    # call rest api
    response_get_picture = requests.get(base_url)
    response = {}
    # General
    code = 200
    print "response_get_picture= " + str(response_get_picture.text)


    try:
        # print response
        # response = "response_get_picture= " + str(response_get_picture.text)


        dict2 = eval(response_get_picture.text)
        print 'response data value= ' + str(dict2['data'])
        data_value = dict2['data']

        imgdata = base64.b64decode(data_value)
        filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

        response = {"status": "success", "err": None}

        db_main(imgdata)

    except Exception, err_msg:
        code = 400
        # response["errorCode"] = "400"
        response["status"] = "fail"
        response["err"] = str(err_msg)

    finally:
        return json.dumps(response) if response else "", code
        # return data_value


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        conn.text_factory = str
        # conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    # finally:
    #     conn.close()
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_project(conn, picture):
    """
    Create a new picture into the pictures table
    :param conn:
    :param picture:
    :return: picture id
    """
    sql = ''' INSERT INTO pictures(name,picture_data)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, picture)
    return cur.lastrowid


def db_main(imgdata):
    database = "pythonsqlite.db"

    sql_create_pictures_table = """ CREATE TABLE IF NOT EXISTS pictures (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        picture_data BLOB
                                    ); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create pictures table
        create_table(conn, sql_create_pictures_table)

    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new picture
        picture = ('Mona Lisa', imgdata)
        picture_id = create_project(conn, picture)

        # ...and read it back:
        # db = sqlite3.connect('pythonsqlite.db')
        # row = conn.execute('SELECT * FROM pictures').fetchone()
        # print repr(str(row[0]))


@my_service.route('/getPicture/1', methods=['GET'])
def call_get_picture_1():
    db = sqlite3.connect('pythonsqlite.db')
    the_data = db.execute('SELECT picture_data FROM pictures where id=1;').fetchone()
    return the_data


if __name__ == '__main__':
    my_service.run(host="0.0.0.0", port=8083, debug=False)
