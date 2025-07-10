from __future__ import annotations
import logging
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet, Q
from django.db import connection

logger = logging.getLogger('models')


class Note(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    is_open = models.BooleanField(default=False)

    @staticmethod
    def get_all_notes_of_user(user: User) -> QuerySet[Note]:
        logger.debug(f'get all notes of {user}')
        return Note.objects.filter(author=user).all()

    @staticmethod
    def get_open_notes_of_user(user: User) -> QuerySet[Note]:
        logger.debug(f'get open notes of {user}')
        return Note.objects.filter(author=user, is_open=True).all()

    @staticmethod
    def get_open_notes() -> QuerySet[Note]:
        logger.debug('get open notes')
        return Note.objects.filter(is_open=True).all()

    @staticmethod
    def find_by_text(text: str) -> QuerySet[Note]:
        logger.debug(f'find notes by text: "{text}"')
        return Note.objects.filter(
            (Q(text__icontains=text) | Q(title__icontains=text)) & Q(is_open=True)
        ).all()

    @staticmethod
    def sql_find_by_text(text: str) -> list[Note]:
        logger.warning(f'use SQL query: "{text}"')
        cursor = connection.cursor()
        query = f"SELECT * FROM 'main_note' WHERE (title LIKE '%{text}%' OR text LIKE '%{text}%') AND is_open=1;"
        cursor.execute(query)
        result = [
            item[0] for item in cursor.fetchall()
        ]
        objects = []
        for id in result:
            objects.append(Note.objects.get(id=id))
        return objects
