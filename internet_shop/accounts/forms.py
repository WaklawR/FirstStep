from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        group = Group.objects.get(name="internet_shop_users")
        user.groups.add(group)
        user.save()
        return user
