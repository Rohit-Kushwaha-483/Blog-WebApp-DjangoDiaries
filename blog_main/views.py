from django.shortcuts import render,redirect
from blogs.models import Category,Blogs,ContactMessage
from .forms import RegistrationForm,ContactForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

# Showing Home Page
def home(request):
    categories = Category.objects.all()
    featured_post = Blogs.objects.filter(is_featured=True, status='published')
    posts = Blogs.objects.filter(is_featured=False, status='published')
    recent_posts = Blogs.objects.filter(is_featured=False, status='published').order_by('-created_at')

    context = {
        'categories':categories,
        'featured_post':featured_post,
        'posts':posts,
        'recent_posts':recent_posts,
        }

    return render(request, 'home.html', context)

# Showing About Us Page
def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the contact message to the database
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Redirect to success page (optional)
            return redirect('contact_success')  # Redirect to a success page you create
    else:
        form = ContactForm()
    return render(request, 'about.html')

# Showing privacy_policy Page
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

# Showing contact Us Page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the contact message to the database
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Redirect to success page (optional)
            return redirect('contact_success')  # Redirect to a success page you create
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact/contact_success.html')


# Handling the Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')
    else:
        form=RegistrationForm()

    context = {
    'form':form,
    }
    
    return render(request, 'register.html',context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print("--------------- > ",username,password)

             # Authenticate the user with the provided username and password
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard') # redirect to dashboard after user succesfully logged-in
    else:
        form = AuthenticationForm()

    context = {
    'form':form,
    }

    return render(request, 'login.html',context)



def logout(request):
    # Log the user out
    auth.logout(request)
    
    # Redirect to the home page or login page after logout
    return redirect('home')

