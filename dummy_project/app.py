from fastapi import FastAPI, HTTPException
from src.validation import Item
from src.car_emi import Car, TataPunch, TataTiago, TataIndica
app = FastAPI()

# In-memory "database"
items_db = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id in items_db:
        return items_db[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/")
def create_item(item: Item):
    item_id = len(items_db) + 1
    emi = None
    if item.name == 'punch':
        punch = TataPunch()
        interest_rate = 5
        loan_period_years = 5
        emi = punch.calculate_emi(interest_rate, loan_period_years)
    elif item.name == 'tiago':
        tiago = TataTiago()
        interest_rate = 5
        loan_period_years = 5
        emi = tiago.calculate_emi(interest_rate, loan_period_years)
    elif item.name == 'indica':
        indica = TataIndica()
        interest_rate = 5
        loan_period_years = 5
        emi = indica.calculate_emi(interest_rate, loan_period_years)
    else:
        raise HTTPException(status_code=400, detail="Invalid car name")

    item.emi = emi
    items_db[item_id] = item
    return {"item_id": item_id, "item": item}

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
