from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Draw(models.Model):
    number = models.PositiveIntegerField(unique=True)
    draw_date = models.DateField()
    status = models.CharField(max_length=12, default="SCHEDULED")  # SCHEDULED | DONE
    winning_numbers = models.JSONField(null=True, blank=True)      # ex) [1, 4, 9, 17, 31, 42]

    class Meta:
        ordering = ["-number"]

    def __str__(self):
        return f"{self.number}회"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    draw = models.ForeignKey(Draw, on_delete=models.PROTECT)  # 정산 보존용
    is_auto = models.BooleanField(default=True)
    picks = models.JSONField()             # ex) [3, 7, 11, 19, 28, 41]
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.draw.number}회"