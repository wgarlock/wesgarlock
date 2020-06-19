from django.contrib.auth import get_user_model, views
from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wesgarlock.base.models import BaseMixin, MessageThread
from wesgarlock.base.serializers import Message, MessageSerializer
from rest_auth.views import PasswordResetConfirmView

class LoginView(views.LoginView):
    def get_success_url(self):
        return '/'


class LogoutView(views.LogoutView):
    next_page = '/'


class PasswordResetView(views.PasswordResetView):
    success_url = reverse_lazy('front_password_reset_done')
    results = {"result": None}

    def response(self):
        return JsonResponse(self.results)

    def form_invalid(self, form):
        self.results["result"] = "errors"
        return self.response()

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = get_user_model().objects.filter(email=email)
        if user:
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            self.results["result"] = "email sent! check your inbox"
        else:
            self.results["result"] = "email does not exist in our system"
        return self.response()


class PasswordResetDoneView(views.PasswordResetDoneView):
    pass


class PasswordResetConfirmView(BaseMixin, views.PasswordResetConfirmView):
    success_url = '/'
    template_name = 'registration/password_reset_confirm.jinja'

    results = {"result": None}

    def response(self):
        return JsonResponse(self.results)


    def get_context_data(self, **kwargs):
        self.form = kwargs.pop("form", None)
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.results["result"] = form.errors
        return self.response()


class PasswordResetConfirmViewAPI(PasswordResetConfirmView):
    pass


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    pass


class PasswordChangeView(views.PasswordChangeView):
    pass


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    pass


class MessagePostView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            instance = Message(**serializer.validated_data)
            thread, created = MessageThread.objects.get_or_create(email=instance.email)
            if created and request.user.is_authenticated:
                thread.owner = request.user
                thread.save()
                instance.author = request.user

            instance.thread = thread
            instance.save()
            return Response("Message was sent!", status=status.HTTP_201_CREATED)
        else:
            return Response("There was an error in your message", status=status.HTTP_400_BAD_REQUEST)
