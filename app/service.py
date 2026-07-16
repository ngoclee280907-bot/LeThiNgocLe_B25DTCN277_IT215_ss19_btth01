from sqlalchemy.orm import Session
from typing import Optional, List
from app import models, schemas

def create_warehouse(db: Session, warehouse_in: schemas.WarehouseCreate) -> models.Warehouse:
    db_warehouse = models.Warehouse(**warehouse_in.model_dump())
    try:
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except Exception as e:
        db.rollback()
        raise e

def get_warehouse_by_id(db: Session, warehouse_id: int) -> Optional[models.Warehouse]:
    return db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()

def create_package(db: Session, package_in: schemas.PackageCreate) -> models.Package:
    db_package = models.Package(**package_in.model_dump())
    try:
        db.add(db_package)
        db.commit()
        db.refresh(db_package)
        return db_package
    except Exception as e:
        db.rollback()
        raise e

def get_package_by_id(db: Session, package_id: int) -> Optional[models.Package]:
    return db.query(models.Package).filter(models.Package.id == package_id).first()

def update_package(db: Session, package_id: int, package_in: schemas.PackageUpdate) -> Optional[models.Package]:
    db_package = get_package_by_id(db, package_id)
    if not db_package:
        return None
    try:
        update_data = package_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_package, key, value)
        db.commit()
        db.refresh(db_package)
        return db_package
    except Exception as e:
        db.rollback()
        raise e

def create_waybill(db: Session, waybill_in: schemas.WaybillCreate) -> models.Waybill:
    db_waybill = models.Waybill(**waybill_in.model_dump())
    try:
        db.add(db_waybill)
        db.commit()
        db.refresh(db_waybill)
        return db_waybill
    except Exception as e:
        db.rollback()
        raise e

def get_waybill_by_id(db: Session, waybill_id: int) -> Optional[models.Waybill]:
    return db.query(models.Waybill).filter(models.Waybill.id == waybill_id).first()

def delete_waybill(db: Session, waybill_id: int) -> bool:
    db_waybill = get_waybill_by_id(db, waybill_id)
    if not db_waybill:
        return False
    try:
        db.delete(db_waybill)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
