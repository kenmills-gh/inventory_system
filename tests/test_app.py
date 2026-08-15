import sys
import os
import pytest

# Add the parent directory (root) to sys.path so Python can find app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, inventory_db


@pytest.fixture
def client():
    """Configures a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Reset the mock database array before each test
        inventory_db.clear()
        yield client


def test_get_empty_inventory(client):
    """Test retrieving inventory when the database is empty."""
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_and_get_item(client):
    """Test adding an item via POST and retrieving it via GET."""
    payload = {"barcode": "3017620422003", "stock": 10, "price": 4.99}  # Nutella

    # Post item
    post_res = client.post("/inventory", json=payload)
    assert post_res.status_code == 201
    data = post_res.get_json()
    assert data["product_name"] == "Nutella"
    assert data["stock"] == 10

    # Get all items
    get_res = client.get("/inventory")
    assert get_res.status_code == 200
    items = get_res.get_json()
    assert len(items) == 1
    assert items[0]["id"] == 1


def test_external_helper_route(client):
    """Test the external OpenFoodFacts helper route directly."""
    response = client.get("/external/3017620422003")
    assert response.status_code == 200
    data = response.get_json()
    assert data["product_name"] == "Nutella"


def test_update_item(client):
    """Test updating an item's stock and price via PATCH."""
    # 1. Add an item and grab its generated ID
    post_res = client.post(
        "/inventory", json={"barcode": "3017620422003", "stock": 10, "price": 4.99}
    )
    created_item = post_res.get_json()
    item_id = created_item["id"]

    # 2. Update the item using the dynamic ID
    update_payload = {"stock": 50, "price": 6.99}
    patch_res = client.patch(f"/inventory/{item_id}", json=update_payload)

    assert patch_res.status_code == 200
    updated_data = patch_res.get_json()
    assert updated_data["stock"] == 50
    assert updated_data["price"] == 6.99


def test_del_item(client):
    """Test deleting an item via DELETE."""
    # 1. Add an item and grab its generated ID
    post_res = client.post(
        "/inventory", json={"barcode": "3017620422003", "stock": 10, "price": 4.99}
    )
    created_item = post_res.get_json()
    item_id = created_item["id"]

    # 2. Delete the item using the dynamic ID
    delete_res = client.delete(f"/inventory/{item_id}")
    assert delete_res.status_code == 200

    # 3. Verify it's gone
    get_res = client.get("/inventory")
    assert len(get_res.get_json()) == 0


def test_not_found_errors(client):
    """Test that requesting, updating, or deleting a non-existent item returns 404."""
    # Try to GET an item that doesn't exist
    get_res = client.get("/inventory/999")
    assert get_res.status_code == 404

    # Try to PATCH an item that doesn't exist
    patch_res = client.patch("/inventory/999", json={"stock": 20})
    assert patch_res.status_code == 404

    # Try to DELETE an item that doesn't exist
    delete_res = client.delete("/inventory/999")
    assert delete_res.status_code == 404
