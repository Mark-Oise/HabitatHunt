from django.core.exceptions import ValidationError
import re


class CustomPasswordValidator:
    def __init__(self):
        self.min_length = 10
        self.max_length = 100

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long."
            )
        if len(password) > self.max_length:
            raise ValidationError(
                f"Password must be at most {self.max_length} characters long."
            )
        if not any(char.islower() for char in password):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "Password must contain at least one special character: !@#$%^&*(),.?\":{}|<>"
            )

    def get_help_text(self):
        return f"""
        Your password must:
        • Be at least {self.min_length} characters long
        • Contain at least one lowercase letter
        • Contain at least one special character
        """