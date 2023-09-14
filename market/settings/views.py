from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect


def clear_all_cache_view(request):
    cache.clear()
    messages.success(request, 'Кэш очищен')
    return redirect(to="admin:index")