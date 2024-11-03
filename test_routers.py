from fastapi.testclient import TestClient
from main import app
from models import WasteStorage, Organization
from services import waste_management

client = TestClient(app)

def test_create_storage():
    response = client.post("/storage/", data={
        "id": "1",
        "max_bio_capacity": 100,
        "max_glass_capacity": 100,
        "max_plastic_capacity": 100,
        "bio_capacity": 0,
        "glass_capacity": 0,
        "plastic_capacity": 0
    })
    assert response.status_code == 200
    storage_data = response.json()
    assert storage_data["id"] == "MHO1"
    assert storage_data["max_capacity"]["bio"] == 100

def test_create_organization():
    response = client.post("/organization/", data={
        "id": "1",
        "max_bio_capacity": 50,
        "max_glass_capacity": 50,
        "max_plastic_capacity": 50,
        "bio_capacity": 0,
        "glass_capacity": 0,
        "plastic_capacity": 0
    })
    assert response.status_code == 200
    org_data = response.json()
    assert org_data["id"] == "OO1"
    assert org_data["max_capacity"]["bio"] == 50

def test_set_distance():
    waste_management.add_storage(WasteStorage(id="MHO2", max_capacity={"bio": 100, "glass": 100, "plastic": 100}, current={"bio": 0, "glass": 0, "plastic": 0}))
    waste_management.add_organization(Organization(id="OO2", max_capacity={"bio": 50, "glass": 50, "plastic": 50}, current={"bio": 0, "glass": 0, "plastic": 0}, distances={}))

    response = client.post("/distance/", data={
        "from_id": "OO2",
        "to_id": "MHO2",
        "distance": 10
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Distance set successfully."}

def test_transfer_waste():
    waste_management.add_storage(WasteStorage(id="MHO3", max_capacity={"bio": 100, "glass": 100, "plastic": 100}, current={"bio": 0, "glass": 0, "plastic": 0}))
    waste_management.add_organization(Organization(id="OO3", max_capacity={"bio": 10, "glass": 10, "plastic": 10}, current={"bio": 10, "glass": 10, "plastic": 10}, distances={}))
    
    response = client.post("/distance/", data={
        "from_id": "OO3",
        "to_id": "MHO3",
        "distance": 10
    })

    response = client.post("/transfer/")
    assert response.status_code == 200
    transfer_result = response.json()
    assert "transfer_results" in transfer_result
    assert "bio" in transfer_result["transfer_results"]
    assert transfer_result["transfer_results"]["bio"] == 10

def test_display_results():
    response = client.get("/results/")
    assert response.status_code == 200
