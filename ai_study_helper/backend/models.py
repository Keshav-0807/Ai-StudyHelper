from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from conf import db
from typing import Optional, List
from datetime import datetime

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    # cascade="all, delete-orphan" ensures Results are deleted when User is deleted
    results: Mapped[List["Results"]] = relationship(
        "Results", back_populates="user", cascade="all, delete-orphan"
    )

class Results(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    correct_ans_count: Mapped[int] = mapped_column(default=0)
    total_ques_count: Mapped[int] = mapped_column(default=0)
    answered_ques_count: Mapped[int] = mapped_column(default=0)
    # store the number of questions the user selected (10, 15, or 20)
    num_questions_selected: Mapped[int] = mapped_column(default=10)
    user: Mapped["User"] = relationship("User", back_populates="results")
    # cascade="all, delete-orphan" ensures Questions are deleted when Results is deleted
    questions: Mapped[List["Questions"]] = relationship(
        "Questions", back_populates="results", cascade="all, delete-orphan"
    )

class Questions(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    result_id: Mapped[int] = mapped_column(ForeignKey("results.id"), nullable=False)
    question: Mapped[str] = mapped_column()
    correct_ans: Mapped[str] = mapped_column()
    user_selected_ans: Mapped[str] = mapped_column()
    is_correct: Mapped[bool] = mapped_column()
    results: Mapped["Results"] = relationship("Results", back_populates="questions")
