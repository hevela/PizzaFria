from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

try:
    from imagekit.admin import AdminThumbnail
except ImportError:
    AdminThumbnail = None

from podcasting.forms import AdminShowForm, AdminEpisodeForm, EnclosureForm as AdminEnclosureForm
from podcasting.models import Show, Episode, Enclosure, EmbedMedia
from podcasting.utils.twitter import can_tweet


class ShowAdmin(admin.ModelAdmin):
    form = AdminShowForm

    list_display = ["title", "slug", "show_sites", "published_flag"]
    list_filter = ["title", "published", "sites"]
    if AdminThumbnail:
        list_display.append("admin_thumbnail")
        admin_thumbnail = AdminThumbnail(image_field="admin_thumb_sm")

    if can_tweet():
        fields.append("tweet_text")  # noqa

    def published_flag(self, obj):
        return bool(obj.published)
    published_flag.short_description = _("Published")
    published_flag.boolean = True

    def show_sites(self, obj):
        return ', '.join([site.name for site in obj.sites.all()])
    show_sites.short_description = "Sites"


class EpisodeAdmin(admin.ModelAdmin):
    form = AdminEpisodeForm

    list_display = ["title", "episode_shows", "slug", "episode_sites", "published_flag"]
    list_filter = ["shows", "published"]
    if AdminThumbnail:
        list_display.append("admin_thumbnail")
        admin_thumbnail = AdminThumbnail(image_field="admin_thumb_sm")

    if can_tweet():
        readonly_fields = ("tweet_text",)

    def published_flag(self, obj):
        return bool(obj.published)
    published_flag.short_description = _("Published")
    published_flag.boolean = True

    def episode_shows(self, obj):
        return obj.shows.title
    episode_shows.short_description = "Shows"

    def episode_sites(self, obj):
        return obj.shows.title
    episode_sites.short_description = "Sites"


class EnclosureAdmin(admin.ModelAdmin):
    form = AdminEnclosureForm

    list_display = ("mime", "url")
    list_filter = ("mime", "episodes")


class EmbedMediaAdmin(admin.ModelAdmin):
    model = EmbedMedia

admin.site.register(Show, ShowAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Enclosure, EnclosureAdmin)
admin.site.register(EmbedMedia, EmbedMediaAdmin)
