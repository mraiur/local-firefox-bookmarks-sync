import os
import sqlite3
import config

databaseFile = os.path.abspath( config.Config.get('App', 'bookmarks_file') )
print('Database file ', databaseFile)
connection = sqlite3.connect(databaseFile, check_same_thread=False)
connection.row_factory = sqlite3.Row