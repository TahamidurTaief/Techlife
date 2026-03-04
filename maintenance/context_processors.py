from django.utils import timezone


def maintenance(request):
    section = getattr(request, "maintenance_section", None)
    config  = getattr(request, "maintenance_config",  None)

    if not section:
        return {"maintenance_active": False}

    until_ms = None
    if config and config.maintenance_until:
        # Always pass the timestamp — let JS decide if it's future or past
        until_ms = int(config.maintenance_until.timestamp() * 1000)

    return {
        "maintenance_active":   True,
        "maintenance_type":     section,
        "maintenance_until_ms": until_ms,
        # Debug: raw value so we can print it in template
        "maintenance_until_raw": str(config.maintenance_until) if config and config.maintenance_until else "",
        "server_now_ms": int(timezone.now().timestamp() * 1000),
    }