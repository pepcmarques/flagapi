from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from flagapi.classify.forms import SubmitSentenceForm, SupervisedClassificationForm
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from flagapi.classify.models import ClassificationChoices, ClassifiedSentences


# from django.contrib import messages
# messages.add_message(self.request, messages.INFO, self.form.cleaned_data["sentence"])


class ClassificationList(ListView):
    model = ClassificationChoices
    context_object_name = 'message_list'
    paginate_by = 10
    ordering = ['classification']

    def get_queryset(self):
        return ClassificationChoices.objects.all()


class ClassificationCreate(CreateView):
    model = ClassificationChoices
    fields = ['classification']
    success_url = reverse_lazy('classify:classification_list')


class ClassificationUpdate(UpdateView):
    model = ClassificationChoices
    fields = ['classification']
    success_url = reverse_lazy('classify:classification_list')


class ClassificationDelete(DeleteView):
    model = ClassificationChoices
    success_url = reverse_lazy('classify:classification_list')


class ClassifiedSentencesList(ListView):
    model = ClassifiedSentences
    context_object_name = 'message_list'
    # paginate_by = 10
    ordering = ['classification']

    def get_queryset(self):
        return ClassifiedSentences.objects.all()


class ClassifiedSentencesCreate(CreateView):
    model = ClassifiedSentences
    fields = ['sentence', 'classification']
    success_url = reverse_lazy('classify:classified_sentences_list')


class ClassifiedSentencesUpdate(UpdateView):
    model = ClassifiedSentences
    fields = ['sentence', 'classification']
    success_url = reverse_lazy('classify:classified_sentences_list')


class ClassifiedSentencesDelete(DeleteView):
    model = ClassifiedSentences
    success_url = reverse_lazy('classify:classified_sentences_list')


class SubmitSentenceView(FormView):
    template_name = 'submit_sentence.html'
    form_class = SubmitSentenceForm
    success_url = 'test.html'

    def __init__(self):
        self.form = None
        self.sentence = None
        super(SubmitSentenceView, self).__init__()

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def post(self, request):
        self.sentence = request.POST.get("sentence")
        return redirect('classify:automatic_classification', self.sentence)


class AutomaticClassificationView(FormView):

    def get(self, request, sentence):
        print(sentence)
        classification = 'not abuse'
        return redirect('classify:supervised_classification', sentence, classification)


class SupervisedClassificationView(FormView):
    template_name = 'automatic_classification.html'
    form_class = SupervisedClassificationForm
    success_url = 'test.html'
    initial = {'sentence': None, 'classification': None}

    def get(self, request, sentence, classification):
        print(sentence, classification)
        self.initial = {'sentence': sentence, 'classification': classification}
        context = self.get_context_data()
        print(context)
        return self.render_to_response(context)

    def form_valid(self, form):
        return redirect('classify:test', form.cleaned_data["sentence"], form.cleaned_data["classification"])
