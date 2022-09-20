import os
import json

def save_json_file(file, jsonData, clear=False):
    filePath = os.getcwd()+'/cache/'+file
    if not os.path.isfile(filePath) or clear == True:
        print('save json file', file)
        with open(filePath, 'w') as cacheFile:
            json.dump(jsonData, cacheFile)
            cacheFile.close()

def load_json_file(file):
    filePath = os.getcwd() + '/cache/' + file
    with open(filePath, 'r') as cacheFile:
        return json.load(cacheFile)

def json_exist(file):
    filePath = os.getcwd() + '/cache/' + file
    return os.path.isfile(filePath)