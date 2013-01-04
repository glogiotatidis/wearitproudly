from forms import ShirtForm, ShotForm
from models import Shirt


def shirt_form(request):
    """
    A context processor that adds a BrowserID form to the request
    """
    shirt_form = ShirtForm(initial={'created_by':'', 'introduced':''})
    shot_form = ShotForm()

    return {'shirt_form_new': shirt_form, 'shot_form_new': shot_form}


def current_page(request):
    return {'PATH': request.path}
