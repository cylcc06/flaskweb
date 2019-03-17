from flask import Blueprint
main = Blueprint('main', __name__)


from . import views,errors
from ..models import Permission


#{% if current_user.can(Permission.WRITE) %}
#'Permission' is undefined
#如果没有，报上面错误
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)