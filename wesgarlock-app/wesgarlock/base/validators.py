from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def hex_validate(value):
    if value[0] != "#":
        raise ValidationError(
                _('%(value)s: hexidecimal colors start with #'),
                params={'value': value},
            )
