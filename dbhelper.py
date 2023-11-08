"""
	Python Database helper
"""
from mysql.connector import connect

def db_connect()->object:
    return connect(
        host="db4free.net",
        user="bilatkaba",
        port=3306,
        password="bilatkayat",
        database="final_project1"
    )
    
def doProcess(sql:str)->bool:
    db:object = db_connect()
    cursor:object = db.cursor()
    cursor.execute(sql)
    db.commit()
    return True if cursor.rowcount>0 else False
    
def getProcess(sql:str)->list:
    db:object = db_connect()
    cursor:object = db.cursor(dictionary=True)
    cursor.execute(sql)
    return cursor.fetchall()

def getall(table:str,page:int)->list:
    offset:int = (page - 1) * 10
    sql:str = f"SELECT * FROM `{table}` LIMIT 10 OFFSET {offset}"
    print(sql)
    return getProcess(sql)


def delete(table:str,**kwargs)->bool:
    params:list = list(kwargs.items())
    flds:list = list(params)
    
    sql:str = f"DELETE FROM ordered_items WHERE o_id IN (SELECT id FROM Orders WHERE c_id = {flds[0][1]})"
    print(sql)
    return doProcess(sql)


def searchK(table:str,key:str)->list:
    sql:str = f"SELECT * FROM {table} WHERE {'title' if table == 'items' else 'name'} LIKE '%{key}%'"
    print(sql)
    return getProcess(sql)
def getItems(o_id:int)->list:
    sql = f"SELECT * FROM ordered_items INNER JOIN items ON items.id = ordered_items.i_id WHERE ordered_items.o_id = {o_id}"
    return getProcess(sql)
def getOrders(c_id:int)->list:
    sql = f"SELECT * FROM orders WHERE orders.c_id = {c_id}"
    return getProcess(sql)
def getReviews(c_id:int)->list:
    sql = f"SELECT * FROM reviews INNER JOIN items on items.id = reviews.i_id WHERE reviews.c_id = {c_id}"
    return getProcess(sql)


def getrecord(table:str,**kwargs)->list:
    params:list = list(kwargs.items())
    flds:list = list(params[0])
    sql:str = f"SELECT * FROM `{table}` WHERE `{flds[0]}`='{flds[1]}'"
    return getProcess(sql)


def getuser(table:str,**kwargs)->list:
    params:list = list(kwargs.items())
    flds:list = list(params)
    sql:str = f"SELECT * FROM `{table}` WHERE `{flds[0][0]}`='{flds[0][1]}' AND `{flds[1][0]}`='{flds[1][1]}'"
    return getProcess(sql)

def addrecord(table:str,**kwargs)->bool:
    flds:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    fld:str = "`,`".join(flds)
    val:str = "','".join(vals)
    sql:str = f"INSERT INTO `{table}`(`{fld}`) values('{val}')"
    return doProcess(sql)

def updaterecord(table:str,**kwargs)->bool:
    flds:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    fld:list = []
    for i in range(1,len(flds)):
        fld.append(f"`{flds[i]}`='{vals[i]}'")
    params:str = ",".join(fld)
    sql:str = f"UPDATE `{table}` SET {params} WHERE `{flds[0]}`='{vals[0]}'"
    return doProcess(sql)
    
def deleterecord(table:str,**kwargs)->bool:
    params:list = list(kwargs.items())
    flds:list = list(params[0])
    sql:str = f"DELETE FROM `{table}` WHERE `{flds[0]}`='{flds[1]}'"
    return doProcess(sql)

#print(getrecord("student",idno='0002'))
#print(getall("student"))
#updaterecord('student',idno='0004',lastname='foxtrot',firstname='gold',course='bscs',level='3')

