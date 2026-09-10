from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
app = FastAPI()

def predict_prices(area:float, bedrooms: int, location: str) ->float:
    if location == "hanoi":
        m = 1.3
    elif location == "hcmc":
        m = 1.25
    else:
        m = 1
    price = round((500 + (15 * area) + (50 *bedrooms)) * m)
    return price*1_000_000

@app.get("/predict")
def predict_price(area: float, bedrooms: int, location: str ="other"):
    predicted_price=predict_prices(area, bedrooms, location)
    return {
        "area": area,
        "bedrooms": bedrooms,
        "location": location,
        "price": predicted_price
    }



app.mount("/static", StaticFiles(directory="../FE"), name="static")