











from app.models import Basket


def basket_totals(request):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user, active=True)
        total_quantity = baskets.total_quantity()
    else:
        total_quantity = 0

    return {
        'total_quantity': total_quantity,
    }
