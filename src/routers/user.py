# src/routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, constr
from auth import get_password_hash, create_access_token, authenticate_user
from database import get_db, User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Schemas
class UserCreate(BaseModel):
    email: EmailStr  # Garante um formato de e-mail válido
    password: constr(min_length=8)  # Garante senha com no mínimo 8 caracteres

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Endpoints

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar um novo usuário.
    """
    # RN1: Validar se o e-mail já está cadastrado
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    # Criar novo usuário com senha hash
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Usuário registrado com sucesso"}

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para autenticar um usuário e retornar um token JWT.

    Este endpoint espera dados de formulário com os campos 'username' e 'password'.
    """
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Criar token de acesso
    access_token = create_access_token(data={"sub": authenticated_user.email})

    return {"access_token": access_token, "token_type": "bearer"}

