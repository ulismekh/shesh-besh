from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Review
from .forms import ReviewForm


def home(request):
    categories = (
        Category.objects
        .filter(dishes__is_available=True)
        .distinct()
        .prefetch_related("dishes")
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