from django.views.generic.list import ListView
from .models import BrowsingHistory


class HistoryView(ListView):
    template_name = "history/view-histroy.jinja2"
    model = BrowsingHistory
    context_object_name = "history"

    def get_context_data(self, **kwargs):
        context = {
            "user_histroy": BrowsingHistory.objects.filter(user_id=self.request.user.id)
        }
        return context
