from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female')
)



class CSRFExemptMixin(object):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


class BaseView(object):
    
    action = None


    def get(self, request, *args, **kwargs):
        
        if self.action is not None:
            func = getattr(self, self.action, None)
            if func is not None:
                return func(request, *args, **kwargs)
        raise Http404("Method Not Allowed")


    def post(self, request, *args, **kwargs):
        
        if self.action is not None:
            func = getattr(self, self.action, None)
            if func is not None:
                return func(request, *args, **kwargs)

        raise Http404("Method Not Allowed")


class CustomForm(object):
    
    def error_to_json(self, form):
        return dict([(k, v[0]) for k, v in form.errors.items()])

