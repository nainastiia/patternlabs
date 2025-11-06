import json
from typing import Dict, Any
from datatypes import Column, IntegerType, StringType, BooleanType, DateType

class Database:
    """Singleton database with Factory Method to create tables."""

    _instance = None

    def __new__(cls, name: str = "default_db"):
        """
        Ensure only one instance (Singleton).

        Args:
            name (str): Database name (default: "default_db").

        Returns:
            Database: Singleton instance.
        """
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, name: str = "default_db"):
        """
        Initialize database (only once due to singleton).

        Args:
            name (str): Database name.
        """
        if self._initialized:
            return
        self.name = name
        self.tables: Dict[str, Any] = {}
        self._initialized = True

    # ---- Factory Method ----
    def create_table_with_factory(self, name: str, schema: dict):
        """
        Create a table based on a schema.

        Args:
            name (str): Table name.
            schema (dict): Table schema with column definitions.

        Returns:
            Table: Created table instance.
        """
        from table import Table
        columns = []
        for col_schema in schema["columns"]:
            col_type = col_schema["type"].lower()
            data_type = self._get_data_type(col_type, col_schema)
            column = Column(
                name=col_schema["name"],
                data_type=data_type,
                nullable=col_schema.get("nullable", True),
                primary_key=col_schema.get("primary_key", False),
                foreign_key=col_schema.get("foreign_key", None),
            )
            columns.append(column)

        table = Table(name, columns)
        self._validate_foreign_keys(table)
        self.tables[name] = table
        return table

    def _get_data_type(self, col_type: str, col_schema: dict):
        """Return the appropriate DataType object based on column type."""
        if col_type in ("int", "integer"):
            return IntegerType()
        elif col_type in ("string", "text"):
            return StringType(col_schema.get("max_length"))
        elif col_type == "bool":
            return BooleanType()
        elif col_type == "date":
            return DateType()
        else:
            raise ValueError(f"Unknown data type: {col_type}")

    def _validate_foreign_keys(self, table):
        """Check that all foreign keys reference existing tables and columns."""
        for column in table.columns.values():
            if column.foreign_key:
                ref_table, ref_column = column.foreign_key
                if ref_table not in self.tables:
                    raise ValueError(f"Foreign key error: table '{ref_table}' not found.")
                if ref_column not in self.tables[ref_table].columns:
                    raise ValueError(f"Foreign key error: column '{ref_column}' not found in '{ref_table}'.")

    def get_table(self, name: str):
        """
        Retrieve a table by name.

        Args:
            name (str): Table name.

        Returns:
            Table: Requested table.

        Raises:
            ValueError: If table does not exist.
        """
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist")
        return self.tables[name]

    def save_to_json(self, filepath: str):
        """
        Save the entire database to a JSON file.

        Args:
            filepath (str): Path to JSON file.
        """
        db_data = {
            "name": self.name,
            "tables": [t.to_dict() for t in self.tables.values()],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(db_data, f, indent=4, ensure_ascii=False)

    def load_from_json(self, filepath: str):
        """
        Load database from a JSON file.

        Args:
            filepath (str): Path to JSON file.
        """
        from table import Table
        with open(filepath, "r", encoding="utf-8") as f:
            db_data = json.load(f)
        self.name = db_data["name"]
        self.tables.clear()
        type_registry = {
            "IntegerType": IntegerType,
            "StringType": StringType,
            "BooleanType": BooleanType,
            "DateType": DateType,
        }
        for tdict in db_data["tables"]:
            table = Table.from_dict(tdict, type_registry)
            self.tables[table.name] = table

    def __repr__(self):
        """Return a string representation of the database."""
        return f"<Database name={self.name}, tables={list(self.tables.keys())}>"
