def is_user_active_superuser(user):
    if user.is_authenticated:
        return user.is_active and user.is_superuser

    return False


def is_user_active_staff(user):
    if user.is_authenticated:
        return user.is_active and user.is_staff

    return False
