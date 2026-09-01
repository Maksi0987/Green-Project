from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib import messages

from main.models import Product, Category
from .forms import ContactForm


def product_list(request, category_slug=None):
    products = Product.objects.select_related('category').filter(is_active=True)
    categories = Category.objects.all()
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sort = request.GET.get('sort', 'new')

    if sort == 'new':
        products = products.order_by('-created_at')
    elif sort == 'old':
        products = products.order_by('created_at')
    elif sort == 'popular':
        products = products.order_by('-views', '-created_at')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    context = {
        'title': "Список продуктів",
        'products': products,
        'categories': categories,
        'category': category,
        'current_sort': sort,
    }

    return render(request, 'main/product_list.html', context)

def product_detail(request, id ,slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        id=id,
        slug=slug,
        is_active=True
    )

    Product.objects.filter(id=id).update(views=F('views') + 1)
    product.refresh_from_db(fields=['views'])

    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id).select_related('category')[:4]

    context = {
        'title': product.name,
        'product': product,
        'related_products': related_products
    }

    return render(request, 'main/product_detail.html', context)

def contact_view(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Від: {name} <{email}>\n\nПовідомлення:\n{message}"

            try:
                send_mail(
                    subject=subject,
                    message=full_message,
                    from_email=email,
                    recipient_list=['admin@greenstore.com'],
                    fail_silently=False,
                )
                messages.success(request, "Ваше повідомлення успішно відправлено!")
                return redirect('main:contact')
            except Exception as e:
                messages.error(request, f"Помилка при відправленні: {e}")
    else:
        form = ContactForm()

    context = {
        'title': 'Зворотний зв\'язок',
        'form': form,
        'categories': categories,
    }
    return render(request, 'main/contact.html', context)