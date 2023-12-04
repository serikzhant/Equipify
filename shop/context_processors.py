from .models import Category


def categories(request):
    """
    Retrieves all categories from the database that do not have a parent category.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
