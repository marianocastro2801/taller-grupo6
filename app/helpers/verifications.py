def user_has_rols(session, rols=set()):
    return rols.issubset(session.get("user")["information"]["rols"])


def user_has_permissions(session, permissions=set()):
    return permissions.issubset(session.get("user")["permissions"])


def user_has_permission(session, permission=""):
    return permission in (session.get("user")["permissions"])
