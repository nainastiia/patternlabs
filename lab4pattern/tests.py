import pytest
from query import SimpleQuery, JoinedTable
from factory import Database
from datatypes import Row

# ---------- Fixtures ----------

@pytest.fixture
def db():
    """Return a singleton test database instance."""
    return Database("TestDB")

@pytest.fixture
def users_table(db):
    """Create and return a 'users' table for testing."""
    schema = {
        "columns": [
            {"name": "id", "type": "int", "nullable": False, "primary_key": True},
            {"name": "name", "type": "string", "nullable": False, "max_length": 50},
            {"name": "age", "type": "int", "nullable": True},
        ]
    }
    return db.create_table_with_factory("users", schema)

@pytest.fixture
def orders_table(db, users_table):
    """Create and return an 'orders' table with foreign key to 'users'."""
    schema = {
        "columns": [
            {"name": "id", "type": "int", "nullable": False, "primary_key": True},
            {"name": "user_id", "type": "int", "nullable": False, "foreign_key": ("users", "id")},
            {"name": "product", "type": "string", "nullable": False, "max_length": 100},
        ]
    }
    return db.create_table_with_factory("orders", schema)

# ---------- CRUD Tests ----------

def test_insert_and_get(users_table):
    """Test inserting rows and retrieving them by ID."""
    users_table.insert({"id": 1, "name": "Alice", "age": 25})
    users_table.insert({"id": 2, "name": "Bob", "age": 30})
    assert len(users_table.get_all()) == 2
    assert users_table.get_by_id(1)["name"] == "Alice"

def test_update_and_delete(users_table):
    """Test updating a row and deleting it."""
    r = users_table.insert({"id": 1, "name": "Alice", "age": 25})
    users_table.update(r.id, {"age": 26})
    assert users_table.get_by_id(r.id)["age"] == 26
    users_table.delete(r.id)
    assert users_table.get_by_id(r.id) is None

def test_primary_key_enforced(users_table):
    """Test that primary key uniqueness is enforced."""
    users_table.insert({"id": 1, "name": "Alice", "age": 25})
    with pytest.raises(ValueError):
        users_table.insert({"id": 1, "name": "Bob", "age": 30})

def test_foreign_key_enforced(users_table, orders_table):
    """Test that foreign key constraints are enforced."""
    users_table.insert({"id": 1, "name": "Alice", "age": 25})
    orders_table.insert({"id": 1, "user_id": 1, "product": "Laptop"})
    with pytest.raises(ValueError):
        orders_table.insert({"id": 2, "user_id": 99, "product": "Phone"})

# ---------- SimpleQuery Tests ----------

def test_simple_query(users_table):
    """Test SimpleQuery filtering and column selection."""
    users_table.insert({"id": 1, "name": "Alice", "age": 25})
    users_table.insert({"id": 2, "name": "Bob", "age": 30})
    query = SimpleQuery(users_table).where("age", ">", 26).select(["id", "name"])
    result = query.execute()
    assert len(result) == 1
    assert result[0]["name"] == "Bob"

def test_order_by(users_table):
    """Test SimpleQuery ordering by column."""
    users_table.insert({"id": 1, "name": "Alice", "age": 25})
    users_table.insert({"id": 2, "name": "Bob", "age": 30})
    users_table.insert({"id": 3, "name": "Charlie", "age": 20})
    query = SimpleQuery(users_table).order_by("age")
    result = query.execute()
    assert result[0]["name"] == "Charlie"
    assert result[2]["name"] == "Bob"

# ---------- JoinedTable Tests ----------

def test_inner_join(users_table, orders_table):
    """Test inner join between users and orders tables."""
    users_table.insert({"id": 1, "name": "Alice", "age": 25})
    users_table.insert({"id": 2, "name": "Bob", "age": 30})
    orders_table.insert({"id": 1, "user_id": 1, "product": "Laptop"})
    orders_table.insert({"id": 2, "user_id": 2, "product": "Phone"})
    joined = JoinedTable(users_table, orders_table, "id", "user_id").execute()
    assert len(joined) == 2
    assert joined[0]["name"] == "Alice"
    assert joined[1]["product"] == "Phone"

# ---------- JSON Persistence Tests ----------

def test_save_load_json(tmp_path):
    """Test saving and loading database to/from JSON."""
    Row._id_counter = 1
    db = Database("JsonDB")
    db.tables.clear()
    schema = {
        "columns": [
            {"name": "id", "type": "int", "nullable": False, "primary_key": True},
            {"name": "name", "type": "string", "nullable": False, "max_length": 50},
        ]
    }
    table = db.create_table_with_factory("users", schema)
    table.insert({"id": 1, "name": "Alice"})

    filepath = tmp_path / "db.json"
    db.save_to_json(filepath)
    db.load_from_json(filepath)
    users2 = db.get_table("users")
    row = users2.get_by_id(1)
    assert row is not None
    assert row["name"] == "Alice"

    new_row = users2.insert({"id": 2, "name": "Bob"})
    assert new_row.id != row.id
    assert users2.get_by_id(2)["name"] == "Bob"

