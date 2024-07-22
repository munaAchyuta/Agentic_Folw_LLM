from src.calculator import Calculator

class Car:
    def __init__(self, name, price, mileage, fuel_type):
        self.name = name
        self.price = price
        self.mileage = mileage
        self.fuel_type = fuel_type

    def calculate_emi(self, interest_rate, loan_period_years):
        """Calculate EMI for the car."""
        loan_period_months = Calculator().multiplication(loan_period_years , 12)
        monthly_interest_rate = Calculator().division(interest_rate, Calculator().multiplication(12 , 100))
        emi = (self.price * monthly_interest_rate * (1 + monthly_interest_rate) ** loan_period_months) / (Calculator().add(1 , monthly_interest_rate) ** loan_period_months - 1)
        return emi

class TataPunch(Car):
    def __init__(self):
        super().__init__(name="Tata Punch", price=700000, mileage=18, fuel_type="Petrol")

class TataTiago(Car):
    def __init__(self):
        super().__init__(name="Tata Tiago", price=600000, mileage=23, fuel_type="Petrol")

class TataIndica(Car):
    def __init__(self):
        super().__init__(name="Tata Indica", price=500000, mileage=20, fuel_type="Diesel")

def main():
    # Example usage:
    punch = TataPunch()
    tiago = TataTiago()
    indica = TataIndica()

    # Calculate EMI for each car with a 5% annual interest rate over 5 years
    interest_rate = 5
    loan_period_years = 5

    print(f"{punch.name} EMI: {punch.calculate_emi(interest_rate, loan_period_years):.2f} INR")
    print(f"{tiago.name} EMI: {tiago.calculate_emi(interest_rate, loan_period_years):.2f} INR")
    print(f"{indica.name} EMI: {indica.calculate_emi(interest_rate, loan_period_years):.2f} INR")

#main()
if __name__=="__main__":
    _ = main()    
