import pymysql
from datetime import datetime


def validate(t):
    if len(t) == 4 and all(type(v) == int for v in t):
        return True


def save_data(t: tuple):
    if not validate(t):
        raise ValueError('Input formatted incorrectly')

    date = format(datetime.utcnow(), '%d/%m/%y')

    with pymysql.connect(host='localhost', port=3306, user='root', passwd='pass', db='mysql',autocommit=True) as cursor:
        sql = 'SELECT column_name FROM information_schema.columns WHERE table_name = "ethereum";'
        cursor.execute(sql)
        columns = tuple(i[0] for i in cursor.fetchall())
        sql = 'SELECT {} FROM `ethereum`;'.format(''.join('MAX(' + column + '), ' for column in columns[:-1])[:-2])
        cursor.execute(sql)
        aths = cursor.fetchone()
        updatedaths = (max(c, m) for c, m in zip(t, aths))
        newaths = tuple((columns[i], v) for i, v in enumerate(updatedaths) if v > aths[i])
        sql = 'INSERT INTO `ethereum` VALUES {};'.format(str(t + (date,)))
        cursor.execute(sql)

        return newaths

