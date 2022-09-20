import sqlite3
import config

connection = sqlite3.connect(config.Config.get('App', 'bookmarks_file'), check_same_thread=False)
connection.row_factory = sqlite3.Row