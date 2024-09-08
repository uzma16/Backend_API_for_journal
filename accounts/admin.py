from django.contrib import admin
from .models import User
import csv
from django.http import HttpResponse

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')
    list_filter = ('is_superuser', 'zodiac_sign')
    actions = ['export_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mydata.csv"'

        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Email', 'Phone'])

        for obj in queryset:
            writer.writerow([obj.full_name, obj.email, obj.phone])

        return response


admin.site.register(User, UserAdmin)