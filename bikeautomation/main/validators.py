from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def email_validator(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def name_validator(full_name):
    if re.search("\d",full_name) is None:
        return True
    return False

def nic_validator(nic):
    if re.match("\d\d\d\d\d-\d\d\d\d\d\d\d-\d",nic) is None:
        return False
    return True
def phone_validator(contact):
    if len(contact) !=11:
        return False
    return True    