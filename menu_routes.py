from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
from models import MenuItem, Restaurant  # ✅ Make sure Restaurant is imported

router = APIRouter()

# 🧠 Pydantic Models for Menu
class MenuItemCreate(BaseModel):
    name: str
    description: str
    price: float

class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    restaurant_id: int

    class Config:
        orm_mode = True

# 🧠 Pydantic Models for Restaurant
class RestaurantCreate(BaseModel):
    name: str
    cuisine_type: str
    location: str
    rating: float = 0.0

class RestaurantResponse(BaseModel):
    id: int
    name: str
    cuisine_type: str
    location: str
    rating: float

    class Config:
        orm_mode = True

# 🛠 DB Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ POST - Add a New Restaurant
@router.post(
    "/api/restaurants",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Restaurants"]
)
def add_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = Restaurant(**restaurant.dict())
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

# ✅ GET - All Restaurants
@router.get(
    "/api/restaurants",
    response_model=list[RestaurantResponse],
    tags=["Restaurants"]
)
def get_all_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()

# ✅ GET - Single Restaurant by ID
@router.get(
    "/api/restaurants/{restaurant_id}",
    response_model=RestaurantResponse,
    tags=["Restaurants"]
)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# ✅ PUT - Update a Restaurant
@router.put(
    "/api/restaurants/{restaurant_id}",
    response_model=RestaurantResponse,
    tags=["Restaurants"]
)
def update_restaurant(restaurant_id: int, updated_data: RestaurantCreate, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    for key, value in updated_data.dict().items():
        setattr(restaurant, key, value)
    
    db.commit()
    db.refresh(restaurant)
    return restaurant

# ✅ DELETE - Remove a Restaurant
@router.delete(
    "/api/restaurants/{restaurant_id}",
    tags=["Restaurants"]
)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"}

# ✅ GET Menu Items for a Restaurant
@router.get(
    "/api/restaurants/{restaurant_id}/menu",
    response_model=list[MenuItemResponse],
    tags=["Menu"]
)
def get_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    items = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="No menu items found")
    return items

# ✅ POST New Menu Item
@router.post(
    "/api/restaurants/{restaurant_id}/menu",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Menu"]
)
def add_menu_item(restaurant_id: int, item: MenuItemCreate, db: Session = Depends(get_db)):
    new_item = MenuItem(
        name=item.name,
        description=item.description,
        price=item.price,
        restaurant_id=restaurant_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# ✅ PUT (Update) Menu Item
@router.put(
    "/api/restaurants/{restaurant_id}/menu/{item_id}",
    response_model=MenuItemResponse,
    tags=["Menu"]
)
def update_menu_item(restaurant_id: int, item_id: int, item: MenuItemCreate, db: Session = Depends(get_db)):
    menu_item = db.query(MenuItem).filter_by(id=item_id, restaurant_id=restaurant_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    menu_item.name = item.name
    menu_item.description = item.description
    menu_item.price = item.price
    db.commit()
    db.refresh(menu_item)
    return menu_item

# ✅ DELETE Menu Item
@router.delete(
    "/api/restaurants/{restaurant_id}/menu/{item_id}",
    tags=["Menu"]
)
def delete_menu_item(restaurant_id: int, item_id: int, db: Session = Depends(get_db)):
    menu_item = db.query(MenuItem).filter_by(id=item_id, restaurant_id=restaurant_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(menu_item)
    db.commit()
    return {"message": "Menu item deleted successfully"}
