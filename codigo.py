import hashlib
from getpass import getpass
from mysql.connector import connect, Error
import random
import string
import pandas as pd

def get_random_account(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
def crear_cuenta():
    user = get_random_account(5)
    mail = user + "@gmail.com"
    password = get_random_account(8)
    pin = get_random_account(6)
    return (user,mail,password,pin)


def md5Hash(password):
    bytepass = bytes(password, 'utf-8')
    hexpass = hashlib.md5(bytepass).hexdigest()
    return hexpass
lista = []
cuentasCreadas = pd.DataFrame()
for i in range(100):
    cuenta=crear_cuenta()
    cuentaCreada = pd.DataFrame([[cuenta[0],cuenta[1],cuenta[2],cuenta[3]]],columns=['nombre','mail','password','pin'])
    cuentasCreadas = cuentasCreadas.append(cuentaCreada, ignore_index=True)
    lista.append((cuenta[0],cuenta[1],md5Hash(cuenta[2]),md5Hash(cuenta[3])))
cuentasCreadas.to_excel('cuentas.xlsx',index=False)

for index, row in cuentasCreadas.iterrows():
    nombre = row['nombre']
    mail = row['mail']
    password = md5Hash(row['password'])
    pin = md5Hash(row['pin'])

insert_reviewers_query = """
INSERT INTO cuentas
(Nombre, Email, Password, Pin)
VALUES ( %s, %s, %s, %s)
"""


try:
    with connect(
        host="-",
        user='root',
        password='123123',
        database="fsao",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(insert_reviewers_query, lista)
            connection.commit()


except Error as e:
    print(e)

