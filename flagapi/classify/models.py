from django.db import models


class ClassificationChoices(models.Model):
    classification = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return '{}'.format(self.classification)


class ClassifiedSentences(models.Model):
    classification = models.ForeignKey(ClassificationChoices, on_delete=models.CASCADE)
    sentence = models.CharField(max_length=256)

    def __str__(self):
        return '{} => {}'.format(self.sentence, self.classification)
