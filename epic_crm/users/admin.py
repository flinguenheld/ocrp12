from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.decorators import staff_member_required

from .models import UserEpic


admin.site.register(UserEpic)



# from django.contrib.auth.models import Group
# my_group = Group.objects.get(name='Managers') 


# my_user = User.objects.get(pk='2') 
# my_group.user_set.add(my_user)


class UserManagerArea(admin.AdminSite):
    site_header = 'User Manager area'


user_site = UserManagerArea(name='UserManagement')
# user_site.register(User, UserManager)


@admin.register(UserEpic, site=user_site)
class UserManager(admin.ModelAdmin):
    pass



