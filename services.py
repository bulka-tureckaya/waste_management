from fastapi import HTTPException
from collections import deque
from models import WasteStorage, Organization, Distance
from typing import List, Tuple

class WasteManagement:
    storages: List[WasteStorage] = []
    organizations: List[Organization] = []
    distances: List[Distance] = []

    @classmethod
    def is_id_unique(cls, id: str) -> bool:
        return not (any(s.id == id for s in cls.storages) or any(o.id == id for o in cls.organizations))

    @classmethod
    def add_storage(cls, storage: WasteStorage):
        if not cls.is_id_unique(storage.id):
            raise HTTPException(status_code=404, detail=f"ID {storage.id} уже существует.")
        cls.storages.append(storage)

    @classmethod
    def add_organization(cls, org: Organization):
        if not cls.is_id_unique(org.id):
            raise HTTPException(status_code=404, detail=f"ID {org.id} уже существует.")
        cls.organizations.append(org)

    @classmethod
    def distance_exists(cls, from_id: int, to_id: int) -> bool:
        return any(d.from_id == from_id and d.to_id == to_id for d in cls.distances) or \
               any(d.from_id == to_id and d.to_id == from_id for d in cls.distances)

    @classmethod
    def add_distance(cls, distance: Distance):
        if any(org.id == distance.from_id for org in cls.organizations) and \
           any(org.id == distance.to_id for org in cls.organizations):
            raise ValueError(f"Нельзя установить дистанцию между организациями с ID {distance.from_id} и {distance.to_id}.")

        if cls.distance_exists(distance.from_id, distance.to_id):
            raise ValueError(f"Distance from {distance.from_id} to {distance.to_id} already exists.")
        
        cls.distances.append(distance)
    
    @classmethod
    def find_nearest_storage(cls, organization: Organization) -> List[Tuple[int, int]]:
        distances = {s.id: float('inf') for s in cls.storages}
        queue = deque()
        
        for distance in cls.distances:
            if distance.from_id == organization.id:
                distances[distance.to_id] = distance.distance
                queue.append(distance.to_id)

        # BFS(Breadth-First Search) для вычисления расстояний
        while queue:
            current_storage_id = queue.popleft()

            for distance in cls.distances:
                if distance.from_id == current_storage_id and distances[current_storage_id] + distance.distance < distances[distance.to_id]:
                    distances[distance.to_id] = distances[current_storage_id] + distance.distance
                    queue.append(distance.to_id)

        # фильтрация и сортировка хранилищ по расстоянию
        sorted_storages = sorted(
            [(storage_id, distances[storage_id]) for storage_id in distances if distances[storage_id] != float('inf')],
            key=lambda x: x[1]
        )
        
        return sorted_storages
    
    @classmethod
    def delete_item(cls, item_id: str):
        org = next((o for o in cls.organizations if o.id == item_id), None)
        storage = next((s for s in cls.storages if s.id == item_id), None)

        if org:
            cls.organizations.remove(org)
        elif storage:
            cls.storages.remove(storage)
        else:
            raise HTTPException(status_code=404, detail=f"Объект с ID {item_id} не найден.")

        # удаляем все дистанции, связанные с данным объектом
        distances_to_remove = []
        
        for d in cls.distances:
            if d.from_id == item_id or d.to_id == item_id:
                distances_to_remove.append(d)

        for d in distances_to_remove:
            cls.distances.remove(d)

        # обновляем записи о дистанциях в оставшихся объектах
        for org in cls.organizations:
            if item_id in org.distances:
                del org.distances[item_id]

        for storage in cls.storages:
            if item_id in storage.distances:
                del storage.distances[item_id]

        print("Оставшиеся дистанции:", cls.distances)

waste_management = WasteManagement()