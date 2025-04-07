from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
from models import Restaurant
from menu_routes import RestaurantCreate, RestaurantResponse

router = APIRouter(tags=["Restaurants"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create a restaurant
@router.post("/api/restaurants", status_code=status.HTTP_201_CREATED, response_model=RestaurantResponse)
def add_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = Restaurant(
        name=restaurant.name,
        cuisine_type=restaurant.cuisine_type,
        location=restaurant.location,
        rating=restaurant.rating
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

# ✅ Get a single restaurant by ID
@router.get("/api/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# ✅ Get all restaurants OR filter by cuisine, rating, or location
@router.get("/api/restaurants", response_model=List[RestaurantResponse], status_code=status.HTTP_200_OK)
def get_restaurants(
    db: Session = Depends(get_db),
    cuisine: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None),
    location: Optional[str] = Query(None)
):
    query = db.query(Restaurant)

    if cuisine:
        query = query.filter(Restaurant.cuisine_type.ilike(f"%{cuisine}%"))
    if min_rating:
        query = query.filter(Restaurant.rating >= min_rating)
    if location:
        query = query.filter(Restaurant.location.ilike(f"%{location}%"))

    restaurants = query.all()

    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")

    return restaurants
