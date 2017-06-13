from .models import *

def base_context(request):
    context = {'categories': Category.objects.all()}
    user = request.user
    if UserProfile.objects.filter(user = user).exists():
        buyer = UserProfile.objects.get(user = user)
        context.update({'cart': buyer.cart.all(), 'cart_total': buyer.cart_total})
    return context
