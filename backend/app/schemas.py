from pydantic import BaseModel, EmailStr


# =========================================================
# USER REGISTRATION
# =========================================================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# =========================================================
# USER RESPONSE
# =========================================================

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# =========================================================
# USER LOGIN
# =========================================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =========================================================
# JWT TOKEN RESPONSE
# =========================================================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================================================
# CREATE POST
# =========================================================

class PostCreate(BaseModel):
    title: str
    content: str


# =========================================================
# POST RESPONSE
# =========================================================

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True


# =========================================================
# CREATE COMMENT
# =========================================================

class CommentCreate(BaseModel):
    content: str


# =========================================================
# COMMENT RESPONSE
# =========================================================

class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    class Config:
        from_attributes = True


# =========================================================
# VOTE
# =========================================================

class VoteCreate(BaseModel):
    value: int