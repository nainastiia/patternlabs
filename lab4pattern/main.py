from factory import Database
from query import SimpleQuery, JoinedTable


def main():
    """
    Demo of a simple in-memory DB using Factory Method.

    Steps:
    1. Create database.
    2. Create 'users' table via factory.
    3. Create 'orders' table with foreign key to 'users'.
    4. Insert sample data (CRUD operations).
    5. Display all users.
    6. Query users older than 23, ordered by age.
    7. Inner join 'users' and 'orders'.
    8. Update and delete users.
    9. Save DB to JSON.
    10. Load DB from JSON.
    """

    # 1. Create database
    db = Database("MyDB")

    # 2. Create 'users' table
    users_schema = {
        "columns": [
            {"name": "id", "type": "int", "nullable": False, "primary_key": True},
            {"name": "name", "type": "string", "nullable": False, "max_length": 50},
            {"name": "age", "type": "int", "nullable": True},
        ]
    }
    users = db.create_table_with_factory("users", users_schema)

    # 3. Create 'orders' table
    orders_schema = {
        "columns": [
            {"name": "id", "type": "int", "nullable": False, "primary_key": True},
            {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "id")},
            {"name": "product", "type": "string", "nullable": False, "max_length": 100},
        ]
    }
    orders = db.create_table_with_factory("orders", orders_schema)

    # 4. Insert sample data
    users.insert({"id": 1, "name": "Alice", "age": 25})
    users.insert({"id": 2, "name": "Bob", "age": 30})
    users.insert({"id": 3, "name": "Charlie", "age": 22})

    orders.insert({"id": 1, "user_id": 1, "product": "Laptop"})
    orders.insert({"id": 2, "user_id": 2, "product": "Phone"})
    orders.insert({"id": 3, "user_id": 3, "product": "Mouse"})
    orders.insert({"id": 4, "user_id": 2, "product": "Computer"})

    # 5. Display all users
    print("\nAll users after insertion")
    for r in users.get_all():
        print(r)

    # 6. Simple query
    print("\nUsers older than 23, ordered by age")
    query = SimpleQuery(users).where("age", ">", 23).order_by("age")
    for r in query.execute():
        print(r)

    # 7. Inner join
    print("\nInner Join: Users + Orders")
    joined = JoinedTable(users, orders, "id", "user_id").execute()
    for row in joined:
        print(row)

    # 8. Update and delete
    users.update(2, {"age": 45})
    users.delete(1)

    print("\nUsers after update/delete")
    for r in users.get_all():
        print(r)

    # 9. Save to JSON
    db.save_to_json("mydb.json")
    print("\nDatabase saved to mydb.json")

    # 10. Load from JSON
    db2 = Database()
    db2.load_from_json("mydb.json")
    print("\nDatabase loaded from mydb.json")


if __name__ == "__main__":
    main()

