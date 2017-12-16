import psycopg2
try:
    conn = psycopg2.connect("dbname='coinkz' user='jonas' host='localhost' password='451524aa'")
    print("ok")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
cur.execute("DROP TABLE products")
command = """
CREATE TABLE products (
        id SERIAL,
        price INT NOT NULL,
        percent INT NOT NULL,
        name VARCHAR(50) NOT NULL,
        city VARCHAR(50) NOT NULL
);
"""
cur.execute(command)

class Data:

    def insert_vendor(price, percent, name, city):
        sql = """INSERT INTO products(price, percent, name, city)
                    VALUES(%s, %s, %s,%s) RETURNING id;"""
        product_id = None

        cur.execute(sql, (price,percent, name, city,))
        product_id = cur.fetchone()[0]
        conn.commit()

        return product_id

    insert_vendor(80, 80, "ss","dd")

    cur.execute("SELECT * FROM products;")
    g = cur.fetchone()
    print(g)