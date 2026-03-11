from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Category, OrderItem,Order,Profile
from django.db.models import Q,Sum

from .forms import OrderForm,ProductForm,CategoryForm,SignUpForm,ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm,ProductForm,SignUpForm
from django.contrib.auth.decorators import login_required,user_passes_test
 
from django.contrib.admin.views.decorators import staff_member_required






def home(request):
    categories = Category.objects.all()
    return render(request, 'trade/home.html', {'categories': categories})


def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'trade/category_products.html', {
        'category': category,
        'products': products
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)
    return render(request, 'trade/detail.html', {
        'product': product,
        'related_products': related_products
    })


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__name__icontains=query)
    )
    return render(request, 'trade/search.html', {'products': products, 'query': query})


#afficher-detail-commande#


@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'trade/order_detail.html', {'order': order})







#panier#

@login_required(login_url='login')

def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    product = Product.objects.get(id=id)

    if str(id) in cart:
        cart[str(id)]['quantity'] += 1
    else:
        cart[str(id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url
        }

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'trade/cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart_detail')


def update_cart(request, id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity'))

    if str(id) in cart:
        cart[str(id)]['quantity'] = quantity

    request.session['cart'] = cart
    return redirect('cart_detail')



#commande#






def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Votre panier est vide.")
        return redirect('home')

    total = sum(item['price'] * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = total
            order.save()

            # Créer les OrderItems
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity']
                )

            # Vider le panier
            request.session['cart'] = {}
            messages.success(request, "Commande effectuée avec succès !")
            return redirect('paiement')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = OrderForm()

    return render(request, 'trade/checkout.html', {'form': form, 'cart': cart, 'total': total})

def paiement(request):
    return render(request,'trade/paiement.html')





#account#




def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            image = request.FILES.get('image')

            Profile.objects.create(
                user=user,
                image=image if image else 'profil/default.webp'
            )

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'trade/signup.html', {'form': form})


# profil



@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        profile = request.user.profile
        profile.image = request.FILES['image']
        profile.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # authenticate ici
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username} !")
                return redirect('home')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    else:
        form = AuthenticationForm()
    return render(request, 'trade/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté")
    return redirect('home')



#admin#



@staff_member_required
def dashboard(request):
    total_ventes = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    total_commandes = Order.objects.count()
    total_produits = Product.objects.count()
    produits_faible_stock = Product.objects.filter(stock__lte=5)
    total_categories = Category.objects.count()
    commandes_recentes = Order.objects.order_by('-created_at')[:5]  # 5 dernières commandes

    context = {
        'total_ventes': total_ventes,
        'total_commandes': total_commandes,
        'total_produits': total_produits,
        'produits_faible_stock': produits_faible_stock,
        'total_categories': total_categories,
        'commandes_recentes': commandes_recentes,
    }
    return render(request, 'trade/dashboard.html', context)






# Dashboard liste produits
@staff_member_required
def product_dashboard(request):
    produits = Product.objects.all()
    return render(request, 'trade/product_dashboard.html', {'produits': produits})

# Ajouter un produit
@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_dashboard')
    else:
        form = ProductForm()
    return render(request, 'trade/product_form.html', {'form': form, 'title': 'Ajouter un produit'})

# Modifier un produit
@staff_member_required
def edit_product(request, id):
    produit = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('product_dashboard')
    else:
        form = ProductForm(instance=produit)
    return render(request, 'trade/product_form.html', {'form': form, 'title': 'Modifier le produit'})

# Supprimer un produit
@staff_member_required
def delete_product(request, id):
    produit = get_object_or_404(Product, id=id)
    produit.delete()
    return redirect('product_dashboard')


@user_passes_test(lambda u: u.is_staff)  # seulement admin
def main_dashboard(request):
    return render(request, 'trade/main_dashboard.html')



@user_passes_test(lambda u: u.is_staff)
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'trade/users_list.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def category_dashboard(request):
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_dashboard')
    else:
        form = CategoryForm()

    return render(request, 'trade/category_dashboard.html', {
        'form': form,
        'categories': categories
    })


