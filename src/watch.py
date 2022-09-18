import os
import time
import sqlite3
import configparser
import threading
import requests

from jsondiff import diff
from flask import Flask, render_template, request, jsonify

Config = configparser.ConfigParser()
Config.read(os.getcwd()+'/config.ini')

compare_url = 'http://'+Config.get('App', 'compare_host')+':'+Config.get('App', 'compare_port')+'/'
def getConnection():
    try:
        connection = sqlite3.connect(Config.get('App', 'bookmarks_file'), check_same_thread=False)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.OperationalError or sqlite3.DatabaseError:
        print('Database locked')
        return None

connection = getConnection()
if connection == None:
    exit()

cursor = connection.cursor()



folders = {}

def rowToDict(row):
    return {
        'id' : row['id'],
        'type': row['type'],
        'parent': row['parent'],
        'position': row['position'],
        'title': row['title']
    }
app = Flask(__name__, template_folder=os.getcwd()+"/src/templates") # static_folder="public"

@app.route('/', methods=['GET'])
def home():
    return jsonify(get_local())

def fetch_compare():
    try:

        res = requests.get(compare_url)
        if res.status_code == 200:
            return res.json()
        return None
    except requests.ConnectionError or requests.JSONDecodeError:
        print('Remote machine not running')
        return None

def get_local():
    cursor.execute('SELECT * FROM moz_bookmarks')
    data = cursor.fetchall()
    dataArray = []
    for row in data:
        dataArray.append(rowToDict(row))
    return dataArray

def activate_job():
    def run_job():
        while True:
            print('run_job')
            remoteData = fetch_compare()

            if remoteData != None:
                localData = get_local()
                jsonDiff = diff(localData, remoteData, marshal=True)

                # first updates
                for change in jsonDiff:
                    if change != '$delete' and change != '$insert':
                        currentRowData = localData[change]
                        for field in jsonDiff[change]:
                            value = jsonDiff[change][field]
                            sql = 'UPDATE moz_bookmarks SET '+field+' = ? WHERE id = ?'
                            sqlData = (value, str(currentRowData['id']))
                            cursor.execute(sql, sqlData)
                            connection.commit()

                # then delete
                if '$delete' in jsonDiff:
                    for index in jsonDiff['$delete']:
                        currentRowData = localData[index]
                        sql = 'DELETE FROM moz_bookmarks WHERE id = ?'
                        cursor.execute(sql, (str(currentRowData['id']), ) )
                        connection.commit()

                # insert new
                if '$insert' in jsonDiff:
                    for change in jsonDiff['$insert']:
                        # 0 - position, 1 - data
                        data = change[1]
                        sql = 'INSERT INTO moz_bookmarks (id, parent, position, title, type) VALUES(?, ?, ?, ?, ?)'
                        sqlData = (data['id'], data['parent'], data['position'], data['title'], data['type'])
                        cursor.execute(sql, sqlData)
                        connection.commit()

            time.sleep(60)

    thread = threading.Thread(target=run_job)
    thread.start()

if __name__ == '__main__':
    print('Compare url', compare_url)
    activate_job()
    app.run(host=Config.get('App', 'host'), port=int(Config.get('App', 'port')))
    fetch_compare()
# cursor.close()
# connection.close()