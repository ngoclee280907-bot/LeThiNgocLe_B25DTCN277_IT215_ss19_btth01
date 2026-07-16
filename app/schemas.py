from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class WarehouseBase(BaseModel):
    warehouse_name: str
    location: str

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class PackageBase(BaseModel):
    package_code: str
    weight: float
    warehouse_id: int

class PackageCreate(PackageBase):
    pass

class PackageResponse(PackageBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None

class WaybillBase(BaseModel):
    tracking_number: str
    shipping_status: str
    package_id: int

class WaybillCreate(WaybillBase):
    pass

class WaybillResponse(WaybillBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class WarehouseDetailResponse(WarehouseResponse):
    packages: List[PackageResponse] = []
