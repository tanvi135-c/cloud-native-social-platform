from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Post, Comment, Vote
from app.schemas import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
    PostCreate,
    PostResponse,
    CommentCreate,
    CommentResponse,
    VoteCreate
)
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


router = APIRouter()


# =========================================================
# USER REGISTRATION
# =========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) |
        (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================================
# USER LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# CREATE POST
# =========================================================

@router.post(
    "/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED
)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# =========================================================
# GET ALL POSTS
# =========================================================

@router.get(
    "/posts",
    response_model=list[PostResponse]
)
def get_posts(
    db: Session = Depends(get_db)
):
    posts = db.query(Post).order_by(
        Post.created_at.desc()
    ).all()

    return posts


# =========================================================
# GET SINGLE POST
# =========================================================

@router.get(
    "/posts/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


# =========================================================
# UPDATE POST
# =========================================================

@router.put(
    "/posts/{post_id}",
    response_model=PostResponse
)
def update_post(
    post_id: int,
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own posts"
        )

    post.title = post_data.title
    post.content = post_data.content

    db.commit()
    db.refresh(post)

    return post


# =========================================================
# DELETE POST
# =========================================================

@router.delete(
    "/posts/{post_id}"
)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own posts"
        )

    db.delete(post)
    db.commit()

    return {
        "message": "Post deleted successfully"
    }


# =========================================================
# CREATE COMMENT
# =========================================================

@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    comment = Comment(
        content=comment_data.content,
        user_id=current_user.id,
        post_id=post_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# =========================================================
# GET COMMENTS
# =========================================================

@router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(
        Comment.created_at.asc()
    ).all()

    return comments
# =========================================================
# VOTE ON POST
# =========================================================

@router.post("/posts/{post_id}/vote")
def vote_on_post(
    post_id: int,
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate vote value
    if vote_data.value not in [1, -1]:
        raise HTTPException(
            status_code=400,
            detail="Vote value must be 1 or -1"
        )

    # Check post
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    # Check existing vote
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.post_id == post_id
    ).first()

    if existing_vote:
        # Update existing vote
        existing_vote.value = vote_data.value
    else:
        # Create new vote
        new_vote = Vote(
            value=vote_data.value,
            user_id=current_user.id,
            post_id=post_id
        )

        db.add(new_vote)

    db.commit()

    return {
        "message": "Vote recorded successfully",
        "post_id": post_id,
        "vote": vote_data.value
    }


# =========================================================
# GET POST VOTE COUNT
# =========================================================

@router.get("/posts/{post_id}/votes")
def get_post_votes(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    upvotes = db.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.value == 1
    ).count()

    downvotes = db.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.value == -1
    ).count()

    return {
        "post_id": post_id,
        "upvotes": upvotes,
        "downvotes": downvotes,
        "score": upvotes - downvotes
    }