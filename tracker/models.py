from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits', verbose_name='Пользователь')
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    pleasant_habit = models.BooleanField(default=False, verbose_name='Приятная привычка')
    linked_habit = models.OneToOneField(
        'self',
        on_delete=models.SET_NULL,
        related_name='linked_to',
        verbose_name='Связанная привычка',
        limit_choices_to={'pleasant_habit': True},
        **NULLABLE
    )
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', **NULLABLE)
    period = models.PositiveSmallIntegerField(default=1, verbose_name='Периодичность выполнения в днях')
    duration = models.PositiveIntegerField(verbose_name='Время выполнения в секундах')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]

    def __str__(self):
        return f"{self.action} - {self.user.username}"

    def clean(self):
        """
        Валидация модели Habit:
        - Нельзя одновременно указать связанную привычку и вознаграждение.
        - Приятная привычка не может иметь связанной привычки или вознаграждения.
        - Время выполнения не может превышать 120 секунд.
        - Период выполнения не может быть больше 7 дней.
        """

        if self.reward and self.linked_habit:
            raise ValidationError('Укажите либо вознаграждение, либо связанную привычку')
        if self.pleasant_habit and (self.reward or self.linked_habit):
            raise ValidationError('Приятная привычка не может иметь ни вознаграждения, ни связанной привычки')
        if self.duration > 120:
            raise ValidationError('Время выполнения не может быть больше 120 секунд')
        if self.period > 7:
            raise ValidationError("Период выполнения не может быть больше 7 дней")
