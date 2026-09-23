"""
Jednoducha kalkulacka - vychozi bod pro kurz Git & GitHub.
Tento soubor se bude v průběhu kurzu postupne měnit a verzovat.
Cílem není mít funkční skript, který počítá, ale vyzkoušet si hlavně Git/GitHub verzování.
Autor/Datum: Tomáš Ježek, 09/2026
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

def power(base, exponent):
    """Vrátí základ umocněný na daný exponent (base ** exponent)."""
    return base ** exponent

def modulo(a, b):
    return a % b
    

def run_tests():
    """Jednoduché ověření správnosti funkcí pomocí assert."""
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(3, 3) == 9
    assert divide(10, 2) == 5
    assert power(2, 3) == 8
    assert modulo(2, 3) == 1

    try:
        divide(10, 0)
        assert False, "Očekávána výjimka ValueError"
    except ValueError:
        pass

    print("Všechny testy prošly OK")

if __name__ == "__main__":
    print("Kalkulacka v1.0")
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
    print("3 * 3 =",multiply(3, 3))
    try:
        print("10 / 0 =", divide(10, 0))
    except ValueError as e:
        print("Chyba:", e)
    print("2 ^ 3 =", power(2, 3))
    print("2 % 3 =", modulo(2, 3))