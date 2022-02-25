from django import forms

from django.apps import apps
get_model = apps.get_model

from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict
try:
    from django.utils.datastructures import MergeDict
    DICT_TYPES = (MultiValueDict, MergeDict)
except:
    DICT_TYPES = (MultiValueDict,)


class SearchableSelect(forms.CheckboxSelectMultiple):
    class Media:
        css = {
            'all': (
                'searchableselect/main.css',
            )
        }
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/jquery.init.js',
            'searchableselect/bloodhound.min.js',
            'searchableselect/typeahead.jquery.min.js',
            'searchableselect/main.js',
        )

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.search_field = kwargs.pop('search_field')
        self.lookup_field = kwargs.pop('lookup_field', 'pk')
        self.load_on_empty = kwargs.pop('load_on_empty', False)
        self.many = kwargs.pop('many', True)
        self.limit = int(kwargs.pop('limit', 10))

        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None, choices=()):
        if value is None:
            value = []

        if not isinstance(value, (list, tuple)):
            # This is a ForeignKey field. We must allow only one item.
            if isinstance(value, str) and self.lookup_field != 'pk' and ',' in value:
                # Fields of type ArrayField (array types in Postgres) are serialized
                # as strings with comma separated values
                value = value.split(',')
            else:
                value = [value]

        queryset = get_model(self.model).objects.filter(**{'{}__in'.format(self.lookup_field): value})

        values = [
            {'name': str(v), 'value': getattr(v, self.lookup_field)} for v in queryset
        ]

        final_attrs = self.build_attrs(attrs, extra_attrs={'name': name})

        return render_to_string('searchableselect/select.html', dict(
            field_id=final_attrs['id'],
            field_name=final_attrs['name'],
            values=values,
            model=self.model,
            search_field=self.search_field,
            lookup_field=self.lookup_field,
            load_on_empty=self.load_on_empty,
            limit=self.limit,
            many=self.many
        ))

    def value_from_datadict(self, data, files, name):
        if self.many and isinstance(data, DICT_TYPES):
            return data.getlist(name)
        return data.get(name, None)
