from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mock Database Array
inventory_db = []
next_id = 1

OPEN_FOOD_FACTS_API = "https://world.openfoodfacts.org/api/v0/product/{}.json"


def fetch_external_product(barcode):
    """Helper function to fetch from OpenFoodFacts API with headers and debugging"""
    url = OPEN_FOOD_FACTS_API.format(barcode)
    # OpenFoodFacts requires a custom User-Agent identifying the app
    headers = {"User-Agent": "InventoryManagementSystem - Python - Version 1.0"}

    try:
        response = requests.get(url, headers=headers)
        print(f"DEBUG: Status Code: {response.status_code}")
        print(
            f"DEBUG: Response JSON: {response.text[:200]}..."
        )  # Print first 200 chars

        if response.status_code == 200:
            data = response.json()
            # OpenFoodFacts returns status 1 if product is found
            if data.get("status") == 1:
                product = data.get("product", {})
                return {
                    "product_name": product.get("product_name", "Unknown"),
                    "brands": product.get("brands", "Unknown"),
                    "ingredients_text": product.get("ingredients_text", "Not listed"),
                }
    except Exception as e:
        print(f"DEBUG: Exception occurred: {e}")

    return None


@app.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory_db), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in inventory_db if i["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id
    data = request.json
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400

    # Fetch external data
    external_data = fetch_external_product(barcode)
    if not external_data:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404

    # Merge data and save
    new_item = {
        "id": next_id,
        "barcode": barcode,
        "stock": data.get("stock", 0),
        "price": data.get("price", 0),
    }
    new_item.update(external_data)

    inventory_db.append(new_item)
    next_id += 1

    return jsonify(new_item), 201


if __name__ == "__main__":
    app.run(debug=True)
