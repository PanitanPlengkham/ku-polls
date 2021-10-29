from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect

def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            # raw_passwd = form.cleaned_data.get('password')
            # user = authenticate(username=username,password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

