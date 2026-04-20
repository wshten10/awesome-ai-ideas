"""
Community - REST API endpoints.
"""
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc
from backend.database.session import get_db
from backend.database.models import User, Pet, CommunityPost, QAQuestion, QAAnswer
from backend.community.models import (
    UserMatchRequest, UserMatchResponse, UserMatch,
    PostCreateRequest, PostResponse, PostListResponse,
    QAQuestionCreate, QAAnswerCreate, QAQuestionResponse, QAQuestionListResponse,
)
from backend.community.engine import user_matcher, content_engine

router = APIRouter()


def _row_to_dict(row):
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


@router.post("/match", response_model=UserMatchResponse)
async def find_matching_users(request: UserMatchRequest, db: AsyncSession = Depends(get_db)):
    """Find matching pet owners based on profile similarity."""
    result = await db.execute(select(User).where(User.id == request.user_id))
    current_user = result.scalar_one_or_none()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user's pets
    pets_result = await db.execute(select(Pet).where(Pet.owner_id == request.user_id))
    user_pets = [{"pet_type": p.pet_type.value, "breed": p.breed} for p in pets_result.scalars().all()]

    # Get all other users with their pets
    all_users_result = await db.execute(select(User).where(User.id != request.user_id).limit(100))
    all_users = []
    for u in all_users_result.scalars().all():
        u_pets_result = await db.execute(select(Pet).where(Pet.owner_id == u.id))
        u_pets = [{"pet_type": p.pet_type.value, "breed": p.breed} for p in u_pets_result.scalars().all()]
        all_users.append({"id": str(u.id), "username": u.username, "avatar_url": u.avatar_url,
                          "location": u.location, "pets": u_pets})

    user_profile = {"id": str(request.user_id), "pets": user_pets, "location": current_user.location}
    matches = user_matcher.find_matches(
        user_profile, all_users, pet_type=request.pet_type, breed=request.breed,
        interests=request.interests, limit=request.limit,
    )

    return UserMatchResponse(
        matches=[UserMatch(**m) for m in matches],
        total_count=len(matches),
    )


@router.post("/posts", response_model=PostResponse)
async def create_post(request: PostCreateRequest, db: AsyncSession = Depends(get_db)):
    """Create a community post."""
    result = await db.execute(select(User).where(User.id == request.author_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    post = CommunityPost(
        author_id=request.author_id, title=request.title, content=request.content,
        post_type=request.post_type, tags=request.tags, images=request.images,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return content_engine.format_post(_row_to_dict(post), {"username": "user", "avatar_url": None})


@router.get("/posts", response_model=PostListResponse)
async def list_posts(
    post_type: Optional[str] = None, tag: Optional[str] = None,
    page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """List community posts with filtering and pagination."""
    stmt = select(CommunityPost).order_by(desc(CommunityPost.created_at))
    if post_type:
        stmt = stmt.where(CommunityPost.post_type == post_type)
    if tag:
        stmt = stmt.where(CommunityPost.tags.contains([tag]))

    # Count total
    from sqlalchemy import func
    count_stmt = select(func.count()).select_from(CommunityPost)
    total = (await db.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)
    result = await db.execute(stmt)
    posts = result.scalars().all()

    formatted = []
    for post in posts:
        author_result = await db.execute(select(User).where(User.id == post.author_id))
        author = author_result.scalar_one_or_none()
        formatted.append(content_engine.format_post(_row_to_dict(post),
                           {"username": author.username if author else "unknown",
                            "avatar_url": author.avatar_url if author else None}))

    return PostListResponse(posts=formatted, total_count=total, has_more=offset + page_size < total)


@router.post("/qa/questions", response_model=QAQuestionResponse)
async def create_question(request: QAQuestionCreate, db: AsyncSession = Depends(get_db)):
    """Create a Q&A question."""
    result = await db.execute(select(User).where(User.id == request.author_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="User not found")

    question = QAQuestion(
        author_id=request.author_id, pet_id=request.pet_id,
        title=request.title, content=request.content,
        tags=request.tags, images=request.images,
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)

    return content_engine.format_question(_row_to_dict(question), {"username": "user"})


@router.get("/qa/questions", response_model=QAQuestionListResponse)
async def list_questions(
    tag: Optional[str] = None, resolved_only: bool = False,
    page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """List Q&A questions."""
    stmt = select(QAQuestion).order_by(desc(QAQuestion.created_at))
    if tag:
        stmt = stmt.where(QAQuestion.tags.contains([tag]))
    if resolved_only:
        stmt = stmt.where(QAQuestion.is_resolved == True)

    from sqlalchemy import func
    total = (await db.execute(select(func.count()).select_from(QAQuestion))).scalar() or 0

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)
    result = await db.execute(stmt)
    questions = result.scalars().all()

    formatted = []
    for q in questions:
        author_result = await db.execute(select(User).where(User.id == q.author_id))
        author = author_result.scalar_one_or_none()

        answers_result = await db.execute(
            select(QAAnswer).where(QAAnswer.question_id == q.id).order_by(QAAnswer.created_at)
        )
        answers = []
        for a in answers_result.scalars().all():
            a_author = (await db.execute(select(User).where(User.id == a.author_id))).scalar_one_or_none()
            answers.append({"content": a.content, "author_username": a_author.username if a_author else "unknown",
                           "is_expert": a.is_expert, "likes_count": a.likes_count, "is_accepted": a.is_accepted,
                           "created_at": a.created_at})

        formatted.append(content_engine.format_question(
            _row_to_dict(q), {"username": author.username if author else "unknown"}, answers))

    return QAQuestionListResponse(questions=formatted, total_count=total, has_more=offset + page_size < total)


@router.post("/qa/questions/{question_id}/answers")
async def create_answer(question_id: UUID, request: QAAnswerCreate, db: AsyncSession = Depends(get_db)):
    """Answer a Q&A question."""
    result = await db.execute(select(QAQuestion).where(QAQuestion.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    answer = QAAnswer(
        question_id=question_id, author_id=request.author_id,
        content=request.content, is_expert=request.is_expert,
    )
    db.add(answer)
    question.answers_count = (question.answers_count or 0) + 1
    if request.is_expert:
        question.expert_answered = True
    await db.commit()
    return {"id": str(answer.id), "status": "created"}
