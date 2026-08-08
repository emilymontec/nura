"""
Límites de uso por plan para el Módulo 1 (Cuentas y Workspace).

Antes de este cambio, UserProfile.plan / daily_messages / last_message_date
existían en el modelo pero ninguna vista los usaba: cualquier usuario podía
enviar mensajes o subir archivos sin límite, sin importar su plan.
"""
from datetime import date
from django.db.models import Sum

PLAN_LIMITS = {
    "free": {
        "daily_messages": 30,
        "max_storage_mb": 100,
        "max_datasets": 10,
        "max_file_size_mb": 20,
    },
    "pro": {
        "daily_messages": 500,
        "max_storage_mb": 2048,
        "max_datasets": 200,
        "max_file_size_mb": 50,
    },
    "enterprise": {
        "daily_messages": None,   # None = sin límite
        "max_storage_mb": None,
        "max_datasets": None,
        "max_file_size_mb": 200,
    },
}

DEFAULT_PLAN = "free"


class QuotaExceeded(Exception):
    """Se lanza cuando una acción supera el límite del plan del usuario."""
    def __init__(self, message, code="quota_exceeded"):
        self.message = message
        self.code = code
        super().__init__(message)


def get_plan_limits(plan: str) -> dict:
    return PLAN_LIMITS.get(plan, PLAN_LIMITS[DEFAULT_PLAN])


def _reset_daily_counter_if_needed(profile) -> None:
    today = date.today()
    if profile.last_message_date != today:
        profile.daily_messages = 0
        profile.last_message_date = today
        profile.save(update_fields=["daily_messages", "last_message_date"])


def check_message_quota(user) -> None:
    """
    Lanza QuotaExceeded si el usuario ya alcanzó su límite diario de
    mensajes de chat. No incrementa el contador (eso lo hace
    increment_message_usage tras una respuesta exitosa).
    """
    profile = user.profile
    _reset_daily_counter_if_needed(profile)
    limit = get_plan_limits(profile.plan)["daily_messages"]
    if limit is not None and profile.daily_messages >= limit:
        raise QuotaExceeded(
            f"Alcanzaste el límite de {limit} mensajes diarios de tu plan "
            f"'{profile.plan}'. Actualiza tu plan o vuelve mañana.",
            code="daily_message_limit",
        )


def increment_message_usage(user) -> None:
    profile = user.profile
    _reset_daily_counter_if_needed(profile)
    profile.daily_messages += 1
    profile.save(update_fields=["daily_messages"])


def get_storage_usage_bytes(workspace) -> int:
    total = workspace.datasets.filter(archived=False).aggregate(total=Sum("file_size"))["total"]
    return total or 0


def check_storage_quota(workspace, incoming_file_size: int) -> None:
    profile = workspace.owner.profile
    limits = get_plan_limits(profile.plan)

    max_file_mb = limits["max_file_size_mb"]
    if max_file_mb is not None and incoming_file_size > max_file_mb * 1024 * 1024:
        raise QuotaExceeded(
            f"El archivo supera el tamaño máximo de {max_file_mb} MB permitido en tu plan '{profile.plan}'.",
            code="file_too_large",
        )

    max_storage_mb = limits["max_storage_mb"]
    if max_storage_mb is not None:
        used = get_storage_usage_bytes(workspace)
        limit_bytes = max_storage_mb * 1024 * 1024
        if used + incoming_file_size > limit_bytes:
            raise QuotaExceeded(
                f"Este archivo excede tu cuota de almacenamiento ({max_storage_mb} MB) "
                f"del plan '{profile.plan}'. Elimina o archiva datasets para liberar espacio.",
                code="storage_limit",
            )


def check_dataset_count_quota(workspace) -> None:
    profile = workspace.owner.profile
    limit = get_plan_limits(profile.plan)["max_datasets"]
    if limit is not None:
        current = workspace.datasets.filter(archived=False).count()
        if current >= limit:
            raise QuotaExceeded(
                f"Alcanzaste el máximo de {limit} datasets activos de tu plan '{profile.plan}'. "
                "Archiva o elimina alguno para subir uno nuevo.",
                code="dataset_count_limit",
            )


def workspace_usage_summary(workspace) -> dict:
    profile = workspace.owner.profile
    limits = get_plan_limits(profile.plan)
    _reset_daily_counter_if_needed(profile)
    used_bytes = get_storage_usage_bytes(workspace)
    return {
        "plan": profile.plan,
        "storage_used_mb": round(used_bytes / (1024 * 1024), 2),
        "storage_limit_mb": limits["max_storage_mb"],
        "dataset_count": workspace.datasets.filter(archived=False).count(),
        "dataset_limit": limits["max_datasets"],
        "messages_used_today": profile.daily_messages,
        "daily_message_limit": limits["daily_messages"],
        "max_file_size_mb": limits["max_file_size_mb"],
    }
