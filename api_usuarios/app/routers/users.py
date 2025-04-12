from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.db_config import get_db
from app.models.schemas import User, UserCreate, UserUpdate
from app.models.user import User as UserModel
from app.auth.auth import get_password_hash, get_current_active_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un usuario con el mismo email
    db_user_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear el nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: UserModel = Depends(get_current_active_user)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/me", response_model=User)
def read_user_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db),
              current_user: UserModel = Depends(get_current_active_user)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_active_user)):
    # Verificar que el usuario actual esté actualizando su propio perfil
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.dict(exclude_unset=True)
    
    # Si se está actualizando la contraseña, hashearla
    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_active_user)):
    # Solo el propio usuario puede eliminar su cuenta
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return None