from .models import Listing


def watchlist_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Listing.objects.filter(watchers=request.user).count()
    return {'watchlist_count': count}