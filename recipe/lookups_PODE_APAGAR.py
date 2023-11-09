from ajax_select import register, LookupChannel
from .models import Ingredient


@register('delivery_points')
class IngredietLookup(LookupChannel):
    model = Ingredient

    def get_query(self, q, request):
        return self.model.objects.filter(name=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
