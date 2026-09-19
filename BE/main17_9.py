from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True

class ItemPublic(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool 
    
class ItemUpdate(BaseModels):
    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None

class ItemListResponse(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int

_items: list[ItemPublic] = []
_next_id = 1

@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global _next_id
    
    new_item = ItemPublic(
        id = _next_id,
        name = data.name,
        price = data.price,
        in_stock = data.in_stock
    )
    
    _items.append(new_item)
    
    _next_id += 1
    
    return new_item

@app.get("/items", response_model = list[ItemPublic])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return _items[skip: skip + limit]

@app.get("/items", response_model = ItemPublic)
def get_item(item_id: int):
    for item in _items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model = ItemPublic)
def update_item(item_id: int, data: ItemCreate):
    for index, item in enumerate(_items):
        if item.id == item_id:
            update_item = ItemPublic(
                id = item_id,
                name = data.name,
                price = data.price,
                in_stock = data.in_stock
            )
            _items[index] = update_item
            return update_item
    raise HTTPException(status_code = 404, detail = "Not found")

@app.delete("/item/{item_id}", status_code=204)
def delete_item(item_id:int):
    for index, item in enumerate(_items):
        if item.id == item_id:
            if item.id == item_id:
                _items.pop(index)
                return
    raise HTTPException(status_code=404, detail="Not found")

@app.post("/predict/house-price", response_model=HousePricePrediction)
def predict_house_price(data: HousePriceRequest):
    price = (data.area_sqm * 15_000_000) - (data.distance_to_center_km * 5_000_000) + (data.bedrooms * 20_000_000)
    
    final_price = price if price > 0 else 0
    return HousePricePrediction(predicted_price=final_price)

app.mount("/static", StaticFiles(directory="../frontend", html=True), name="static")
