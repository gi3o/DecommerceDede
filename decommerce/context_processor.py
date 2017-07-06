from .models import *

def base_context(request):
    context = {'categories': Category.objects.all()}
    user = request.user
    if request.user.is_authenticated():
        context.update({'is_buyer': user.groups.filter(name='Buyer').exists(), 'is_seller': user.groups.filter(name='Seller').exists()})
        if UserProfile.objects.filter(user = user).exists():
            buyer = UserProfile.objects.get(user = user)
            context.update({'cart': buyer.cart.all(), 'cart_total': buyer.cart_total})
    return context
