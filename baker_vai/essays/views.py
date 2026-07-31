from django.shortcuts import render, get_object_or_404
from .models import Essay, Category


def home(request):
    essays = Essay.objects.filter(status=Essay.Status.PUBLISHED).select_related('category')
    categories = Category.objects.filter(is_active=True)

    current_category = request.GET.get('category')
    if current_category:
        essays = essays.filter(category__slug=current_category)

    context = {
        'essays': essays,
        'categories': categories,
        'total': essays.count(),
        'current_category': current_category,
    }
    return render(request, 'essays/home.html', context)


def essay_detail(request, pk):
    essay = get_object_or_404(
        Essay.objects.select_related('category', 'created_by').prefetch_related('quotes'),
        pk=pk,
        status=Essay.Status.PUBLISHED,
    )

    related = Essay.objects.filter(
        status=Essay.Status.PUBLISHED, category=essay.category
    ).exclude(pk=essay.pk).select_related('category')[:3]

    return render(request, 'essays/detail.html', {'essay': essay, 'related': related})
