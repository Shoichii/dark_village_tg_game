from django.contrib import admin

from base.models import Ability, Buff, Debuff, Game, GameProcessJournal, Role, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'gender', 'birthday',
                    'player_role', 'last_action', 'bought',)
    list_filter = ('tg_id', 'gender', 'birthday',
                   'player_role', 'last_action', 'bought',)
    search_fields = ('tg_id', 'gender', 'birthday',
                     'player_role', 'last_action', 'bought',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'creature',
                    'boss', 'image', 'description')
    list_filter = ('name', 'gender', 'creature',
                   'boss', 'image', 'description')
    search_fields = ('name', 'gender', 'creature',
                     'boss', 'image', 'description')


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = ('name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'creator', 'status', 'start_time', 'end_time')
    list_filter = ('chat_id', 'creator', 'status', 'start_time', 'end_time')
    search_fields = ('chat_id', 'creator', 'status', 'start_time', 'end_time')


@admin.register(GameProcessJournal)
class GameProcessJournalAdmin(admin.ModelAdmin):
    list_display = ('inited_game', 'player_in_game', 'voted',
                    'selected_race', 'selected_victim')
    list_filter = ('inited_game', 'player_in_game', 'voted',
                   'selected_race', 'selected_victim')


@admin.register(Buff)
class BuffAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = ('name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Debuff)
class DebuffAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = ('name', 'description',)
    search_fields = ('name', 'description',)
