import os
import random
import time

import psycopg2
import pymongo


def main() -> None:
    # Hotfix: Wait for postgres to boot up
    time.sleep(10)

    # Example configuration for Postgres DB
    pg_conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'default'),
        user=os.environ.get('POSTGRES_USER', 'user'),
        password=os.environ['POSTGRES_PASSWORD'],
        # NOTE: in "real" environment that also should be loaded from env
        host="postgres_db"
    )

    # Some connection to Postgres
    # Based on example from https://www.psycopg.org/docs/usage.html
    cur = pg_conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (random.randint(1, 100), "abc'def"))
    cur.execute("SELECT * FROM test;")
    data = cur.fetchall()
    pg_conn.commit()
    cur.close()

    print(data)

    # Example configuration for MongoDB
    client_mongo = pymongo.MongoClient(
        host="mongo_db", port=27017,
        username=os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'user'),
        password=os.environ['MONGO_INITDB_ROOT_PASSWORD']
    )

    # Test connection to MongoDB
    # Based on https://www.mongodb.com/languages/python and
    # https://pymongo.readthedocs.io/en/stable/tutorial.html
    client_mongo.admin.command('ping')

    mongo_db = client_mongo.test
    print(mongo_db.name)
    print(mongo_db.my_collection)

    item_1 = {
        "name": "Piano",
        "category": "musical instruments",
    }

    item_2 = {
        "name": "Egg",
        "category": "food",
    }

    item_3 = {
        "name": "Bacon",
        "category": "food",
    }

    mongo_db.my_collection.insert_many([item_1, item_2, item_3])
    for item in mongo_db.my_collection.find():
        # This does not give a very legible output
        print(item)


if __name__ == "__main__":
    main()
