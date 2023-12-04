from django.shortcuts import get_object_or_404, render

from .models import Category, ProductProxy


def products_view(request):
    """
    Renders the products view.
    """
    categories = Category.objects.all()
    products = ProductProxy.objects.all()
    context = {'categories': categories, 'products': products}
    return render(request, 'shop/products.html', context)


def product_detail_view(request, slug):
    """
    Renders the product detail view.
    """
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request, slug):
    """
    Renders the category list view.
    """
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related(
        'category').filter(category=category)
    context = {'products': products, 'category': category}
    return render(request, 'shop/category_list.html', context)
