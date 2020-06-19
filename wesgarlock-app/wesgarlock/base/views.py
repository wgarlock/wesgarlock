# Create your views here.
from django.shortcuts import redirect
from wagtail.admin import messages
from wagtail.contrib.modeladmin.views import EditView
from wagtail.core.models import Site


class BaseAppEditView(EditView):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super(BaseAppEditView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        site = Site.find_for_request(self.request)
        instance.site = site
        instance.save()
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())
