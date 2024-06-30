from django.contrib import admin

# Register your models here.
import cloudinary
from django.contrib import admin
from django.db.models.functions import Trunc
from django.utils import timezone
from django.utils.html import mark_safe
from ShareJourneysApp.models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from oauth2_provider.models import AccessToken

from django.utils.html import mark_safe
from django.urls import path
from django.db.models import Count, Avg, F, Sum,IntegerField,Func,Q,Subquery,ExpressionWrapper,FloatField
from django.template.response import TemplateResponse

class TruncDiv(Func):
    function = 'TRUNC'
    template = '%(function)s(%(expressions)s / %(connect)s %(dividend)s)'
    output_field = IntegerField()
class MyAdminSite(admin.AdminSite):
    site_header = 'shareJourney'

    def get_urls(self):
        return [path('stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        stats = Posts.objects.annotate(avg_rating=Avg('rating__rate')).values('title', 'avg_rating').order_by('-avg_rating')
        print(stats);
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


admin_site = MyAdminSite(name='shareJourney')


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Posts
        fields = '__all__'


class MyPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_date', 'updated_date', 'active']
    search_fields = ['title', 'content']
    list_filter = ['id', 'created_date', 'title']
    readonly_fields = ['my_image']
    form = PostForm

    def my_image(self, instance):
        if instance:
            if instance.image is cloudinary.CloudinaryResource:
                return mark_safe(f"<img width='120' src='{instance.image.url}' />")

            return mark_safe(f"<img width='120' src='/static/{instance.image.name}' />")

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'expires', 'created')
    search_fields = ('user__username',)
    list_filter = ('user', 'created')

     # Call get_username method to retrieve username


admin_site.register(AccessToken,AccessTokenAdmin)

admin_site.register(Posts, MyPostAdmin)
admin_site.register(User)
admin_site.register(Tag)
admin_site.register(Comments)
admin_site.register(JourneyPictures)
admin_site.register(CommentReply)
admin_site.register(TravelCompanion)
admin_site.register(CommentTick)
admin_site.register(Rating)
admin_site.register(Reports)
admin_site.register(Users_Report)
admin_site.register(DiaDiemDungChan)
admin_site.register(Local)
admin_site.register(Transportation)
admin_site.register(Journey)
admin_site.register(UserRoute)



