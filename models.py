from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cuisine_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    rating = Column(Float, default=0.0)

    # ✅ Use correct table name "menu_items"
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")

class MenuItem(Base):  # ✅ Use "MenuItem" instead of "Menu"
    __tablename__ = "menu_items"  # ✅ Correct table name

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)

    restaurant = relationship("Restaurant", back_populates="menu_items")
