from asyncio import create_subprocess_exec, create_subprocess_shell
from pipes import Template
from time import sleep
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .models import Products, orderDetail
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from django.urls import reverse, reverse_lazy
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings as s
from django.views.decorators.csrf import csrf_exempt
import stripe

# Create your views here.
def index(request):
    return render(request, 'myapp/base.html')

def products(request):
    page_obj = productss = Products.objects.all()

    product_name = request.GET.get('product_name')
    
    if (product_name):
        page_obj = productss.filter(name__icontains=product_name)
    
    paginator = Paginator(page_obj, 3) # Paginates the objects by 3
    page_num = request.GET.get('page')  # Gets the page number from the request (.../?page=x)
    page_obj = paginator.get_page(page_num) # Gets the items within that page

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'myapp/index.html', context)

# class based view
class ProductListView(ListView):
    model = Products
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    paginate_by = 4

def product_detail(request, id):
    products = Products.objects.get(id=id)

    context = {
        'product': products
    }
    return render(request, 'myapp/detail.html', context)

# class based view
class ProductDetailView(DetailView):
    model = Products
    template_name = 'myapp/detail.html'
    context_object_name = 'product'
    
    pk_url_kwarg = 'pk' #kwarg is actually the id of the product for which the payment has to be done

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs) #gets context data
        context['stripe_publishable_key'] = s.STRIPE_PUBLIC_KEY   # modifies context
        return context

@login_required
def add_product(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        
        try:
            image = request.FILES['upload']
            product = Products(name=name, price=price, desc=desc, image=image, user=user)
        except Exception as e:
            print(e)
            product = Products(name=name, price=price, desc=desc, user=user)

        product.save()

        return redirect('/myapp/products')

    return render(request, 'myapp/addproduct.html')

# class based view
class ProductCreateView(CreateView):
    model = Products
    fields = ['user', 'name', 'price', 'desc', 'image']
    

def update_product(request, id):
    product = Products.objects.get(id=id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')
        product.image = request.FILES['upload']
        product.save()

        return redirect('/myapp/products')

    context = {
        'product': product
    }
    return render(request, 'myapp/updateprod.html', context)

class ProductUpdateView(UpdateView):
    model = Products
    fields = ['user', 'name', 'desc', 'price', 'image']
    template_name = 'myapp/prod_update_form.html'

def delete_product(request, id):
    product = Products.objects.get(id=id)
    context = {
        'product': product,
    }

    if (request.method == 'POST'):
        product.delete()
        return redirect('/myapp/products')
    
    return render(request, 'myapp/deleteprod.html', context=context)

class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'myapp/prod_delete.html'
    success_url = reverse_lazy('myapp:products')

@login_required
def my_listings(request):
    products = Products.objects.filter(user=request.user)
    context = {
        'products': products
    }
    return render(request, 'myapp/mylistings.html', context)

@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Products, pk=id)
    stripe.api_key = s.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email = request.user.email,
        payment_method_types = ['card'],
        line_items = [
            # Item1
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode = 'payment', # one-time payment OR subscription

        success_url = request.build_absolute_uri(reverse('myapp:success')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url = request.build_absolute_uri(reverse('myapp:failed')),
    )

    order = orderDetail()
    order.customer_username = request.user.username
    order.product = product
    order.checkout_session_id = checkout_session['id']
    order.amount = int(product.price * 100)
    order.save()

    return JsonResponse({'sessionId': checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = 'myapp/success.html'

    def get(self, request, *args, **kwargs):

        sessionId = request.GET.get('session_id') # gets session_id from URL (.../?sessoin_id=xxx)
        
        if not sessionId:
            return HttpResponseNotFound()
        
        session = stripe.checkout.Session.retrieve(sessionId)
        stripe.api_key = s.STRIPE_SECRET_KEY

        order = get_object_or_404(orderDetail, checkout_session_id=sessionId) # gets the order by matching 'strip_payment_intent' field
        order.has_paid = True
        order.payment_intent = session.payment_intent
        order.save()

        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = 'myapp/failed.html'
