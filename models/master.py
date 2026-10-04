"""Master Data Schemas Module for Food Order App.

Defines static domain models including Zones, Dining Tables, Categories,
Menu Items, Option Groups, and Option Items using SQLModel ORM.
Fully compliant with PEP 8 standards, strict type annotations, and relationship references.
"""

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Zone(SQLModel, table=True):
    """Represents a physical dining zone within the restaurant (e.g., Air Conditioned, Outdoor)."""

    __tablename__: str = "zones"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)

    # Relationships (One-to-Many with DiningTable)
    tables: List["DiningTable"] = Relationship(back_populates="zone")


class DiningTable(SQLModel, table=True):
    """Represents a physical dining table assigned to a specific Zone.

    Note: Table numbers may duplicate across different zones.
    """

    __tablename__: str = "dining_tables"

    id: Optional[int] = Field(default=None, primary_key=True)
    table_number: str = Field(index=True, max_length=20)
    capacity: int = Field(default=4)
    is_active: bool = Field(default=True)

    # Foreign Keys
    zone_id: int = Field(foreign_key="zones.id", index=True)

    # Relationships
    zone: Optional[Zone] = Relationship(back_populates="tables")


class Category(SQLModel, table=True):
    """Represents a food or beverage category (e.g., Drinks, Main Course, Desserts)."""

    __tablename__: str = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)

    # Relationships (One-to-Many with MenuItem)
    menu_items: List["MenuItem"] = Relationship(back_populates="category")


class MenuItem(SQLModel, table=True):
    """Represents an individual menu item available for customer ordering."""

    __tablename__: str = "menu_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=150)
    description: Optional[str] = Field(default=None, max_length=500)
    price: float = Field(default=0.0, ge=0.0)
    image_url: Optional[str] = Field(default=None, max_length=500)
    is_available: bool = Field(default=True)

    # Foreign Keys
    category_id: int = Field(foreign_key="categories.id", index=True)

    # Relationships
    category: Optional[Category] = Relationship(back_populates="menu_items")


class OptionGroup(SQLModel, table=True):
    """Represents a group of item customization options (e.g., Spicy Level, Sweetness Level)."""

    __tablename__: str = "option_groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    is_required: bool = Field(default=False)
    max_selectable: int = Field(default=1)

    # Relationships (One-to-Many with OptionItem)
    options: List["OptionItem"] = Relationship(back_populates="option_group")


class OptionItem(SQLModel, table=True):
    """Represents a specific selectable choice within an OptionGroup (e.g., Mild, Extra Spicy (+10 THB))."""

    __tablename__: str = "option_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    extra_price: float = Field(default=0.0, ge=0.0)

    # Foreign Keys
    option_group_id: int = Field(foreign_key="option_groups.id", index=True)

    # Relationships
    option_group: Optional[OptionGroup] = Relationship(back_populates="options")
