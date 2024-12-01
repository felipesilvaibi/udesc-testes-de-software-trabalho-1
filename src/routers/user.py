# src/routers/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session

from auth import authenticate_user, create_access_token, get_password_hash
from database import User, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: constr(min_length=1)
    password: constr(min_length=8)


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
    RF1: O sistema deve permitir o cadastro de novos usuários
    """

    # RF1-RN1: O e-mail deve ser único por usuário
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado",
        )

    # RF1-RN2: A senha precisa ser encriptada antes de ser armazenada
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, name=user.name, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Usuário registrado com sucesso"}


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    RF2: O sistema deve permitir o login de usuários
    """

    # RF2-RN1: O login deve ser realizado com o e-mail e senha cadastrados.
    authenticated_user = authenticate_user(form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": authenticated_user.email})

    return {"access_token": access_token, "token_type": "bearer"}
