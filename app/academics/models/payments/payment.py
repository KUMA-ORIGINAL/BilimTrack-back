import uuid
from django.db import models
from django.conf import settings


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает оплаты"
        PAID = "success", "Оплачено"
        CANCELED = "canceled", "Отменено"
        FAILED = "failed", "Ошибка"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь")
    grade = models.ForeignKey("Grade", on_delete=models.CASCADE, related_name="payments", verbose_name="Оценка/занятие")
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Организация",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, verbose_name="Статус")
    payment_link = models.URLField(blank=True, null=True, verbose_name="Ссылка на оплату")
    provider_payload = models.JSONField(blank=True, null=True, verbose_name="Ответ провайдера")
    paid_at = models.DateTimeField(blank=True, null=True, verbose_name="Время оплаты")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self) -> str:
        return f"{self.id} | {self.user} | {self.amount} | {self.status}"
