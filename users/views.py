from django.shortcuts import redirect, render
from .models import Profile
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid(): # is_valid() -> in-built function
            print("hey")
            form.save() # save() is defined in forms.py
            return redirect('/myapp/products')

    form = NewUserForm()
    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def create_profile(request):
    if request.method == 'POST':
        user = request.user #logged in user
        contact = request.POST.get('contact')
        try:
            dp = request.FILES['upload']
            profile = Profile(user=user, dp=dp, contact=contact)
        except Exception as e:
            print(e)
            profile = Profile(user=user, contact=contact)

        profile.save()
        return redirect('users/profile.html')

    return render(request, 'users/createprofile.html')

def seller_profile(request, id):
    seller = User.objects.get(id=id)
    context = {
        'seller': seller
    }
    return render(request, 'users/sellerprofile.html', context)
