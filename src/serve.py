import os
import threading
import time

import config as Config
import cache as Cache
import database_operations as DB
import json_changes as JsonChanges
import request_operations as Fetch

from flask import Flask, request, jsonify

app = Flask(__name__, template_folder=os.getcwd()+"/src/templates") # static_folder="public"

@app.route('/', methods=['GET'])
def home():
    localData = DB.get_local()
    if localData != None:
        return jsonify(localData)
    else:
        return 'Cannot fetch local data', 400

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    localData = DB.get_local()
    if localData != None:
        # Update with incomming changes
        for row in data['insert']:
            hasLocal = DB.get_by_id(row['id'])
            if hasLocal is None:
                print('/update insert', row)
                DB.insertRecord(row)
            else:
                print('/update insert -> UPDATE', row)
                DB.updateRecord(row['id'], row)

        for row in data['update']:
            print('/update update',)
            DB.updateRecord(row['id'], row)

        for row in data['delete']:
            print('/update delete', row)
            DB.deleteRecord(row)

        # Update cache
        localData = DB.get_local()
        Cache.save_json_file('local_records.json', localData, clear=True)
        return 'ok', 200
    else:
        return 'Cannot fetch local data', 400

def activate_job():
    def run_job():
        while True:
            print('run_job')
            localData = DB.get_local()

            if localData != None:
                cacheExists=Cache.json_exist('local_records.json')
                Cache.save_json_file('local_records.json', localData)
                if cacheExists:
                    localCache = Cache.load_json_file('local_records.json')

                    localOperations = JsonChanges.getChanges(localCache, localData)
                    if localOperations['hasChanges']:
                        Fetch.push_changes(localOperations)
                else:
                    print('Skip submitting changes, cache was missing');
            time.sleep(60)

    thread = threading.Thread(target=run_job)
    thread.start()

if __name__ == '__main__':
    activate_job()
    app.run(host=Config.LocalHost, port=Config.LocalPort)