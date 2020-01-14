import datetime


def var_name(variable):
    return '_'.join(variable.split(':')[0].lower().split())


def var_value(variable):
    if variable.strip()[-1] == '»':
        value = variable.split(':')[1].split('(')[0].split('\n')[0].strip()
    else:
        value = variable.split(':')[1].split('(')[0].strip()
    return value


def date_time(value):
    if value == None:
        pass
    try:
        date = datetime.datetime.strptime(value, '%B %d, %Y').date()
    except:
        pass
    try:
        date = datetime.datetime.strptime(value, '%d %B %Y').date()
    except:
        pass
    try:
        date = datetime.datetime.strptime(value, '%Y').date()
    except:
        pass
    try:
        date = datetime.datetime.strptime(value, '%B %Y').date()
    except:
        pass
    try:
        date = datetime.datetime.strptime(value, '%B %d').date()
    except:
        pass
    try:
        date = datetime.datetime.strptime(value, '%B, %Y').date()
    except:
        pass

    return date
