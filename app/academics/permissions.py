from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMentorOrReadOnly(BasePermission):
    """
    Менторы могут выполнять любые действия (create, update, delete),
    студенты — только читать данные.
    """

    def has_permission(self, request, view):
        # Проверяем, если запрос на чтение (GET, HEAD, OPTIONS) — разрешаем всем
        if request.method in SAFE_METHODS:
            return True

        # Только аутентифицированные менторы могут изменять данные
        return request.user and request.user.is_authenticated and request.user.role == 'mentor'
