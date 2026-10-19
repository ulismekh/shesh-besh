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