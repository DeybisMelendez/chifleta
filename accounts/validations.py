from django.contrib import messages
from django.contrib.auth import get_user_model


class ErrorCode():
    INVALID_USERNAME = "El nombre de usuario debe tener entre 3 y 50 caracteres alfanuméricos."
    INVALID_FIRSTNAME = "El nombre deben tener entre 3 y 50 caracteres."
    INVALID_LASTNAME = "El apellido deben tener entre 3 y 50 caracteres."
    USERNAME_EXISTS = "El nombre de usuario ya existe, elija otro."
    DIFFERENT_PASSWORD = "Las contraseñas no coinciden, inténtelo de nuevo."
    INVALID_PASSWORD = "La contraseña debe tener al menos 8 caracteres."
    WRONG_USER = "Usuario o contraseña incorrectos."
    INVALID_BIO = "La biografía debe ser menor a 160 caracteres."

def is_valid_name(name):
    return 3 <= len(name) <= 50

def is_valid_register_form(request, username, first_name, last_name, password, confirm_password):
    User = get_user_model()

    if not (is_valid_name(username) and username.isalnum()):
        messages.add_message(request, messages.ERROR,
                            ErrorCode.INVALID_FIRSTNAME)
        return False

    if not is_valid_name(first_name):
        messages.add_message(request, messages.ERROR,
                            ErrorCode.INVALID_FIRSTNAME)
        return False
    if not is_valid_name(last_name):
        messages.add_message(request, messages.ERROR,
                            ErrorCode.INVALID_LASTNAME)
        return False

    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR,
                            ErrorCode.USERNAME_EXISTS)
        return False

    if password != confirm_password:
        messages.add_message(request, messages.ERROR,
                            ErrorCode.DIFFERENT_PASSWORD)
        return False

    if len(password) < 8:
        messages.add_message(request, messages.ERROR,
                            ErrorCode.INVALID_PASSWORD)
        return False
    return True


def is_valid_update_form(request, first_name, last_name, bio):
    if not is_valid_name(first_name):
        messages.add_message(request, messages.ERROR,
                            ErrorCode.INVALID_FIRSTNAME)
        return False
    if not is_valid_name(last_name):
        messages.add_message(request, messages.ERROR,
                            ErrorCode.INVALID_LASTNAME)
        return False
    return True

def is_valid_login_form(request,user):
    if not user:
        messages.add_message(request, messages.ERROR,
                            ErrorCode.WRONG_USER)
        return False
    return True