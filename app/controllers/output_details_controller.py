from datetime import timedelta
from fastapi import HTTPException
from app.repository.output_details_repository import OutputDetailsRepository
from app.models.output_details_model import OutputDetails

class OutputDetailsController:
    
   @staticmethod
   def get_all_outputDetails():
    error, outputDetails = OutputDetailsRepository.find_all_outpuDetails()
    if error:
      raise HTTPException(status_code=400, detail=error)
    return{
      "data":outputDetails
    }
    
   @staticmethod
   def get_outputDetails_by_id(output_details_id:int):
     error, outputDetails = OutputDetailsRepository.find_by_id(output_details_id)
     if error:
       raise HTTPException(status_code=400 , detail=error)
     return{
       "data": outputDetails
     }
   
   @staticmethod
   def create_outputDetails(output_details_data:OutputDetails):
     error, success, message = OutputDetailsRepository.create(output_details_data)
     if error:
       raise HTTPException(status_code=400, detail=error)
     return{
       "success":success,
       "message":message
     }
   
   @staticmethod
   def update_outputDetails(output_details_id:int, output_details_data: dict):
     error, success, message = OutputDetailsRepository.update(output_details_id, output_details_data)
     if error:
       raise HTTPException (status_code=400, detail=error)
     return{
        "success": success,
        "message": message
     }
   
   @staticmethod
   def disable_output(out_order_id:int):
     error, success, message = OutputDetailsRepository.disable(out_order_id)
     if error:
       raise HTTPException(status_code=400, detail=error)
     return{
       "success": success,
       "message": message
     }
   
   @staticmethod
   def enable_output(out_order_id):
      error, success, message = OutputDetailsRepository.enable(out_order_id)
      if error:
         raise HTTPException(status_code=400, detail=error)
      return {
         "success": success,
         "message": message
      }

   @staticmethod
   def get_transformations_by_date_range(start_date: str, end_date: str):
     error, transformations = OutputDetailsRepository.find_transformations_by_date_range(start_date, end_date)
     if error:
       raise HTTPException(status_code=400, detail=error)
     return {
       "data": transformations
     }
   
   @staticmethod
   def get_deleted_transformations_by_date_range(start_date: str, end_date: str):
       error, transformations = OutputDetailsRepository.find_deleted_transformations_by_date_range(start_date, end_date)

       if error:
           raise HTTPException(status_code=404, detail=error)
       
       return{
           "data": transformations
       }
   
   @staticmethod
   def get_all_transformations():
       error, transformations= OutputDetailsRepository.find_all_transformations()
       if error:
           raise HTTPException(status_code=400, detail=error)
       return{
           "data":transformations
       }
   
   @staticmethod
   def get_completed_transformations():
       error, transformations= OutputDetailsRepository.find_completed_transformations()
       if error:
           raise HTTPException(status_code=400, detail=error)
       return{
           "data":transformations
       }