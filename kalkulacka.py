"""
Jednoducha kalkulacka - vychozi bod pro kurz Git & GitHub.
Tento soubor se bude v prubehu kurzu postupne menit a verzovat.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    """
    Vrátí rozdíl dvou čísel.

    Args:
        a (int/float): Menšenec.
        b (int/float): Menšitel.

    Returns:
        int/float: Výsledek a - b.
    """
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Nelze dělit nulou")
    return a / b

if __name__ == "__main__":
    print("Kalkulacka v0.1")
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
    print("3 * 3 =",multiply(3, 3))
    try:
        print("10 / 0 =", divide(10, 0))
    except ValueError as e:
        print("Chyba:", e)
