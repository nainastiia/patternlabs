from customer1 import Customer
from operator1 import Operator

def main():
    """
    Demonstrates the interaction between Customers and Operators.

    Steps performed:
    1. Create Operator instances with specific rates and discount rates.
    2. Create Customer instances with age and unique IDs.
    3. Assign operators to customers.
    4. Display information about customers and their assigned operators.
    5. Simulate talking (voice calls) between customers.
    6. Simulate sending messages between customers.
    7. Simulate mobile data usage (internet) for customers.
    8. Demonstrate paying bills.
    9. Demonstrate changing assigned operators.
    10. Demonstrate changing bill limits.
    """
    print("\nCreating operators:")
    operators = [
        Operator(0, talking_charge=1.5, message_cost=0.5, network_charge=0.1, discount_rate=20),
        Operator(1, talking_charge=2.0, message_cost=0.4, network_charge=0.15, discount_rate=10),
    ]
    for o in operators:
        print(o)

    print("\nCreating customers:")
    customers = [
        Customer(0, "Ivan", 25),
        Customer(1, "Olia", 17),
        Customer(2, "Petro", 70),
    ]
    for c in customers:
        print(c)

    print("\nSet operators:")
    customers[0].set_operator(operators[0])
    customers[1].set_operator(operators[1])
    customers[1].set_operator(operators[0])
    customers[2].set_operator(operators[1])

    print("\nInformation:")
    for c in customers:
        print(c.name, c.age, "Operators:", list(c.operators.keys()))

    # 3. Talking
    print("\nTalking:")
    customers[0].talk(10, customers[1], operator_id=0)
    customers[1].talk(10, customers[0], operator_id=0)

    # 4. Messages
    print("\nMessages:")
    customers[1].message(5, customers[2], operator_id=0)
    customers[2].message(5, customers[1], operator_id=1)

    # 5. Internet
    print("\nInternet:")
    customers[2].connection(100, operator_id=1)
    customers[0].connection(500, operator_id=0)

    # 6. Pay bills
    print("\nPay bill:")
    customers[0].pay_bill(operator_id=0, amount=20)
    customers[1].pay_bill(operator_id=0, amount=40)

    # 7. Change operator
    print("\nChange operator:")
    customers[0].set_operator(operators[1])
    customers[2].set_operator(operators[0])

    # 8. Change bill limit
    print("\nChange bill limit:")
    customers[0].change_bill_limit(500, operator_id=1)
    customers[1].change_bill_limit(250, operator_id=0)


if __name__ == "__main__":
    main()
