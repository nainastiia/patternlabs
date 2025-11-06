from __future__ import annotations
from typing import Dict
from operator1 import Operator

class Customer:
    """
    Represents a mobile network customer.

    Attributes:
        id_ (int): Unique identifier of the customer.
        name (str): Name of the customer.
        age (int): Age of the customer.
        operators (Dict[int, Operator]): Dictionary of operators assigned to the customer.
    """

    def __init__(self, id_: int, name: str, age: int):
        """
        Initializes a new customer.

        Args:
            id_ (int): Unique identifier of the customer.
            name (str): Name of the customer.
            age (int): Age of the customer.
        """
        self.id_ = id_
        self.name = name
        self.age = age
        self.operators: Dict[int, Operator] = {}

    def __str__(self):
        """
        Returns a string representation of the customer.

        Returns:
            str: String containing customer id, name, and age.
        """
        return f"Customer id={self.id_}, name={self.name}, age={self.age}."

    def talk(self, minute: int, other: 'Customer', operator_id: int):
        """
        Performs a voice call to another customer using a specific operator.

        Args:
            minute (int): Duration of the call in minutes.
            other (Customer): The customer who is receiving the call.
            operator_id (int): ID of the operator to use for the call.
        """
        operator: Operator = self.operators.get(operator_id)
        if operator:
            cost = operator.calculate_talking_cost(minute, self)
            print(f"{self.name} talked to {other.name} for {minute} min, cost={cost:.2f}")

    def message(self, quantity: int, other: 'Customer', operator_id: int) -> None:
        """
        Sends messages to another customer using a specific operator.

        Args:
            quantity (int): Number of messages to send.
            other (Customer): The customer receiving the messages.
            operator_id (int): ID of the operator to use for sending messages.
        """
        operator: Operator = self.operators.get(operator_id)
        if operator:
            cost = operator.calculate_message_cost(quantity, self, other, operator)
            print(f"{self.name} sent {quantity} messages to {other.name}, cost={cost:.2f}")
        else:
            print(f"No such operator with ID = {operator_id}")

    def connection(self, amount: float, operator_id: int) -> None:
        """
        Uses mobile data via a specific operator.

        Args:
            amount (float): Amount of data used in MB.
            operator_id (int): ID of the operator to use.
        """
        operator: Operator = self.operators.get(operator_id)
        if operator:
            cost = operator.calculate_network_cost(amount, self)
            print(f"{self.name} used {amount} MB, cost={cost:.2f}")
        else:
            print(f"No such operator with ID = {operator_id}")

    def set_operator(self, new_operator: Operator):
        """
        Assigns a new operator to the customer.

        Args:
            new_operator (Operator): Operator object to assign.
        """
        new_operator.assign(self)
        self.operators[new_operator.id_] = new_operator
        print(f"Customer {self.name} set operator {new_operator.id_}")

    def pay_bill(self, operator_id: int, amount: float) -> None:
        """
        Pays a bill to a specific operator.

        Args:
            operator_id (int): ID of the operator.
            amount (float): Amount to pay.
        """
        operator = self.operators.get(operator_id)
        if operator:
            bill = operator.bills[self.id_]
            bill.pay(amount)
            print(f"{self.name} paid {amount:.2f} to operator {operator.id_}")
        else:
            print(f"No such operator with ID = {operator_id}")

    def change_bill_limit(self, new_limit: float, operator_id: int):
        """
        Changes the billing limit for a specific operator.

        Args:
            new_limit (float): New billing limit.
            operator_id (int): ID of the operator.
        """
        operator: Operator = self.operators.get(operator_id)
        if operator:
            operator.bills[self.id_].change_limit(new_limit)
            print(f"Customer {self.name} changed limit to {new_limit:.2f}")
        else:
            print(f"No such operator with ID = {operator_id}")

