import sqlite3

connection = sqlite3.connect("products_data.db")
cursor = connection.cursor()


def initiate_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
                       )""")



    #list_prod = [["1","Картошка","ВКусная картошка","100"],["2","Морковь","Оранжевая и сочная","200"],["3","Яблоки","Сладкие и красные","300"],["4","Сок берёзовый","Вкусный и полезный","400"]]
    #cursor.executemany("INSERT INTO Products (id,title,description,price) VALUES(?,?,?,?)", (list_prod))
    connection.commit()

initiate_db()


def is_included(username):
    cursor.execute("SELECT username FROM Users")
    username_list = cursor.fetchall()

    for i in range(len(username_list)):
        if username in username_list[i]:

            return True

    return False


def is_includ_email(email):
    cursor.execute("SELECT email FROM Users")
    email_list= cursor.fetchall()
    for i in range(len(email_list)):
        if email in email_list[i]:
            return True
    return False



def add_users(username, email, age):

    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (username, email, age, 1000))
    connection.commit()




def get_all_products():
    cursor.execute("SELECT * FROM Products")
    product_list = cursor.fetchall()
    return product_list

get_all_products()


