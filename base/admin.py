from django.contrib import admin

from base.models import Ability, Game, Role, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'gender', 'birthday', 'bought',)
    list_filter = ('tg_id', 'gender', 'birthday', 'bought',)
    search_fields = ('tg_id', 'gender', 'birthday', 'bought',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'image', 'description')
    list_filter = ('name', 'gender', 'image', 'description')
    search_fields = ('name', 'gender', 'image', 'description')


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'passive', 'damage', 'action_time')
    list_filter = ('name', 'description', 'passive', 'damage', 'action_time')
    search_fields = ('name', 'description', 'passive', 'damage', 'action_time')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('creater', 'status')
    list_filter = ('creater', 'status')
    search_fields = ('creater', 'status')
