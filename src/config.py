import os
import sys
import configparser

Config = configparser.ConfigParser()

configFile = os.getcwd()+'/config.ini'
# Warning this is to be used LOCALLY ONLY
if len(sys.argv) > 1 and os.path.exists(os.getcwd()+'/'+sys.argv[1]):
    configFile = os.getcwd()+'/'+sys.argv[1]

Config.read(configFile)

compare_url = 'http://'+Config.get('App', 'compare_host')+':'+Config.get('App', 'compare_port')+'/'
update_url = compare_url + 'update'

AllowDelete = Config.get('App', 'allow_delete') == 'True'
AllowInsert = Config.get('App', 'allow_insert') == 'True'
AllowUpdate = Config.get('App', 'allow_update') == 'True'

LocalHost = Config.get('App', 'host')
LocalPort = int(Config.get('App', 'port'))
