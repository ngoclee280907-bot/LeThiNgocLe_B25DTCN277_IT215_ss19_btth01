from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, service
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Supply Chain Management API",
    description="FastAPI application for managing Warehouses, Packages, and Waybills",
    version="1.0.0"
)

@app.post(
    "/warehouses",
    response_model=schemas.WarehouseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Warehouse"
)
def create_warehouse(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    try:
        return service.create_warehouse(db=db, warehouse_in=warehouse)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create warehouse: {str(e)}"
        )

@app.get(
    "/warehouses/{warehouse_id}",
    response_model=schemas.WarehouseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Warehouse details with Packages"
)
def read_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    db_warehouse = service.get_warehouse_by_id(db=db, warehouse_id=warehouse_id)
    if db_warehouse is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    return db_warehouse

@app.post(
    "/packages",
    response_model=schemas.PackageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Package (Helper API)"
)
def create_package(package: schemas.PackageCreate, db: Session = Depends(get_db)):
    try:
        return service.create_package(db=db, package_in=package)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create package: {str(e)}"
        )

@app.patch(
    "/packages/{package_id}",
    response_model=schemas.PackageResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially update a Package"
)
def update_package(package_id: int, package: schemas.PackageUpdate, db: Session = Depends(get_db)):
    db_package = service.get_package_by_id(db=db, package_id=package_id)
    if db_package is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    try:
        updated_package = service.update_package(db=db, package_id=package_id, package_in=package)
        return updated_package
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update package: {str(e)}"
        )

@app.post(
    "/waybills",
    response_model=schemas.WaybillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Waybill (Helper API)"
)
def create_waybill(waybill: schemas.WaybillCreate, db: Session = Depends(get_db)):
    try:
        return service.create_waybill(db=db, waybill_in=waybill)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create waybill: {str(e)}"
        )

@app.delete(
    "/waybills/{waybill_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a Waybill physically (Hard Delete)"
)
def delete_waybill(waybill_id: int, db: Session = Depends(get_db)):
    db_waybill = service.get_waybill_by_id(db=db, waybill_id=waybill_id)
    if db_waybill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waybill not found"
        )
    try:
        service.delete_waybill(db=db, waybill_id=waybill_id)
        return {"message": f"Waybill with ID {waybill_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete waybill: {str(e)}"
        )
