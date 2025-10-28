"""Simple inventory system with safe I/O and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Iterable
import json
import os


@dataclass
class Inventory:
    """In-memory inventory with basic CRUD and reporting."""
    stock: Dict[str, int] = field(default_factory=dict)

    def add_item(self, item: str, qty: int = 0, logs: List[str] | None = None) -> None:
        """Add quantity to an item; creates the item if missing."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError("item must be a non-empty string")
        if not isinstance(qty, int):
            raise TypeError("qty must be int")
        if logs is None:
            logs = []
        self.stock[item] = self.stock.get(item, 0) + qty
        logs.append(f"{datetime.now().isoformat(timespec='seconds')}: Added {qty} of {item}")

    def remove_item(self, item: str, qty: int) -> None:
        """Decrease quantity of an item; removes item if quantity drops to 0 or below."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError("item must be a non-empty string")
        if not isinstance(qty, int):
            raise TypeError("qty must be int")
        current = self.stock.get(item)
        if current is None:
            # No-op: removing a non-existent item is ignored
            return
        new_qty = current - qty
        if new_qty <= 0:
            del self.stock[item]
        else:
            self.stock[item] = new_qty

    def get_qty(self, item: str) -> int:
        """Return quantity for item; 0 if missing."""
        if not isinstance(item, str) or not item.strip():
            raise ValueError("item must be a non-empty string")
        return self.stock.get(item, 0)

    def check_low_items(self, threshold: int = 5) -> List[str]:
        """List items with quantity below threshold."""
        if not isinstance(threshold, int):
            raise TypeError("threshold must be int")
        return [name for name, qty in self.stock.items() if qty < threshold]

    def print_report(self) -> None:
        """Print a simple inventory report."""
        print("Items Report")
        for name, qty in self.stock.items():
            print(f"{name} -> {qty}")

    def load(self, file_path: str = "inventory.json") -> None:
        """Load inventory from JSON file if it exists."""
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path must be a non-empty string")
        if not os.path.exists(file_path):
            # No-op if file does not exist
            return
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, int) for k, v in data.items()):
            raise ValueError("Invalid inventory file format")
        self.stock = dict(data)

    def save(self, file_path: str = "inventory.json") -> None:
        """Save inventory to JSON file."""
        if not isinstance(file_path, str) or not file_path.strip():
            raise ValueError("file_path must be a non-empty string")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.stock, f, ensure_ascii=False, indent=2)


def demo() -> None:
    """Demonstrate basic usage without unsafe calls."""
    inv = Inventory()
    logs: List[str] = []

    inv.add_item("apple", 10, logs=logs)
    inv.add_item("banana", 2, logs=logs)
    # Intentionally add negative to simulate correction/return
    inv.add_item("banana", -2, logs=logs)

    inv.remove_item("apple", 3)
    inv.remove_item("orange", 1)  # non-existent: no error

    print(f"Apple stock: {inv.get_qty('apple')}")
    print(f"Low items: {inv.check_low_items()}")

    inv.save()
    inv.load()
    inv.print_report()

    # Show logs
    for entry in logs:
        print(entry)


if __name__ == "__main__":
    demo()
