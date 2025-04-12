from django.shortcuts import render, redirect,HttpResponse
from .models import Blogs, Category, Comment, Like
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from dashboard.models import UserProfile
from django.contrib.auth.models import User


# This view will display posts that belong to a specific category.

def posts_by_category(request, category_id):
    # Fetch all the blog posts that are 'published' and belong to the category with the given ID ('category_id')
    posts = Blogs.objects.filter(status='published', category=category_id)

    # The try/except block is used to handle the case when the category doesn't exist.
    # If the category with the given ID doesn't exist, it will redirect to the homepage.

    try:
        # Try to get the category from the database using the provided 'category_id'
        category = Category.objects.get(pk=category_id)
    except:
        # If the category doesn't exist, redirect the user to the homepage
        return redirect('home')

    # The 'get_object_or_404' line below does the same thing as the try/except block above.
    # It tries to get the category with the given 'category_id', but if it doesn't exist, 
    # it automatically shows a 404 error page.

    # category = get_object_or_404(Category, pk=category_id)

    # Preparing the context that will be passed to the template.
    context = {
        'posts': posts,
        'category': category,
    }

    # Rendering the 'posts_by_category.html' template with the context data
    return render(request, 'posts_by_category.html', context)

# Blogs | Single Blog page Setup 
def blogs(request, slug):
    # Step 1: Get the blog post using the 'slug' passed in the URL
    single_post = get_object_or_404(Blogs, slug=slug, status='published')

    # Step 2: Handle a comment or reply submission (POST request)
    if request.method == 'POST':
        # Check if the user is logged in (authenticated)
        if request.user.is_authenticated:
            # Check if the action is a comment submission
            if 'comment' in request.POST:
                # Create a new Comment object and save it
                comment = Comment()
                comment.user = request.user  # The current user
                comment.blog = single_post  # The blog post the comment belongs to
                comment.comment = request.POST['comment']  # Get the comment content from the form

                # Check if this is a reply to an existing comment
                parent_comment_id = request.POST.get('parent_comment_id')  # This will be None for top-level comments
                if parent_comment_id:
                    parent_comment = get_object_or_404(Comment, id=parent_comment_id)
                    comment.parent_comment = parent_comment  # Set the parent comment to create a reply

                comment.save()  # Save the comment (or reply) to the database
                return redirect('blogs', slug=slug)  # Redirect to the same blog page

            # Handle like/unlike functionality
            elif 'like' in request.POST:
                # Check if the user has already liked this post
                user_liked = Like.objects.filter(blog=single_post, user=request.user).exists()

                if user_liked:
                    # If the user has already liked the post, remove the like
                    Like.objects.filter(blog=single_post, user=request.user).delete()
                else:
                    # If the user has not liked the post, add the like
                    Like.objects.create(blog=single_post, user=request.user)

                return redirect('blogs', slug=slug)  # Redirect to the same blog page

        else:
            # If the user is not logged in, redirect to the login page
            return redirect('login')

    # Step 3: Fetch all the comments (top-level and replies) for the blog
    comments = Comment.objects.filter(blog=single_post, parent_comment__isnull=True).order_by('created_at')
    
    # Step 4: Count the total comments for display
    comment_counts = comments.count()

    # Fetch the total number of likes for the post
    like_count = Like.objects.filter(blog=single_post).count()

    # Step 5: Check if the logged-in user has already liked this post (only if the user is authenticated)
    user_liked = Like.objects.filter(blog=single_post, user=request.user).exists() if request.user.is_authenticated else False

    # Retrieve the user's profile
    author_profile = UserProfile.objects.filter(user=single_post.author).first()

    # Step 6: Prepare the context for the template (data to be passed to the HTML)
    context = {
        'single_post': single_post,
        'comments': comments,
        'comment_counts': comment_counts,
        'like_count': like_count,
        'user_liked': user_liked,
        'author_profile': author_profile,  # 👈 updated variable
    }

    # Step 7: Render the HTML page and pass the context data
    return render(request, 'blogs.html', context)

# Search Functionality for Blogs
def search(request):
    keyword = request.GET.get('keyword')
    
    # Query the Blogs model to find blogs that contain the keyword in the title, description, or body
    # It only returns blogs that have a 'published' status
    # The `|` operator is used to perform an OR search (matching any of the conditions),
    # and the `,` is used for an AND condition (all conditions must be true).
    blogs = Blogs.objects.filter(
        Q(title__icontains=keyword) |  # OR: keyword can be in the title
        Q(short_description__icontains=keyword) |  # OR: keyword can be in the short description
        Q(blog_body__icontains=keyword),  # OR: keyword can be in the blog body
        status='published'  # AND: the blog must have 'published' status
    )

    context = {
        'blogs': blogs,
        'keyword': keyword,
    }

    return render(request, 'search.html', context)

def posts_by_author(request, username):
    author = get_object_or_404(User, username=username)

    # Fetch posts associated with the author that are published, ordered by creation date (newest first)
    author_posts = Blogs.objects.filter(author=author, status='published').order_by('-created_at')

    context = {
        'author': author,
        'author_posts': author_posts,
    }

    return render(request, 'author_posts.html', context)

