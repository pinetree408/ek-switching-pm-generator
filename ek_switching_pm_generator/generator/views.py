# coding: utf-8
from django.views.generic.base import TemplateView
from django.conf import settings
import pm

class GeneratorView(TemplateView):
    template_name = "generator/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(GeneratorView, self).get_context_data(*args, **kwargs)
        frequency = settings.BASE_DIR + "/frequency.txt"
        dictionary = settings.BASE_DIR + "/wordsKo.txt"
        generator = pm.Generator()
        context['result1'] = generator.calculator(frequency, 0)
        context['result2'] = generator.calculator(dictionary, 1)
        return context
