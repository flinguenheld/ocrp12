from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.decorators import staff_member_required

from .models import UserRole


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserEpicInline(admin.StackedInline):
    model = UserRole
    can_delete = False
    verbose_name_plural = 'UsersEpic'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    pass
    inlines = (UserEpicInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)




admin.site.register(UserRole)





# from django.contrib.auth.models import Group
# my_group = Group.objects.get(name='Managers') 


# my_user = User.objects.get(pk='2') 
# my_group.user_set.add(my_user)


class UserManagerArea(admin.AdminSite):
    site_header = 'User Manager area'


user_site = UserManagerArea(name='UserManagement')
# user_site.unregister(User)
user_site.register(User, UserAdmin)


# @admin.register(UserEpic, site=user_site)
# class UserManager(admin.ModelAdmin):
    # pass



