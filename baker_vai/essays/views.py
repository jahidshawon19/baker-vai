import json
import urllib.request
import urllib.parse

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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


def translate_page(request):
    return render(request, 'essays/translate.html')


@csrf_exempt
@require_POST
def translate_api(request):
    try:
        data   = json.loads(request.body)
        text   = data.get('text', '').strip()
        source = data.get('source', 'en')   # 'en' or 'bn'
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not text:
        return JsonResponse({'translation': ''})

    target = 'bn' if source == 'en' else 'en'
    langpair = f'{source}|{target}'

    try:
        url    = 'https://api.mymemory.translated.net/get?' + urllib.parse.urlencode({'q': text, 'langpair': langpair})
        req    = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
        translation = result['responseData']['translatedText']
        return JsonResponse({'translation': translation})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)
