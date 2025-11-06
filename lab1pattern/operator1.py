from __future__ import annotations
from typing import Dict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from customer1 import Customer
from bill1 import Bill


class Operator:
    """
    Represents a mobile network operator.

    Attributes:
        id_ (int): Unique identifier of the operator.
        talking_charge (float): Cost per minute of a call.
        message_cost (float): Cost per message.
        network_charge (float): Cost per MB of data.
        discount_rate (int): Discount rate for eligible customers.
        operators (Dict[int, Operator]): Dictionary of assigned operators (optional use).
        bills (Dict[int, Bill]): Dictionary of bills for each customer.
    """

    LIMITING_AMOUNT = 300

    def __init__(self, id_: int, talking_charge: float, message_cost: float,
                 network_charge: float, discount_rate: int):
        """
        Initializes a new operator with given rates and discount.

        Args:
            id_ (int): Operator ID.
            talking_charge (float): Cost per minute for calls.
            message_cost (float): Cost per message.
            network_charge (float): Cost per MB of data.
            discount_rate (int): Discount percentage for eligible customers.
        """
        self.id_ = id_
        self.talking_charge = talking_charge
        self.message_cost = message_cost
        self.network_charge = network_charge
        self.discount_rate = discount_rate
        self.operators: Dict[int, Operator] = {}
        self.bills: Dict[int, Bill] = {}

    def __str__(self):
        """
        Returns a string representation of the operator.

        Returns:
            str: Information about the operator and its rates.
        """
        return (f"Operator id={self.id_} with talking_charge={self.talking_charge}, "
                f"message_cost={self.message_cost}, network_charge={self.network_charge}, "
                f"discount_rate={self.discount_rate}.")

    def assign(self, customer: 'Customer') -> None:
        """
        Assigns this operator to a customer and creates a bill.

        Args:
            customer (Customer): Customer to assign the operator to.
        """
        self.bills[customer.id_] = Bill(limiting_amount=self.LIMITING_AMOUNT)

    def calculate_talking_cost(self, minute: int, customer: 'Customer') -> float:
        """
        Calculates the cost of a voice call for a customer.

        Args:
            minute (int): Duration of the call in minutes.
            customer (Customer): Customer making the call.

        Returns:
            float: Cost of the call after discounts.
        """
        cost = minute * self.talking_charge
        if customer.age < 18 or customer.age > 65:
            cost *= (1 - self.discount_rate / 100)
        self.bills[customer.id_].add(amount=cost)
        return round(cost, 2)

    def calculate_message_cost(self, quantity: int, customer: 'Customer', other: 'Customer',
                               operator: 'Operator') -> float:
        """
        Calculates the cost of sending messages to another customer.

        Args:
            quantity (int): Number of messages to send.
            customer (Customer): Customer sending the messages.
            other (Customer): Customer receiving the messages.
            operator (Operator): Operator used for sending messages.

        Returns:
            float: Cost of messages after discounts (if applicable).
        """
        cost = quantity * self.message_cost
        sending_operator = self.operators.get(operator.id_)
        receiving_operator = other.operators.get(operator.id_)
        if sending_operator and receiving_operator:
            cost *= (1 - self.discount_rate / 100)
        self.bills[customer.id_].add(amount=cost)
        return round(cost, 2)

    def calculate_network_cost(self, amount: float, customer: 'Customer') -> float:
        """
        Calculates the cost of mobile data usage for a customer.

        Args:
            amount (float): Amount of data used in MB.
            customer (Customer): Customer using the data.

        Returns:
            float: Cost of data usage.
        """
        cost = amount * self.network_charge
        self.bills[customer.id_].add(amount=cost)
        return round(cost, 2)


