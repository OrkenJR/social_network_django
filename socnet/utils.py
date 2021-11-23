from django.contrib.auth.models import User

class DataMixin:
    def get_context_data(self, **kwargs):
        context = kwargs
