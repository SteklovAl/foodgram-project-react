from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredientDetails, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredientDetails
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'favorites')
    search_fields = ('text',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'
    inlines = (RecipeIngredientInline, )

    def favorites(self, obj):
        return obj.favorites.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
