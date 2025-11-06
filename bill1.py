from typing import Dict

class Bill:
    """
    Represents a customer's bill with a limiting amount and current debt.

    Attributes:
        limiting_amount (float): Maximum allowed debt.
        current_debt (float): Current amount of debt.
        bills (Dict[int, Bill]): Optional dictionary to store bills (if needed).
    """

    def __init__(self, limiting_amount: float):
        """
        Initializes a new bill with a limiting amount.

        Args:
            limiting_amount (float): Maximum allowed debt for this bill.
        """
        self.limiting_amount = limiting_amount
        self.current_debt = 0.0
        self.bills: Dict[int, Bill] = {}

    def check(self, amount: float) -> bool:
        """
        Checks if adding a certain amount would exceed the limit.

        Args:
            amount (float): Amount to check.

        Returns:
            bool: True if the new amount does not exceed the limit, False otherwise.
        """
        return (self.current_debt + amount) <= self.limiting_amount

    def add(self, amount: float):
        """
        Adds an amount to the current debt if it does not exceed the limit.

        Args:
            amount (float): Amount to add to debt.
        """
        if self.check(amount):
            self.current_debt += amount
        else:
            print("Limit exceeded! Cannot add debt.")

    def pay(self, amount: float):
        """
        Pays off part of the debt.

        Args:
            amount (float): Amount to pay.
        """
        self.current_debt = max(0.0, self.current_debt - amount)

    def change_limit(self, amount: float):
        """
        Changes the limiting amount of the bill.

        Args:
            amount (float): New limiting amount.
        """
        self.limiting_amount = amount

    def get_limiting_amount(self) -> float:
        """
        Returns the limiting amount of the bill.

        Returns:
            float: Limiting amount.
        """
        return self.limiting_amount

    def get_current_debt(self) -> float:
        """
        Returns the current debt amount.

        Returns:
            float: Current debt.
        """
        return self.current_debt
