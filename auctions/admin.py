from django.contrib import admin

from .models import Category, Listing, Bid, Comment
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ['name',]
    

# Bid Inline for Listing:
class BidInline(admin.TabularInline):
    model = Bid
    extra = 1  # number of empty forms


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'current_price', 'active', 'created_date', 'creator')
    list_filter = ('active', 'created_date', 'category')
    search_fields = ['title', 'description']
    inlines = [BidInline]

    # Custom Actions:
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(active=True)

    make_active.short_description = "Mark selected listings as active"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)

    make_inactive.short_description = "Mark selected listings as inactive"


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'auction', 'user', 'offer', 'date')
    list_filter = ('auction', 'user', 'date')
    search_fields = ['user__username', 'offer']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'user', 'created_date')
    list_filter = ('listing', 'user', 'created_date')
    search_fields = ['user__username', 'comment']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)


