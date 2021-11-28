from storehouse.models import Category


class CategoryManager:

    def get_categories(self):
        try:
            categories = Category.objects.all()
            return categories
        except Exception as ex:
            print(f'Exception was occurred while retrieving all categories. Exception: {ex}')

    def delete_category(self, category_id):
        try:
            category = Category.objects.filter(id=category_id)
            category.delete()
            return
        except Exception as ex:
            print(f'Exception was occurred while deleting category. Exception: {ex}')
