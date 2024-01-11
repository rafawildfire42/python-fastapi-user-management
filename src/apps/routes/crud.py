from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def get_routes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Route).offset(skip).limit(limit).all()


def get_route(db, route_id: int):
    return db.query(models.Route).filter(models.Route.id == route_id).first()


def delete_route(db, route_id: int):
    db_route = db.query(models.Route).filter(
        models.Route.id == route_id).first()

    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")

    db.delete(db_route)
    db.commit()

    response_body = {"message": f"Route #{route_id} deleted."}

    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


def create_route(db, route):
    try:
        db_route = models.Route(
            path=route.path, needs_permission=route.needs_permission)
        db.add(db_route)
        db.commit()
        db.refresh(db_route)
        return db_route
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Router with this name has been registered")


def update_route(db: Session, route: schemas.Route, id: int):
    db_route = db.query(models.Route).filter(models.Route.id == id).first()

    if not db_route:
        raise HTTPException(status_code=404, detail="Route not found")

    for field, value in route.model_dump(exclude_unset=True).items():
        setattr(db_route, field, value)

    db.commit()
    db.refresh(db_route)

    return db_route
