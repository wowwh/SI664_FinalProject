import django_filters
from googleapp.models import App,Category


class AppFilter(django_filters.FilterSet):
    
    
    app_name = django_filters.CharFilter(
		field_name='app_name',
		label='Google Store App',
		lookup_expr='icontains'
	)

    

    updated_time = django_filters.CharFilter(
        field_name='updated_time',
		label='Updated Time',
		lookup_expr='icontains'
    )


    category = django_filters.ModelChoiceFilter(
        field_name='category',
		label='Category',
		queryset=Category.objects.all().order_by('category_name'),
		lookup_expr='exact'
    )

    
    


    class Meta:
        model = App
        # form = SearchForm
        # fields [] is required, even if empty.
        fields = []