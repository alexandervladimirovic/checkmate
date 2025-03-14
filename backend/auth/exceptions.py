class PasswordHashingException(Exception):
    """
    Raise if hashing password failed.
    """

class ValidatePasswordException(Exception):
    """
    Raise if the password does not pass verification.
    """


class CreateJWTException(Exception):
    """
    Raise if an error occurred when creating access token.
    """


class CreateRefreshTokenException(Exception):
    """
    Raise if an error occurred when creating refresh token.
    """
    