import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

PAYMENT_API_URL = getattr(
    settings,
    "PAY_OPERATOR_API_URL",
    "https://pay.operator.kg/api/v1/payments/make-payment-link/",
)
PAY_OPERATOR_TOKEN = getattr(settings, "PAY_OPERATOR_TOKEN", None)


def generate_payment_link(payment, redirect_url: str) -> str | None:
    """
    Создает платёжную ссылку через pay.operator.kg и записывает ее в payment.payment_link.
    Возвращает URL или None при ошибке.
    """
    if not PAY_OPERATOR_TOKEN:
        logger.error("PAY_OPERATOR_TOKEN is not configured in settings/environment.")
        return None

    payload = {
        "amount": str(payment.amount),
        "transaction_id": str(payment.id),
        "comment": f"Оплата отсутствия за занятие #{payment.grade.session_id}",
        "redirect_url": redirect_url,
        "token": PAY_OPERATOR_TOKEN,
    }

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(PAYMENT_API_URL, json=payload, headers=headers, timeout=30)
    except Exception as e:
        logger.error(f"Ошибка при запросе к платежному сервису: {str(e)}", exc_info=True)
        return None

    if response.status_code == 200:
        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Не удалось распарсить JSON ответа платежного сервиса: {e}")
            return None

        payment_url = data.get("pay_url")
        if payment_url:
            payment.payment_link = payment_url
            # сохраним для дебага полезную нагрузку
            try:
                payment.provider_payload = data
            except Exception:
                pass
            payment.save(update_fields=["payment_link", "provider_payload", "updated_at"])
            return payment_url

        logger.error(f"В ответе платежного сервиса отсутствует pay_url. Ответ: {data}")
        return None

    logger.error(f"Ошибка создания платёжной ссылки. Код: {response.status_code}, Ответ: {response.content}")
    return None
