import config
import database as DB

def insertRecord(data):
    if config.AllowInsert:
        cursor = DB.connection.cursor()
        sql = 'INSERT INTO moz_bookmarks (id, parent, position, title, type) VALUES(?, ?, ?, ?, ?)'
        sqlData = (data['id'], data['parent'], data['position'], data['title'], data['type'])
        cursor.execute(sql, sqlData)
        DB.connection.commit()
        print('DB Add', data)
    else:
        print('DB Add skip', data)

def deleteRecord(data):
    if config.AllowDelete:
        cursor = DB.connection.cursor()
        sql = 'DELETE FROM moz_bookmarks WHERE id = ?'
        cursor.execute(sql, (str(data['id']),))
        DB.connection.commit()
        print('DB Delete', data)
    else:
        print('DB Delete skip', data)

def updateRecord(id, record ):
    if config.AllowUpdate:
        cursor = DB.connection.cursor()
        sql = 'UPDATE moz_bookmarks SET parent = ?,  position = ?, title = ?, type = ? WHERE id = ?'
        sqlData = (record['parent'], record['position'], record['title'], record['type'], str(id) )
        cursor.execute(sql, sqlData)
        DB.connection.commit()
        print('DB Update', id, record)
    else:
        print('DB Update skip', id, record)


def rowToDict(row):
    return {
        'id' : row['id'],
        'type': row['type'],
        'parent': row['parent'],
        'position': row['position'],
        'title': row['title']
    }

def get_local():
    try:
        cursor = DB.connection.cursor()
        cursor.execute('SELECT * FROM moz_bookmarks')
        data = cursor.fetchall()
        dataArray = []
        for row in data:
            dataArray.append(rowToDict(row))
        return dataArray
    except DB.sqlite3.OperationalError or DB.sqlite3.DatabaseError:
        print('Database locked')
        return None

def get_by_id(id):
    cursor = DB.connection.cursor()
    sql = 'SELECT * FROM moz_bookmarks WHERE id = ?'
    cursor.execute(sql, ( str(id), ))
    data = cursor.fetchone()
    if data is not None:
        return rowToDict(data)
    return None
