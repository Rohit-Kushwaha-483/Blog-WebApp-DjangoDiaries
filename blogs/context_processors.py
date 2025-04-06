def current_year(request):
    from datetime import datetime
    return {'current_year': datetime.now().year}

# ────────────────────────────────────────────────────────
from .models import Category

def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
