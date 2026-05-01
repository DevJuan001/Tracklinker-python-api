from app.features.warranties.warranties_repository import WarrantiesRepository
from app.features.warranties.warranties_model import WarrantyUpdate, WarrantiesFilter, CreateWarranty


class WarrantiesService:

    @staticmethod
    def get_all_warranties(filters: WarrantiesFilter):
        error, warranties = WarrantiesRepository.find_all_warranties(filters)
        if error:
            return "Error al obtener las garantías", None
        return None, warranties

    @staticmethod
    def get_warranty_by_id(warranty_incidents_id: int):
        error, warranty = WarrantiesRepository.find_warranty_by_id(
            warranty_incidents_id)
        if error:
            return "Error al obtener la garantía", None
        return None, warranty

    @staticmethod
    def create_warranty(warranty_data: CreateWarranty):
        error, success, message = WarrantiesRepository.create_warranty(
            warranty_data)
        if error:
            return "Error al crear la garantía", None, None
        return None, success, message

    @staticmethod
    def update_warranty(warranty_incidents_id: int, warranty_data: WarrantyUpdate):
        error, success, message = WarrantiesRepository.update_warranty(
            warranty_incidents_id, warranty_data)
        if error:
            return "Error al actualizar la garantía", None, None
        return None, success, message

    @staticmethod
    def delete_warranty(warranty_incidents_id: int):
        error, success, message = WarrantiesRepository.delete_warranty(
            warranty_incidents_id)
        if error:
            return "Error al eliminar la garantía", None, None
        return None, success, message
