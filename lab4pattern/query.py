from typing import Any, List, Optional
from datatypes import Row
from table import Table

# ---------- SimpleQuery ----------

class SimpleQuery:
    """Simple query system for a table: SELECT, WHERE, ORDER BY."""

    def __init__(self, table: Table):
        """
        Initialize a query for a given table.

        Args:
            table (Table): The table to query.
        """
        self.table = table
        self.selected_columns: Optional[List[str]] = None
        self.filter_conditions = []
        self.sort_column = None
        self.sort_ascending = True

    def select(self, columns: List[str]):
        """Specify columns to select."""
        self.selected_columns = columns
        return self

    def where(self, column: str, operator: str, value: Any):
        """Add a filter condition."""
        self.filter_conditions.append((column, operator, value))
        return self

    def order_by(self, column: str, ascending: bool = True):
        """Specify sorting column and order."""
        self.sort_column = column
        self.sort_ascending = ascending
        return self

    def execute(self) -> List[Row]:
        """
        Execute the query.

        Returns:
            List[Row]: Filtered, sorted, and optionally column-selected rows.
        """
        results = []

        # 1. Filtering
        filtered_rows = []
        for row in self.table.get_all():
            match = True
            for col, op, val in self.filter_conditions:
                r_val = row[col]
                if op == "=" and r_val != val:
                    match = False
                    break
                elif op == ">" and not (r_val > val):
                    match = False
                    break
                elif op == "<" and not (r_val < val):
                    match = False
                    break
            if match:
                filtered_rows.append(row)

        # 2. Sorting
        if self.sort_column:
            filtered_rows.sort(
                key=lambda r: r[self.sort_column],
                reverse=not self.sort_ascending,
            )

        # 3. Column selection
        for row in filtered_rows:
            if self.selected_columns:
                filtered_data = {
                    col: row[col] for col in self.selected_columns if col in row.data
                }
                results.append(Row(filtered_data))
            else:
                results.append(row)

        return results


# ---------- JoinedTable ----------

class JoinedTable:
    """Inner join of two tables."""

    def __init__(self, left: Table, right: Table, left_col: str, right_col: str):
        """
        Initialize an inner join between two tables.

        Args:
            left (Table): Left table.
            right (Table): Right table.
            left_col (str): Column from the left table to join on.
            right_col (str): Column from the right table to join on.
        """
        self.left = left
        self.right = right
        self.left_col = left_col
        self.right_col = right_col

    def execute(self) -> List[dict]:
        """
        Perform inner join and return merged rows as dictionaries.

        Returns:
            List[dict]: List of joined rows combining both tables' data.
        """
        joined = []
        for left_row in self.left.get_all():
            for right_row in self.right.get_all():
                if left_row[self.left_col] == right_row[self.right_col]:
                    joined.append({**left_row.data, **right_row.data})
        return joined
