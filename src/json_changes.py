from jsondiff import diff

def getChanges(baseJson, newJson):
    changeDiff = diff(baseJson, newJson, marshal=True)
    changes = {
        'hasChanges': False,
        'insert': [],
        'update': [],
        'delete': []
    }

    for change in changeDiff:
        if change != '$delete' and change != '$insert':
            toUpdate = True
            if change < len(baseJson):
                row = baseJson[change].copy()
            else:
                row = newJson[change].copy()
                toUpdate = False

            for field in changeDiff[change]:
                value = changeDiff[change][field]
                row[field] = value
            if toUpdate:
                changes['update'].append(row)
                print('JsonChanges Update', row)
            else:
                changes['insert'].append(row)
                print('JsonChanges Update -> Insert', row)


    # then delete
    if '$delete' in changeDiff:
        for index in changeDiff['$delete']:
            row = baseJson[index]
            changes['delete'].append(row)
            print('JsonChanges Delete', row)

    # insert new
    if '$insert' in changeDiff:
        for change in changeDiff['$insert']:
            # 0 - position, 1 - data
            data = change[1]
            print('JsonChanges Add', data)
            changes['insert'].append(data)

    changes['hasChanges'] = len(changes['insert'])>0 or len(changes['update'])>0 or len(changes['delete'])>0
    return changes

