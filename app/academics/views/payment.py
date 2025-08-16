from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Session, Grade, Payment
from ..serializers.payment import AbsencePaymentCreateRequestSerializer, PaymentSerializer
from ..serializers.grade import MakeUpSubmissionRequestSerializer
from ..services.pay_operator import generate_payment_link
import logging

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Payments"],
    request=AbsencePaymentCreateRequestSerializer,
    responses={
        200: PaymentSerializer,
        201: PaymentSerializer,
        400: OpenApiResponse(description="Некорректные данные"),
        403: OpenApiResponse(description="Оплата не требуется (не отсутствие)"),
    },
    summary="Создать/получить ссылку на оплату за отсутствие на занятии",
    description="Создает платёж за отсутствие (grade=0) и возвращает ссылку на оплату. Если платёж уже создан и не оплачен — вернёт существующий.",
)
class AbsencePaymentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AbsencePaymentCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = serializer.validated_data["session_id"]
        session = get_object_or_404(Session, id=session_id)
        user = request.user

        grade, _ = Grade.objects.get_or_create(
            user=user,
            session=session,
            defaults={"grade": 0},
        )

        # Оплата требуется только если это отсутствие
        if grade.grade != 0:
            return Response(
                {"detail": "Оплата не требуется: студент не отсутствовал на занятии."},
                status=status.HTTP_403_FORBIDDEN,
            )

        payment = (
            Payment.objects
            .filter(user=user, grade=grade, status__in=[Payment.Status.PENDING, Payment.Status.FAILED])
            .order_by("-created_at")
            .first()
        )
        if payment is None:
            payment = Payment.objects.create(
                user=user,
                grade=grade,
                amount=getattr(settings, "ABSENCE_PAYMENT_AMOUNT", 500),
                status=Payment.Status.PENDING,
                organization=user.organization,
            )

        redirect_url = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/payments/{payment.id}/success"
        # pay_url = generate_payment_link(payment, redirect_url=redirect_url)
        pay_url = 'https://paylink.bakai.kg/25dc79fe-eca4-4e50-a02a-bbf91e332828'

        data = PaymentSerializer(payment).data
        if pay_url:
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Не удалось сформировать ссылку на оплату", "payment": data},
            status=status.HTTP_502_BAD_GATEWAY,
        )


@extend_schema(
    tags=["Payments"],
    request=MakeUpSubmissionRequestSerializer,
    responses={200: OpenApiResponse(description="Ссылка/файл отработки сохранены"), 400: OpenApiResponse(description="Некорректные данные"), 402: OpenApiResponse(description="Оплата требуется")},
    summary="Отправить ссылку или файл для отработки после оплаты",
    description="Доступно только студенту с оплаченной отсутствием (наличие Payment=paid по данному занятию). Принимает либо make_up_link, либо make_up_file.",
)
class MakeUpSubmissionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MakeUpSubmissionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = serializer.validated_data["session_id"]
        make_up_link = serializer.validated_data.get("make_up_link")
        make_up_file = request.FILES.get("make_up_file") or serializer.validated_data.get("make_up_file")

        session = get_object_or_404(Session, id=session_id)
        grade = get_object_or_404(Grade, user=request.user, session=session)

        # Проверка наличия оплаченного платежа
        has_paid = Payment.objects.filter(user=request.user, grade=grade, status=Payment.Status.PAID).exists()
        if not has_paid:
            return Response({"detail": "Требуется оплата за отсутствие."}, status=status.HTTP_402_PAYMENT_REQUIRED)

        updated_fields = []
        if make_up_link:
            grade.make_up_link = make_up_link
            updated_fields.append("make_up_link")
        if make_up_file:
            grade.make_up_file = make_up_file
            updated_fields.append("make_up_file")

        if not updated_fields:
            return Response({"detail": "Нужно указать make_up_link или приложить make_up_file."}, status=status.HTTP_400_BAD_REQUEST)

        grade.save(update_fields=updated_fields + ["updated_at"])
        return Response({"ok": True}, status=status.HTTP_200_OK)


@extend_schema(tags=["Payments"],)
class PaymentWebhookViewSet(viewsets.ViewSet):
    """
    Webhook в формате, похожем на предоставленный пример:
    POST body: {"operation_id": "<uuid>", "operation_state": "<status>"}
    Также поддерживает альтернативные ключи: transaction_id / status.
    """
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            transaction_id = data.get('operation_id') or data.get('transaction_id')
            payment_status = data.get('operation_state') or data.get('status')

            if not transaction_id or not payment_status:
                logger.warning("Недостаточно данных в webhook: %s", data)
                return Response({'error': 'Недостаточно данных'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                payment = Payment.objects.get(id=transaction_id)
            except Payment.DoesNotExist:
                logger.error(f"Платёж не найден: ID {transaction_id}")
                return Response({'error': 'Платёж не найден'}, status=status.HTTP_404_NOT_FOUND)

            normalized = str(payment_status).lower()
            if normalized == "paid":
                payment.status = Payment.Status.PAID
                payment.paid_at = timezone.now()
            elif normalized in ("canceled", "cancelled"):
                payment.status = Payment.Status.CANCELED
            elif normalized in ("failed", "error"):
                payment.status = Payment.Status.FAILED
            else:
                payment.status = Payment.Status.PENDING

            payment.save(update_fields=["status", "paid_at", "updated_at"])
            return Response({'success': True}, status=status.HTTP_200_OK)

        except Exception:
            logger.exception("Ошибка при обработке webhook")
            return Response({'error': 'Внутренняя ошибка'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
