import psycopg2

try:
    conn = psycopg2.connect("dbname='postgres' user='dbuser' host='localhost' password=''")
except:
    print "I am unable to connect to the database"