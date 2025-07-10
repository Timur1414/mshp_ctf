from __future__ import annotations
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Q


class Note(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    is_open = models.BooleanField(default=False)

    @staticmethod
    def get_all_notes_of_user(user: User) -> QuerySet[Note]:
        return Note.objects.filter(author=user).all()

    @staticmethod
    def get_open_notes_of_user(user: User) -> QuerySet[Note]:
        return Note.objects.filter(author=user, is_open=True).all()

    @staticmethod
    def get_open_notes() -> QuerySet[Note]:
        return Note.objects.filter(is_open=True).all()

    @staticmethod
    def find_by_text(text: str) -> QuerySet[Note]:
        return Note.objects.filter(
            (Q(text__icontains=text) | Q(title__icontains=text)) & Q(is_open=True)
        ).all()
