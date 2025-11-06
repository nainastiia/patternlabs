from typing import Any, List, Optional
from datatypes import Column, Row
from factory import Database  # used for FK checks

class Table:
    """Table supporting CRUD operations and primary/foreign key constraints."""

    def __init__(self, name: str, columns: List[Column]):
        """
        Initialize a table.

        Args:
            name (str): Table name.
            columns (List[Column]): List of columns in the table.
        """
        self.name = name
        self.columns = {c.name: c for c in columns}
        self.rows: List[Row] = []

    # ---- CREATE ----
    def insert(self, row_data: dict[str, Any]) -> Row:
        """
        Insert a new row with type, PK, and FK validation.

        Args:
            row_data (dict): Column-value mapping for the new row.

        Returns:
            Row: Inserted row instance.

        Raises:
            ValueError: If validation fails or keys are violated.
        """
        for col_name, column in self.columns.items():
            value = row_data.get(col_name)
            if not column.validate(value):
                raise ValueError(f"Invalid value for column '{col_name}': {value}")

        # Check primary key
        pk_col = self.get_primary_key()
        if pk_col and pk_col.name in row_data:
            for r in self.rows:
                if r[pk_col.name] == row_data[pk_col.name]:
                    raise ValueError(f"Duplicate primary key '{pk_col.name}' value")

        # Check foreign keys
        for col in self.columns.values():
            if col.foreign_key and row_data.get(col.name) is not None:
                ref_table_name, ref_col_name = col.foreign_key
                ref_table = Database().get_table(ref_table_name)
                if all(r[ref_col_name] != row_data[col.name] for r in ref_table.get_all()):
                    raise ValueError(f"Foreign key violation on column '{col.name}'")

        row = Row(row_data)
        self.rows.append(row)
        return row

    # ---- READ ----
    def get_all(self) -> List[Row]:
        """Return all rows in the table."""
        return self.rows

    def get_by_id(self, row_id: int) -> Optional[Row]:
        """Return a row by its id, or None if not found."""
        return next((r for r in self.rows if r.id == row_id), None)

    # ---- UPDATE ----
    def update(self, row_id: int, new_data: dict[str, Any]):
        """
        Update a row by id with new data after validation.

        Args:
            row_id (int): ID of the row to update.
            new_data (dict): Column-value mapping to update.

        Raises:
            ValueError: If row not found, column invalid, or value invalid.
        """
        row = self.get_by_id(row_id)
        if not row:
            raise ValueError(f"No row with id={row_id}")

        for key, value in new_data.items():
            if key not in self.columns:
                raise ValueError(f"Column '{key}' does not exist")
            column = self.columns[key]
            if not column.validate(value):
                raise ValueError(f"Invalid value for column '{key}': {value}")
            row[key] = value

    # ---- DELETE ----
    def delete(self, row_id: int):
        """
        Delete a row by id.

        Args:
            row_id (int): ID of the row to delete.
        """
        row = self.get_by_id(row_id)
        if row:
            self.rows.remove(row)

    # ---- Helpers ----
    def get_primary_key(self) -> Optional[Column]:
        """Return the primary key column if it exists, else None."""
        for c in self.columns.values():
            if c.primary_key:
                return c
        return None

    def to_dict(self) -> dict:
        """Return a dictionary representation of the table for JSON serialization."""
        return {
            "name": self.name,
            "columns": [
                {
                    "name": c.name,
                    "type": c.data_type.__class__.__name__,
                    "nullable": c.nullable,
                    "primary_key": c.primary_key,
                    "foreign_key": c.foreign_key,
                }
                for c in self.columns.values()
            ],
            "rows": [r.to_dict() for r in self.rows],
        }

    @staticmethod
    def from_dict(data: dict, type_registry: dict[str, Any]):
        """
        Create a Table instance from a dictionary.

        Args:
            data (dict): Table data as dictionary.
            type_registry (dict): Mapping from type name to DataType class.

        Returns:
            Table: Reconstructed table instance.
        """
        columns = []
        for c in data["columns"]:
            dtype_class = type_registry[c["type"]]
            dtype = dtype_class() if c["type"] != "StringType" else dtype_class(None)
            columns.append(
                Column(
                    c["name"],
                    dtype,
                    nullable=c["nullable"],
                    primary_key=c["primary_key"],
                    foreign_key=c["foreign_key"],
                )
            )
        table = Table(data["name"], columns)
        table.rows = [Row.from_dict(r) for r in data["rows"]]
        return table
