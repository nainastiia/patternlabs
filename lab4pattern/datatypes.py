from datetime import date
from typing import Any, Optional

# ---------- DataType base class and subclasses ----------

class DataType:
    """Base class for all data types."""

    def validate(self, value: Any) -> bool:
        """Check if a value is valid for this type."""
        raise NotImplementedError("Method 'validate' must be implemented")

    def __str__(self):
        return self.__class__.__name__


class IntegerType(DataType):
    """Integer data type."""

    def validate(self, value: Any) -> bool:
        return isinstance(value, int) or value is None


class StringType(DataType):
    """String data type with optional max length."""

    def __init__(self, max_length: Optional[int] = None):
        self.max_length = max_length

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        if not isinstance(value, str):
            return False
        if self.max_length and len(value) > self.max_length:
            return False
        return True


class BooleanType(DataType):
    """Boolean data type."""

    def validate(self, value: Any) -> bool:
        return isinstance(value, bool) or value is None


class DateType(DataType):
    """Date data type."""

    def validate(self, value: Any) -> bool:
        return isinstance(value, date) or value is None


# ---------- Column class ----------

class Column:
    """Represents a table column with type, keys, and constraints."""

    def __init__(
        self,
        name: str,
        data_type: DataType,
        nullable: bool = True,
        primary_key: bool = False,
        foreign_key: Optional[tuple[str, str]] = None
    ):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.primary_key = primary_key
        self.foreign_key = foreign_key

    def validate(self, value: Any) -> bool:
        """Check if a value is valid for this column."""
        if value is None and not self.nullable:
            return False
        return self.data_type.validate(value)

    def __repr__(self):
        fk = f", FK={self.foreign_key}" if self.foreign_key else ""
        pk = ", PK" if self.primary_key else ""
        return f"Column({self.name}: {self.data_type}{pk}{fk})"


# ---------- Row class ----------

class Row:
    """Represents a table row with unique id."""

    _id_counter = 1

    def __init__(self, data: dict[str, Any]):
        if "id" in data:
            self.id = data["id"]
        else:
            self.id = Row._id_counter
            Row._id_counter += 1
        self.data = data

    def __getitem__(self, key):
        """Access value by column name: row['name']."""
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return f"Row(id={self.id}, data={self.data})"

    def to_dict(self):
        """Return a dictionary for JSON serialization."""
        return {"id": self.id, "data": self.data}

    @staticmethod
    def from_dict(d: dict[str, Any]):
        """Create a Row object from a dictionary."""
        row = Row.__new__(Row)  # skip __init__
        row.id = int(d["id"])
        row.data = d["data"]
        Row._id_counter = max(Row._id_counter, row.id + 1)
        return row
