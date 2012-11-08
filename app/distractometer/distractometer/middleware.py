from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .forms import DistractionForm

class LoginFormMiddleware(object):
    def process_request(self, request):

        # if the top login form has been posted
        if request.method == 'POST':
            # validate the form
            login_form = AuthenticationForm(prefix='login', data=request.POST)
            if login_form.is_valid():
                # log the user in
                from django.contrib.auth import login
                login(request, login_form.get_user())


                return HttpResponseRedirect('/')





        else:
            login_form = AuthenticationForm(prefix='login',request=request)


        # attach the form to the request so it can be accessed within the templates
        request.login_form = login_form
