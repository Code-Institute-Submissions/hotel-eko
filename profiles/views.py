from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages

from .models import UserProfile
from owner_blog.models import OwnerBlog
from owner_blog.forms import BlogForm
from .forms import UserProfileForm
from checkout.models import Order

from django.contrib.auth.decorators import login_required

import datetime


@login_required
def profile(request):
    """
    Displays the user's profile on their 'my account' page
    as well as the owner's blog posts
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    blog_posts = OwnerBlog.objects.all()
    blog_form = BlogForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile. \
                                        Please try again.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        'profile': profile,
        'blog_posts': blog_posts,
        'blog_form': blog_form,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def new_blog(request):
    """ Allows the owner of the hotel to add new blog posts
    to the profile page, checking that the post content is not empty """

    user_profile = UserProfile.objects.get(user=request.user)

    if request.user.is_authenticated and request.user.is_superuser:

        if request.method == 'POST':
            blog_form = BlogForm(request.POST)

            if blog_form.is_valid():
                if len(request.POST["thought_content"]) <= 0:
                    messages.error(
                        request, "You have not added any content to your post. \
                                            Please add content and try again.")
                    return redirect(reverse("profile"))
                new_post = blog_form.save(commit=False)
                new_post.user_profile = user_profile
                date_added = datetime.datetime.now()
                blog_form.save()
                messages.success(request, 'Success! Your new post has \
                                            been added')
                return redirect(reverse("profile"))
            else:
                messages.error(request, 'Your post could not be added. \
                                            Please check your post is valid.')
        else:
            blog_form = BlogForm()

    template = 'profiles/profile.html'
    context = {
        'blog_form': blog_form,
    }

    return render(request, template, context)


@login_required
def delete_blog(request, blog_post_id):
    """ Removes a blog post from the profiles template if the
    same hotel owner is in session """

    post = get_object_or_404(OwnerBlog, id=blog_post_id)

    if request.user.is_superuser:
        post.delete()
        messages.success(request, 'Success! Your post has \
                                    been deleted')
        return redirect(reverse("profile"))
    else:
        messages.error(request, 'Only the hotel owner can delete posts.')
        return redirect(reverse("profile"))

    template = 'profiles/profile.html'
    context = {
        'post': post,
    }

    return render(request, template, context)


@login_required
def edit_blog(request, blog_post_id):
    """ Allows the superuser to edit the blog post that they've written """

    user_profile = get_object_or_404(UserProfile, user=request.user)
    blog = get_object_or_404(OwnerBlog, id=blog_post_id)
    blog_form = BlogForm()

    if request.user.is_superuser:
        if request.method == 'POST':
            blog_form = BlogForm(request.POST, instance=blog)
            if blog_form.is_valid():
                if len(request.POST["title" or "thought_content"]) <= 0:
                    messages.error(
                        request, "You have not completed the post form. \
                                            Please add content and try again.")
                    return redirect(reverse("profile"))
                else:
                    blog = blog_form.save(commit=False)
                    user_profile = user_profile
                    blog_form.save()
                    messages.success(request, 'Success! Your post has \
                                                    been updated.')
                    return redirect(reverse("profile"))
        else:
            blog_form = BlogForm(instance=blog)

    template = 'profile/profile.html'
    context = {
        'blog_form': blog_form,
        'user_profile': user_profile,
        'blog': blog,
    }

    return render(request, template, context)
