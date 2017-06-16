from .models import *

def base_context(request):
    context = {'categories': Category.objects.all()}
    user = request.user
    if request.user.is_authenticated() and UserProfile.objects.filter(user = user).exists():
        buyer = UserProfile.objects.get(user = user)
        cart = []
        for item in buyer.cart.all():
            if item.product in cart:
                product = list.pop()
        context.update({'cart': buyer.cart.all(), 'cart_total': buyer.cart_total})
    return context
