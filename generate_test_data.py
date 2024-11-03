import requests

BASE_URL = "http://127.0.0.1:8000/"

def create_storage(storage_id, max_bio_capacity, max_glass_capacity, max_plastic_capacity, bio_capacity, glass_capacity, plastic_capacity):
    storage_data = {
        "id": storage_id,
        "max_bio_capacity": max_bio_capacity,
        "max_glass_capacity": max_glass_capacity,
        "max_plastic_capacity": max_plastic_capacity,
        "bio_capacity": bio_capacity,
        "glass_capacity": glass_capacity,
        "plastic_capacity": plastic_capacity
    }
    response = requests.post(f"{BASE_URL}/storage/", data=storage_data)
    print(f"Создано хранилище: {response.json() if response.status_code == 200 else response.text}")

def create_organization(org_id, max_bio_capacity, max_glass_capacity, max_plastic_capacity, bio_capacity, glass_capacity, plastic_capacity):
    org_data = {
        "id": org_id,
        "max_bio_capacity": max_bio_capacity,
        "max_glass_capacity": max_glass_capacity,
        "max_plastic_capacity": max_plastic_capacity,
        "bio_capacity": bio_capacity,
        "glass_capacity": glass_capacity,
        "plastic_capacity": plastic_capacity
    }
    response = requests.post(f"{BASE_URL}/organization/", data=org_data)
    print(f"Создана организация: {response.json() if response.status_code == 200 else response.text}")

def set_distance(from_id, to_id, distance):
    distance_data = {
        "from_id": from_id,
        "to_id": to_id,
        "distance": distance
    }
    response = requests.post(f"{BASE_URL}/distance/", data=distance_data)
    print(f"Создана дистанция: {response.json() if response.status_code == 200 else response.text}")

if __name__ == "__main__":
    create_storage("1", 100, 100, 100, 0, 0, 0)
    create_storage("2", 80, 80, 80, 0, 0, 0)

    create_organization("1", 50, 50, 50, 50, 50, 50)
    create_organization("2", 70, 70, 70, 70, 70, 70)

    set_distance("OO1", "MHO1", 10)
    set_distance("OO1", "MHO2", 20)
    set_distance("OO2", "MHO1", 15)
