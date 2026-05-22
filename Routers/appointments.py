from datetime import date
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import (
    get_current_user,
    PermissionChecker
)

from Models.user import User
from Models.appointments import Appointment


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# Doctor Schedule
@router.get("/my-schedule")
def get_my_schedule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(
        PermissionChecker("appointments:view")
    )
):

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == current_user.id,
            Appointment.appointment_date >= date.today()
        )
        .order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        )
        .all()
    )

    return {
        "doctor_id": current_user.id,
        "total_appointments": len(appointments),
        "appointments": appointments
    }


# Get Single Appointment
@router.get("/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(
        PermissionChecker("appointments:view")
    )
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.doctor_id == current_user.id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


# Update Appointment Status
@router.put("/{appointment_id}")
def update_appointment_status(
    appointment_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(
        PermissionChecker("appointments:update")
    )
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.doctor_id == current_user.id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = status

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment updated successfully",
        "appointment": appointment
    }