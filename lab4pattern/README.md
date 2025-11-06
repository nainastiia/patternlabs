# MiniDB: Міні-Система Керування Базою Даних на Python

---

## Особливості
- Таблиці з колонками різних типів:
  - `IntegerType`, `StringType`, `BooleanType`, `DateType`.
- Підтримка `nullable`, `primary key` та `foreign key`.
- CRUD-операції: `insert`, `get_all`, `get_by_id`, `update`, `delete`.
- Простий SQL-подібний запит через клас `SimpleQuery`.
- Inner join двох таблиць через `JoinedTable`.
- Збереження та завантаження бази даних у форматі JSON.
- Використання `Singleton` для класу `Database` та `Factory Method` для створення таблиць.

---

## Структура файлів
- `datatypes.py` # Типи даних та класи Column/Row
- `table.py` # Клас Table для CRUD
- `query.py` # SimpleQuery та JoinedTable
- `factory.py` # Клас Database з Singleton + Factory Method
- `main.py` # Демонстрація роботи
- `tests.py` # Тести для pytest
- `README.md`

---

## Запуск
- `pytest tests.py`
- `python main.py`