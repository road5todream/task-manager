from enum import Enum
from django.utils.translation import gettext as _


class VerboseName(Enum):
    NAME = _('Name')
    STATUS = _('Status')
    EXECUTOR = _('Executor')
    LABEL = _('Label')
    LABELS = _('Labels')
    DESCRIPTION = _('Description')


class FlashMessages(Enum):
    REGISTER_SUCCESS = _('User is successfully registered')
    LOGIN_SUCCESS = _('You are logged in')
    LOGOUT_SUCCESS = _('You are logged out')
    NO_PERMIT_TO_CHANGE_USER = _('You have no rights to change another user')
    USER_SUCCESSFULLY_CHANGED = _('User successfully changed')
    USER_SUCCESSFULLY_DELETE = _('User successfully delete')
    NO_AUTHENTICATION = _('You are not logged in! Please log in.')
    USER_IS_USING = _('Unable to delete a user because he is being used')
    STATUS_CREATED = _('Status successfully created')
    STATUS_SUCCESSFULLY_CHANGED = _('Status successfully changed')
    STATUS_IS_USING = _('It is impossible to delete a '
                        'status because it is in use')
    STATUS_SUCCESSFULLY_DELETE = _('Status successfully deleted')
    LABEL_CREATED = _('Label successfully created')
    LABEL_SUCCESSFULLY_CHANGED = _('Label successfully changed')
    LABEL_SUCCESSFULLY_DELETE = _('Label successfully deleted')
    LABEL_IS_USING = _('It is impossible to delete a '
                       'label because it is in use')
    TASK_CREATED = _('Task successfully created')
    TASK_SUCCESSFULLY_CHANGED = _('Task successfully changed')
    TASK_SUCCESSFULLY_DELETE = _('Task successfully deleted')
    NO_PERMIT_TO_DELETE_TASK = _('The task can be deleted only by its author')
