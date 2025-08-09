from django.db import models


class PaymentToken(models.Model):
    organization = models.OneToOneField(
        'Organization',
        on_delete=models.CASCADE,
        related_name="payment_token",
        verbose_name="Организация",
    )
    token = models.CharField(max_length=512, verbose_name="Токен провайдера")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Платёжный токен организации"
        verbose_name_plural = "Платёжные токены организаций"

    def __str__(self) -> str:
        return f"{self.organization} — токен"
