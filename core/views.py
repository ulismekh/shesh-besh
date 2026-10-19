from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Review
from .forms import ReviewForm
from django.db import models


def home(request):
    categories = (
    Category.objects
        .filter(dishes__is_available=True)
        .distinct()
        .prefetch_related("dishes")
        .order_by(
            models.Case(
                models.When(name="Салаты", then=0),
                models.When(name="Первые блюда", then=1),
                models.When(name="Горячие блюда", then=2),
                default=3,
                output_field=models.IntegerField(),
            )
        )
    )

    reviews = Review.objects.filter(is_approved=True)[:10]

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Спасибо! Ваш отзыв отправлен на проверку."
            )
            return redirect("home")
    else:
        form = ReviewForm()

    context = {
        "categories": categories,
        "reviews": reviews,
        "form": form,
    }

    return render(request, "core/home.html", context)

import os
import secrets
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET


@require_GET
def create_admin_once(request):
    token = os.environ.get("CREATE_ADMIN_TOKEN", "")
    if not token or not secrets.compare_digest(
        request.GET.get("token", ""), token
    ):
        return HttpResponse("Forbidden", status=403)

    User = get_user_model()
    username = os.environ.get("ADMIN_USERNAME", "")
    password = os.environ.get("ADMIN_PASSWORD", "")

    if not username or not password:
        return HttpResponse("Missing credentials", status=500)

    if User.objects.filter(username=username).exists():
        return HttpResponse("Username already exists", status=409)

    User.objects.create_superuser(username=username, email="", password=password)
    return HttpResponse("Admin created. Remove this endpoint immediately.")