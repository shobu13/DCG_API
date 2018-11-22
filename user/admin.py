from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdminCustom(UserAdmin):
    UserAdmin.fieldsets += (
                               'Détails', {
                                   'fields': ('city', 'postal_code', 'street', 'phone_number',
                                              'birth_date', 'photo')
                               },
                           ), (
                               'Confidentialitée', {
                                   'fields': ('act_prop_tous', 'act_part_visible', 'act_part_tous',
                                              'stay_connected')
                               },
                           ), (
                               'Social', {
                                   'fields': ('amis', 'est_verif')
                               },
                           ),
    filter_horizontal = ('amis', )

    for i in UserAdmin.fieldsets[1:]:
        i[1]['classes'] = ('collapse', )


admin.site.register(User, UserAdminCustom)
