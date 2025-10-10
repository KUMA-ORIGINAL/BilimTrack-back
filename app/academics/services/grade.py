import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)


def send_grade_update(user, session, grade, created=False):
    """
    Отправляет в WebSocket сообщение о новой (или обновлённой) отметке
    студента на занятии.
    Рассылает сразу во все группы, привязанные к сессии.

    user     – экземпляр User
    session  – экземпляр Session
    grade    – экземпляр Grade
    created  – True, если отметка создана только что
    """
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.warning("Channel layer недоступен, уведомление не отправлено.")
        return

    try:
        group_ids = session.groups.values_list("id", flat=True)
        for gid in group_ids:
            room_group_name = f"grades_{gid}_{session.subject_id}"

            data = {
                "student_id": user.id,
                "student_name": f"{user.full_name}",
                "session_id": session.id,
                "attendance": grade.attendance,
                "created": created,
            }

            async_to_sync(channel_layer.group_send)(
                room_group_name,
                {"type": "grade_marked", "data": data},
            )
            logger.info(
                "WebSocket уведомление отправлено -> room=%s user_id=%s created=%s",
                room_group_name, user.id, created
            )

    except Exception as e:
        logger.exception("Ошибка при отправке WebSocket уведомления: %s", e)
