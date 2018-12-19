from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import App, AppGenre
from django.shortcuts import redirect
from django_filters.views import FilterView
from .forms import AppForm
from .filters import AppFilter

# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the Google Play Store index page.")

class AboutPageView(generic.TemplateView):
	template_name = 'googleapp/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'googleapp/home.html'


class AppListView(generic.ListView):
	model = App
	context_object_name = 'apps'
	template_name = 'googleapp/app.html'
	paginate_by = 300

	def get_queryset(self):
		return App.objects.all().order_by('app_name')

class AppDetailView(generic.DetailView):
	model = App
	context_object_name = 'app'
	template_name = 'googleapp/app_detail.html'




# Filter View
class AppFilterView(FilterView):
	filterset_class = AppFilter
	template_name = 'googleapp/app_filter.html'




# login
@method_decorator(login_required, name='dispatch')
class AppCreateView(generic.View):
	model = App
	form_class = AppForm
	success_message = "App data created successfully"
	template_name = 'googleapp/app_new.html'
	

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = AppForm(request.POST)
		if form.is_valid():
			app = form.save(commit=False)
			app.save()
			for genre in form.cleaned_data['genre']:
				AppGenre.objects.create(app=app, genre=genre)
			return redirect(app) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'googleapp/app_new.html', {'form': form})

	def get(self, request):
		form = AppForm()
		return render(request, 'googleapp/app_new.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class AppUpdateView(generic.UpdateView):
	model = App
	form_class = AppForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'app'
	# pk_url_kwarg = 'site_pk'
	success_message = "App data updated successfully"
	template_name = 'googleapp/app_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		app = form.save(commit=False)
		app.save()

		
		old_ids = AppGenre.objects\
			.values_list('genre_id', flat=True)\
			.filter(app_id=app.app_id)

		# New genres list
		new_genres = form.cleaned_data['genre']

		# TODO can these loops be refactored?

		# New ids
		new_ids = []

		# Insert new unmatched genre entries
		for genre in new_genres:
			new_id = genre.genre_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				AppGenre.objects \
					.create(app=app,genre=genre)

		# Delete old unmatched country entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				AppGenre.objects \
					.filter(app_id=app.app_id, genre_id=old_id) \
					.delete()

		return HttpResponseRedirect(app.get_absolute_url())




@method_decorator(login_required, name='dispatch')
class AppDeleteView(generic.DeleteView):
	model = App
	success_message = "App deleted successfully"
	success_url = reverse_lazy('apps')
	context_object_name = 'app'
	template_name = 'googleaoo/app_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		AppGenre.objects \
			.filter(app_id=self.object.app_id) \
			.delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())



