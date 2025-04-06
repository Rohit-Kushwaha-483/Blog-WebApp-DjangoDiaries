from django.shortcuts import render,redirect
from blogs.models import Category,Blogs
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,BlogPostForm,AddUserForm,EditUserForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    category_counts = Category.objects.all().count()
    blogs_counts = Blogs.objects.all().count()

    context = {
        'category_counts':category_counts,
        'blogs_counts':blogs_counts,
    }

    return render(request, 'dashboard/dashboard.html',context)


def categories(request):
    context = {
    }

    return render(request, 'dashboard/categories.html',context)


def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('categories')  # Redirect to the categories page after form submission
    else:
        form = CategoryForm()  # Initialize the form when the request is GET
    
    context = {
        'form': form,
    }

    return render(request, 'dashboard/add_categories.html', context)


def edit_categories(request, pk):
    # Get the category object based on the primary key
    category = get_object_or_404(Category, pk=pk)
    
    # If the form is submitted via POST, process it
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        # Otherwise, create the form and pre-populate with the category data
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }

    return render(request, 'dashboard/edit_categories.html', context)


def delete_categories(request, pk):
    # Get the category object based on the primary key
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('categories')

    context = {
        'category': category
    }

    return render(request, 'dashboard/confirm_delete_category.html',context)


def posts(request):
    # To display only the posts created by the logged-in user, you'll need to Filter posts by the logged-in user
    user_posts = Blogs.objects.filter(author=request.user)

    context = {
        'posts': user_posts,
    }

    return render(request, 'dashboard/posts.html',context)


def add_posts(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to the database yet
            post.author = request.user       # Assign the logged-in user as the author

            # Auto-generate slug if not provided
            # Slug Auto-Generation: If slug is empty, it's generated from the title using slugify().
            if not post.slug:
                title = form.cleaned_data['title']
                post.slug = slugify(title)

                # Ensure the slug is unique
                # Uniqueness Check: If the slug already exists, it appends -1, -2, etc., to ensure uniqueness.
                count = 1
                original_slug = post.slug
                while Blogs.objects.filter(slug=post.slug).exists():
                    post.slug = f"{original_slug}-{count}"
                    count += 1

            post.save()                      # Now save to the database
            return redirect('posts')        # Redirect to the posts page after submission
            
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }

    return render(request, 'dashboard/add_posts.html', context)


def edit_posts(request, pk):
    post = get_object_or_404(Blogs, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title)
            post.save()
            return redirect('posts')
        
    form = BlogPostForm(instance=post)    # Populate form with the current post data

    context = {
        'form':form,
        'post':post,
    }

    return render(request, 'dashboard/edit_posts.html', context)


def delete_posts(request, pk):
    # Get the post object based on the primary key
    post = get_object_or_404(Blogs, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    
    context = {
        'post':post
    }

    return render(request, 'dashboard/confirm_delete_post.html', context)

def users(request):
    users = User.objects.all()
    
    context = {
        'users':users,
    }

    return render(request, 'dashboard/users.html', context)


def add_users(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')  # Redirect to a success page or user list page 
    else:
        form = AddUserForm()  # Create an empty form for GET request

    context = {
        'form': form,
    }

    return render(request, 'dashboard/add_users.html', context)


def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        
    # If the request method is GET (or form is not valid), show the form with the current user data
    else:
        form = EditUserForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'dashboard/edit_users.html', context)


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
            user.delete()
            return redirect('users')
    
    context = {
        'user': user
    }

    return render(request, 'dashboard/confirm_delete_users.html', context)
