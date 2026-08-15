import requests

BASE_URL = "http://127.0.0.1:5000"


def print_item_card(item):
    """Helper function to print inventory items in a clean card format."""
    print(f"🆔 ID          : {item.get('id')}")
    print(f"📦 Product     : {item.get('product_name')} ({item.get('brands')})")
    print(f"🏷️  Barcode     : {item.get('barcode')}")
    print(f"📊 Stock Level : {item.get('stock')}")
    print(f"💵 Price       : ${item.get('price', 0):.2f}")
    print(f"🌾 Ingredients : {item.get('ingredients_text')}")
    print("-" * 45)


def main():
    while True:
        print("\n--- Inventory Management System ---")
        print("1. View All Items")
        print("2. View Single Item")
        print("3. Add New Item (Fetches from OpenFoodFacts)")
        print("4. Update Item Price/Stock")
        print("5. Delete Item")
        print("6. Search External API directly")
        print("7. Exit")

        choice = input("Select an option: ").strip()

        # 1. View All Items
        if choice == "1":
            res = requests.get(f"{BASE_URL}/inventory")
            if res.status_code == 200:
                items = res.json()
                if not items:
                    print("\n[!] Your inventory is currently empty.")
                else:
                    print("\n" + "=" * 45)
                    print("                CURRENT INVENTORY")
                    print("=" * 45)
                    for item in items:
                        print_item_card(item)
            else:
                print("\n[!] Failed to retrieve inventory from server.")

        # 2. View Single Item
        elif choice == "2":
            item_id = input("Enter Item ID to view: ").strip()
            res = requests.get(f"{BASE_URL}/inventory/{item_id}")
            if res.status_code == 200:
                item = res.json()
                print("\n" + "=" * 45)
                print(f"                ITEM DETAILS (ID: {item_id})")
                print("=" * 45)
                print_item_card(item)
            else:
                print(f"\n[!] Item with ID {item_id} not found.")

        # 3. Add New Item
        elif choice == "3":
            barcode = input("Enter barcode (e.g., 3017620422003): ").strip()
            stock_input = input("Enter stock quantity: ").strip()
            price_input = input("Enter price: ").strip()

            try:
                stock = int(stock_input)
                price = float(price_input)
            except ValueError:
                print(
                    "\n[!] Invalid input format. Stock must be an integer and price must be a number."
                )
                continue

            payload = {"barcode": barcode, "stock": stock, "price": price}

            res = requests.post(f"{BASE_URL}/inventory", json=payload)
            if res.status_code == 201:
                item = res.json()
                print("\n[+] Item successfully added to inventory!")
                print("=" * 45)
                print_item_card(item)
            else:
                print(f"\n[!] Error adding item: {res.json()}")

        # 4. Update Item Price/Stock
        elif choice == "4":
            item_id = input("Enter Item ID to update: ").strip()
            print("Note: Leave input blank if you don't want to change that field.")
            stock_input = input("Enter new stock level: ").strip()
            price_input = input("Enter new price: ").strip()

            payload = {}
            if stock_input:
                try:
                    payload["stock"] = int(stock_input)
                except ValueError:
                    print("\n[!] Invalid stock format.")
                    continue
            if price_input:
                try:
                    payload["price"] = float(price_input)
                except ValueError:
                    print("\n[!] Invalid price format.")
                    continue

            if not payload:
                print("\n[!] No updates provided.")
                continue

            res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
            if res.status_code == 200:
                item = res.json()
                print("\n[+] Item successfully updated!")
                print("=" * 45)
                print_item_card(item)
            else:
                print(f"\n[!] Error updating item: {res.json()}")

        # 5. Delete Item
        elif choice == "5":
            item_id = input("Enter Item ID to delete: ").strip()
            res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
            if res.status_code == 200:
                print(f"\n[+] Item ID {item_id} deleted successfully.")
            else:
                print(f"\n[!] Error deleting item: {res.json()}")

        # 6. Search External API directly
        elif choice == "6":
            barcode = input("Enter barcode to search externally: ").strip()
            res = requests.get(f"{BASE_URL}/external/{barcode}")
            if res.status_code == 200:
                data = res.json()
                print("\n" + "=" * 45)
                print("            EXTERNAL API PRODUCT DATA")
                print("=" * 45)
                print(
                    f"📦 Product     : {data.get('product_name')} ({data.get('brands')})"
                )
                print(f"🏷️  Barcode     : {data.get('barcode')}")
                print(f"🌾 Ingredients : {data.get('ingredients_text')}")
                print("-" * 45)
            else:
                print(
                    f"\n[!] Product with barcode {barcode} not found on OpenFoodFacts."
                )

        # 7. Exit
        elif choice == "7":
            print("\nExiting CLI. Goodbye!")
            break
        else:
            print("\n[!] Invalid choice. Please select an option between 1 and 7.")


if __name__ == "__main__":
    main()
