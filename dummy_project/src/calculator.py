class Calculator:
    def add(self, a, b):
        """Return the sum of a and b."""
        return a + b

    def minus(self, a, b):
        """Return the difference between a and b."""
        return a - b

    def division(self, a, b):
        """Return the division of a by b. Raise an error if b is zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def multiplication(self, a, b):
        """Return the product of a and b."""
        return a * b

    def percentage(self, part, whole):
        """Return the percentage of part out of whole."""
        if whole == 0:
            raise ValueError("Whole cannot be zero")
        return (part / whole) * 100

    def absolute_value(self, number):
        """Return the absolute value of the number."""
        return abs(number)


if __name__=='__main__':
    # Example usage:
    calc = Calculator()

    # Basic operations
    print(calc.add(10, 5))          # Output: 15
    print(calc.minus(10, 5))        # Output: 5
    print(calc.division(10, 2))     # Output: 5.0
    print(calc.multiplication(10, 5)) # Output: 50

    # Percentage calculation
    print(calc.percentage(20, 200)) # Output: 10.0

    # Absolute value calculation
    print(calc.absolute_value(-10)) # Output: 10
