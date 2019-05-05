from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import redirect, render

from main.forms.form import LoginForm
from main.models import USession
from django.contrib.auth import authenticate, login as sys_login, logout as sys_logout, user_login_failed


@login_required
def dashboard(request):
    try:
        return render(request, 'pages/dashboard.html', {})
    except Exception as ex:
        print(ex)


def login(request):
    form = LoginForm(request.POST or None)
    messages = None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            if not request.POST.get('remember', None):
                request.session.set_expiry(0)

            sys_login(request, user)
            user_session = USession()
            user_session.id = user.id
            user_session.user_id = user.id
            user_session.email = user.email
            user_session.first_name = user.first_name
            user_session.last_name = user.last_name
            user_session.full_name = user.get_full_name()
            request.session['my'] = model_to_dict(user_session)
            return redirect('dashboard')
        else:
            messages = ['Kullanıcı adı veya parola hatalı']

    return render(request, "pages/login.html", {"form": form, 'messages': messages})


@login_required
def logout(request):
    try:
        sys_logout(request)
        request.session.flush()
        return redirect('/')
    except Exception as ex:
        print(ex)
