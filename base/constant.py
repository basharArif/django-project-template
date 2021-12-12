from django.utils.translation import gettext_lazy as _

ACCOUNTANT = 0
OPERATOR = 1
USER_TYPE = {
    (ACCOUNTANT, _('Accountant')),
    (OPERATOR, _('Operator'))
}
