"""Models Package Initialization.

Exports all SQLModel entities to facilitate automatic metadata collection for database migrations
and table creation via SQLModel.metadata.create_all().
Uses relative imports within the models package.
"""

from .master import (
    Category,
    DiningTable,
    MenuItem,
    OptionGroup,
    OptionItem,
    Zone,
)

__all__: list[str] = [
    "Zone",
    "DiningTable",
    "Category",
    "MenuItem",
    "OptionGroup",
    "OptionItem",
]
