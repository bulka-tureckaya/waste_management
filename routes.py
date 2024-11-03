from fastapi import APIRouter, HTTPException, Form
from models import WasteStorage, CurrentCapacity, Organization, Distance
from services import waste_management
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/organization/")
def create_organization(
    id: str = Form(...),
    max_bio_capacity: int = Form(...),
    max_glass_capacity: int = Form(...),
    max_plastic_capacity: int = Form(...),
    bio_capacity: int = Form(...),
    glass_capacity: int = Form(...),
    plastic_capacity: int = Form(...)
):
    max_capacity = {
        "bio": max_bio_capacity,
        "glass": max_glass_capacity,
        "plastic": max_plastic_capacity
    }
    
    if (bio_capacity > max_bio_capacity or 
        glass_capacity > max_glass_capacity or 
        plastic_capacity > max_plastic_capacity):
        raise HTTPException(status_code=400, detail="Текущие объемы превышают максимальные.")

    current = CurrentCapacity(bio=bio_capacity, glass=glass_capacity, plastic=plastic_capacity)
    org = Organization(id="OO" + id, max_capacity=max_capacity, current=current, distances={})

    waste_management.add_organization(org)
    return org

@router.post("/storage/")
def create_storage(
    id: str = Form(...),
    max_bio_capacity: int = Form(...),
    max_glass_capacity: int = Form(...),
    max_plastic_capacity: int = Form(...),
    bio_capacity: int = Form(...),
    glass_capacity: int = Form(...),
    plastic_capacity: int = Form(...)
):
    max_capacity = {
        "bio": max_bio_capacity,
        "glass": max_glass_capacity,
        "plastic": max_plastic_capacity
    }

    if (bio_capacity > max_bio_capacity or 
        glass_capacity > max_glass_capacity or 
        plastic_capacity > max_plastic_capacity):
        raise HTTPException(status_code=400, detail="Текущие объемы превышают максимальные.")

    current = CurrentCapacity(bio=bio_capacity, glass=glass_capacity, plastic=plastic_capacity)
    storage = WasteStorage(id="MHO" + id, max_capacity=max_capacity, current=current)

    waste_management.add_storage(storage)
    return storage

@router.post("/distance/")
def set_distance(
    from_id: str = Form(...),
    to_id: str = Form(...),
    distance: int = Form(...)
):
    distance_obj = Distance(from_id=from_id, to_id=to_id, distance=distance)
    
    try:
        waste_management.add_distance(distance_obj)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if to_id in [s.id for s in waste_management.storages]:
        for storage in waste_management.storages:
            if storage.id == from_id:
                storage.distances[to_id] = distance
    if from_id in [s.id for s in waste_management.storages]:
        for storage in waste_management.storages:
            if storage.id == to_id:
                storage.distances[from_id] = distance

    for org in waste_management.organizations:
        if org.id == from_id:
            org.distances[to_id] = distance
        elif org.id == to_id:
            org.distances[from_id] = distance

    return {"message": "Distance set successfully."}

transfer_result = {
    "before_sorting": {},
    "transfer_results": {"bio": 0, "glass": 0, "plastic": 0},
    "after_sorting": {}
}

@router.post("/transfer/")
def transfer_waste():
    global transfer_result

    state_before = {
        "organizations": [org.model_dump() for org in waste_management.organizations],
        "storages": [storage.model_dump() for storage in waste_management.storages]
    }

    transfer_results = {"bio": 0, "glass": 0, "plastic": 0}

    for org in waste_management.organizations:
        nearest_storages_with_distance = waste_management.find_nearest_storage(org)

        for storage_id, _ in nearest_storages_with_distance:
            storage = next((s for s in waste_management.storages if s.id == storage_id), None)
            if storage is None:
                continue

            for waste_type, amount in org.current.model_dump().items():
                if amount > 0:
                    can_transfer = min(storage.available_capacity.get(waste_type, 0), amount)
                    if can_transfer > 0:
                        storage.current.__setattr__(waste_type, storage.current.model_dump()[waste_type] + can_transfer)
                        org.current.__setattr__(waste_type, org.current.model_dump()[waste_type] - can_transfer)
                        transfer_results[waste_type] += can_transfer

    state_after = {
        "organizations": [org.model_dump() for org in waste_management.organizations],
        "storages": [storage.model_dump() for storage in waste_management.storages]
    }

    transfer_result = {
        "before_sorting": state_before,
        "transfer_results": transfer_results if any(transfer_results.values()) else {"message": "No waste transferred."},
        "after_sorting": state_after
    }

    return transfer_result

@router.delete("/delete/")
def delete_item(item_id: str):
    try:
        waste_management.delete_item(item_id)
        return {"message": f"Объект с ID {item_id} был успешно удален."}
    except HTTPException as e:
        raise e

@router.get("/results/")
async def display_results(request: Request):
    return templates.TemplateResponse(request, "template.html", {"request": request, **transfer_result})
