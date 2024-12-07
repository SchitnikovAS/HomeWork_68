import sqlite3


def initiate_db():
    cursor.execute("""                          
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    """)
    cursor.execute("""                          
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    """)


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    users = cursor.fetchall()
    return users


def is_included(username):
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchall()
    if not check_user:
        return False
    else:
        return True


def add_user(username, email, age):
    cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, int(age), 1000))
    conection.commit()


conection = sqlite3.connect('product_base.db')
cursor = conection.cursor()




if __name__ == '__main__':
    initiate_db()

    # for i in range(4):
    #     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
    #                    (f'Продукт {i + 1}', f'Описание {i + 1}', (i + 1) * 100))


    conection.commit()
    conection.close()
