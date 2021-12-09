from django.contrib import admin
from django.db import models
from .helper import get_latest_logs
from .models import TimezoneLog
from django.template.response import TemplateResponse
from api.global_variable import BASE_DIR
# Register your models here.


@admin.register(TimezoneLog)
class concat_logAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        text = get_latest_logs(BASE_DIR + '/timezone_calc/timezone.txt')
        html = "<br>".join(text.split('\n'))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            html=html,
        )
        print(context['html'])
        return TemplateResponse(request, "logs.html", context)