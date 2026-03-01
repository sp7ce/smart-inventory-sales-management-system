"""Export MySQL data to CSV files for Pandas analysis.

Run from the smart_inventory root:
    python analytics/export_data.py
"""

import csv
import os
import sys

# Add parent to path so we can import from database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import get_connection

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")


def ensure_output_dir() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def export_table(table_name: str, query: str, headers: list[str]) -> str:
    """Export a query result set to CSV and return the file path."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    filepath = os.path.join(OUTPUT_DIR, f"{table_name}.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"  ✓ {table_name}.csv  ({len(rows)} rows)")
    return filepath


def main() -> None:
    ensure_output_dir()
    print("Exporting data to CSV …\n")

    export_table(
        "products",
        "SELECT id, name, category, price, quantity_in_stock FROM products",
        ["id", "name", "category", "price", "quantity_in_stock"],
    )

    export_table(
        "customers",
        "SELECT id, name, email FROM customers",
        ["id", "name", "email"],
    )

    export_table(
        "orders",
        "SELECT id, customer_id, order_date FROM orders",
        ["id", "customer_id", "order_date"],
    )

    export_table(
        "order_items",
        "SELECT id, order_id, product_id, quantity, unit_price FROM order_items",
        ["id", "order_id", "product_id", "quantity", "unit_price"],
    )

    print("\nDone! Files saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
