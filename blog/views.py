# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView, FormView, ListView, DetailView

from blog.forms import ContactForm
from podcast.models import EpisodePodcast, Panelist
from podcasting.models import Show
from .models import Post


class AboutView(TemplateView):
    template_name = 'podcast/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['panelists'] = Panelist.objects.filter(status=True)
        return context


class ThanksView(TemplateView):
    template_name = 'podcast/thanks.html'


class ContactView(FormView):
    template_name = 'podcast/contact_us.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        contact_name = form.cleaned_data.get(
            'contact_name', '')
        contact_email = form.cleaned_data.get(
            'contact_email', '')
        subject = form.cleaned_data.get(
            'subject', '')
        form_content = form.cleaned_data.get('content', '')
        form_content = contact_name + ' dice: ' + form_content
        send_mail(
            subject,
            form_content,
            contact_email,
            ['hellocutiepie@pizzafria.com'],
            fail_silently=False,
        )
        return super(ContactView, self).form_valid(form)


class HomeEpisodeList(ListView):
    model = Post
    paginate_by = 11
    template_name = "podcast/home.html"

    def get_queryset(self):
        last = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        episodes = Post.objects.exclude(
            published=None
        ).exclude(
            pk=last.post.pk
        ).order_by('-published')

        return episodes

    def get_context_data(self, **kwargs):
        context = super(HomeEpisodeList, self).get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message', None)
        context['show'] = Show.objects.first().slug
        context['feed_type'] = 'mp3'
        context['itunes_url'] = settings.ITUNES_URL
        context['domain'] = settings.PODCAST_DOMAIN
        context['latest'] = EpisodePodcast.objects.exclude(
            episode__published__isnull=True).first()
        context['main_tags'] = context['latest'].episode.keywords.split(',')
        context['panelists'] = Panelist.objects.filter(status=True)

        return context


class EpisodeSingle(DetailView):
    template_name = "podcast/episode_single.html"

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_field, None)
        if slug:
            return EpisodePodcast.objects.get(episode__slug=slug)

    def get_context_data(self, **kwargs):
        context = super(EpisodeSingle, self).get_context_data(**kwargs)
        context['show'] = Show.objects.first().slug
        context['feed_type'] = 'mp3'
        context['itunes_url'] = settings.ITUNES_URL
        context['domain'] = settings.PODCAST_DOMAIN
        next_episode = EpisodePodcast.objects.filter(
            pk__gt=self.object.pk
        ).exclude(
            episode__published__isnull=True
        ).order_by('pk')

        next_episode = next_episode.first()

        prev_episode = EpisodePodcast.objects.filter(
            pk__lt=self.object.pk
        ).exclude(
            episode__published__isnull=True
        ).order_by('-pk')
        prev_episode = prev_episode.first()

        context['next'] = next_episode
        context['prev'] = prev_episode

        # Time marks
        time_marks = []
        timemarks = self.object.episode.tracklist
        if timemarks:
            timemarks = timemarks.splitlines()
            for timemark in timemarks:
                timemark = timemark.split('-')
                try:
                    seconds = timemark[0]
                    mark = timemark[1]
                except ValueError:
                    print 'malformed timemark', timemark
                    continue
                m, s = divmod(int(seconds), 60)
                h, m = divmod(m, 60)
                if h:
                    human_time = "%d:%02d:%02d" % (h, m, s)
                else:
                    human_time = "%02d:%02d" % (m, s)
                time_marks.append(dict(human_time=human_time,
                                       seconds=seconds, mark=mark))
        context['time_marks'] = time_marks
        return context
