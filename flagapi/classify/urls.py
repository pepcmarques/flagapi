from django.urls import path
from django.views.generic import TemplateView

from flagapi.classify.views import ClassificationList, ClassificationCreate, ClassificationUpdate, \
    ClassificationDelete, SubmitSentenceView, AutomaticClassificationView, SupervisedClassificationView, \
    ClassifiedSentencesList, ClassifiedSentencesCreate, ClassifiedSentencesUpdate, ClassifiedSentencesDelete

app_name = 'classify'

urlpatterns = [
    path('classification/', ClassificationList.as_view(), name='classification_list'),
    path('classification/create/', ClassificationCreate.as_view(), name='classification_create'),
    path('classification/update/<int:pk>', ClassificationUpdate.as_view(), name='classification_update'),
    path('classification/delete/<int:pk>', ClassificationDelete.as_view(), name='classification_delete'),

    path('classified_sentences/', ClassifiedSentencesList.as_view(), name='classified_sentences_list'),
    path('classified_sentences/create/', ClassifiedSentencesCreate.as_view(), name='classified_sentences_create'),
    path('classified_sentences/update/<int:pk>', ClassifiedSentencesUpdate.as_view(), name='classified_sentences_update'),
    path('classified_sentences/delete/<int:pk>', ClassifiedSentencesDelete.as_view(), name='classified_sentences_delete'),

    path('submit_sentence/', SubmitSentenceView.as_view(), name='submit_sentence'),
    path('automatic_classification/<str:sentence>', AutomaticClassificationView.as_view(),
         name='automatic_classification'),
    path('supervised_classification/<str:sentence>/<str:classification>',
         SupervisedClassificationView.as_view(), name='supervised_classification'),
    path('test/<str:sentence>/<str:classification>',
         TemplateView.as_view(template_name="test.html"), name='test'),
]
