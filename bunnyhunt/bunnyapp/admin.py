from django.contrib import admin

from bunnyapp.models import Forest, Hunter, Rabbit, Tree, Burrow

admin.site.register(Forest)
admin.site.register(Hunter)
admin.site.register(Tree)


class RabbitAdmin(admin.ModelAdmin):
    list_display = ('speed', 'color', 'kilometers', 'position_x', 'position_y', 'message')


class BurrowAdmin(admin.ModelAdmin):
    list_display = ('position_x', 'position_y', 'occupied')


admin.site.register(Rabbit, RabbitAdmin)
admin.site.register(Burrow, BurrowAdmin)
