import nltk

from collections import namedtuple, defaultdict

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from flagapi import settings
from flagapi.classify.models import ClassificationChoices, ClassifiedSentences

nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')

TASKS = ("flag_it", "flag_ml", "include")

if settings.STEMMER == 'porter':
    stemmer = nltk.PorterStemmer()
elif settings.STEMMER == 'lancaster':
    stemmer = nltk.LancasterStemmer()

WORDS = ["abuse", "afflict", "agonize", "alienate", "antagonize", "asphyxiate", "bash", "batter", "beat", "beguile",
         "belittle", "bite", "brawl", "break", "bruise", "burn", "butcher", "castigate", "chastise", "choke", "claw",
         "coerce", "control", "convince", "cower", "criticize", "cut", "demean", "demoralize", "deprecate", "depress",
         "deride", "devastate", "disappoint", "discourage", "disgust", "dishearten", "disparage", "distress", "disturb",
         "divorce", "drown", "embarrass", "enrage", "exhaust", "fault", "fight", "flinch", "frighten", "grope", "hate",
         "hit", "horrify", "humiliate", "hunt", "hurl", "hurt", "injure", "insult", "intimidate", "isolate", "kick",
         "kill", "knock", "lash", "loathe", "love", "malign", "mock", "molest", "monitor", "mortify", "murder", "pity",
         "plow", "poison", "punch", "punish", "push", "pushed", "rape", "recoil", "reprimand", "ridicule", "sadden",
         "scare", "scratch", "scrutinize", "shame", "shock", "shoot", "shove", "sicken", "slam", "slap", "smack",
         "smash", "smother", "spank", "stab", "strike", "suffer", "suffocate", "tear", "tease", "terrify", "terrorize",
         "thrash", "threaten", "throw", "tire", "torment", "torture", "track", "victimize", "weary", "weep", "worry",
         "yell"]

WORDS = [stemmer.stem(w) for w in WORDS]


def get_words_in_database():
    words = []
    documents_tmp = defaultdict(list)
    documents = []
    sentences = ClassifiedSentences.objects.all()
    for sentence_obj in sentences:
        ws = nltk.word_tokenize(sentence_obj.sentence.lower())
        words.extend(ws)
        documents_tmp[sentence_obj.classification.__str__()].extend(ws)
    for cl in documents_tmp:
        documents_tmp[cl] = set(documents_tmp[cl])
    for k, v in documents_tmp.items():
        documents.append((v, k))
    return words, documents


def get_classification_choices():
    cl_choices = {}
    choices = ClassificationChoices.objects.all()
    for choice_obj in choices:
        cl_choices[choice_obj.classification.__str__()] = str(choice_obj.pk)
    return cl_choices


def document_features(document, word_feats):
    features = {}
    for word in word_feats:
        features[word] = (word in document)
        # features['contains(%s)' % word] = (word in document_words)
    return features


def replace_names(sentence="", to_replace="X"):
    # tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    # words = [w.lower() for w in tokenizer.tokenize(sentence.lower())]
    words = [w.lower() for w in nltk.word_tokenize(sentence.lower())]
    res = set(words).intersection(settings.FIRST_NAMES)
    if len(res) > 0:
        for w in res:
            sentence = sentence.replace(w.lower(), to_replace*(len(w)))
            sentence = sentence.replace(w.upper(), to_replace*(len(w)))
            sentence = sentence.replace(w.title(), to_replace * (len(w)))
    return sentence


def flag_it(sentence=""):
    words = [stemmer.stem(w) for w in nltk.word_tokenize(sentence.lower())]

    res = set(words).intersection(set(WORDS))
    if len(res) > 0:
        return True
    return False


class SimpleClassificationApi(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = request.data
        if not data:
            content = {"error": "no data received"}
        else:
            create_inquiry = namedtuple("Inquiry", "task sentences")
            try:
                inquiry = create_inquiry(**data)
            except TypeError:
                content = {"error": "data format error"}
                return Response(content)

            if inquiry.task not in TASKS:
                content = {"error": "task not recognized"}
                return Response(content)

            answer = {"task": inquiry.task, "sentences": []}

            for sentence in inquiry.sentences:
                sentence = replace_names(sentence, "X")
                flag = flag_it(sentence)
                answer["sentences"].append((sentence, flag))
            content = answer
        return Response(content)


def bag_of_words(words):
    return dict([w.lower(), True] for w in words if w not in nltk.corpus.stopwords.words('english'))


def classify_sentences(sentences=[]):
    WORDS_IN_DATABASE, DOCUMENTS_IN_DATABASE = get_words_in_database()
    ALL_WORDS = nltk.FreqDist(w.lower() for w in WORDS_IN_DATABASE)
    WORD_FEATURES = ALL_WORDS.keys()
    TRAIN_SET = [(document_features(d, WORD_FEATURES), c) for (d, c) in DOCUMENTS_IN_DATABASE]
    CLASSIFIER = nltk.NaiveBayesClassifier.train(TRAIN_SET)

    to_return = []
    for sentence in sentences:
        words = nltk.tokenize.word_tokenize(sentence)
        feats = bag_of_words(words)
        classify = CLASSIFIER.classify(feats)
        to_return.append((sentence, classify))

    return to_return


class MachineLearningClassificationApi(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        CLASSIFICATION_CHOICES = get_classification_choices()

        data = request.data
        if not data:
            content = {"error": "no data received"}
        else:
            create_inquiry = namedtuple("Inquiry", "task sentences")
            try:
                inquiry = create_inquiry(**data)
            except TypeError:
                content = {"error": "data format error"}
                return Response(content)

            if inquiry.task not in TASKS:
                content = {"error": "task not recognized"}
                return Response(content)

            l_classifications = classify_sentences(inquiry.sentences)

            answer = []
            for l_cl in l_classifications:
                if l_cl[0] == "":
                    answer.append((l_cl[0], "0"))
                else:
                    answer.append((l_cl[0], CLASSIFICATION_CHOICES[l_cl[1]]))

            content = {"result": answer, "choices": CLASSIFICATION_CHOICES}

        return Response(content)


class IncludeClassificationApi(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        CLASSIFICATION_CHOICES = get_classification_choices()

        data = request.data
        if not data:
            content = {"error": "no data received"}
        else:
            create_inquiry = namedtuple("Inquiry", "task sentences")
            try:
                inquiry = create_inquiry(**data)
            except TypeError:
                content = {"error": "data format error"}
                return Response(content)

            if inquiry.task not in TASKS:
                content = {"error": "task not recognized"}
                return Response(content)

            answer = []

            for sentence in inquiry.sentences:
                try:
                    s, c = sentence
                except (ValueError, TypeError):
                    content = {"error": "sentence format must be ['sentence', 'classification']"}
                    return Response(content)

                c_value = CLASSIFICATION_CHOICES.get(c, 'not found')

                if c_value == 'not found':
                    answer.append((s, "classification not found"))
                    continue

                try:
                    obj = ClassifiedSentences.objects.get(sentence=s)
                    if str(obj.classification) == c:
                        answer.append((s, "sentence already exists with '%s' classification" % c))
                        continue
                    msg = "sentence was updated with '%s' classification" % c
                except ClassifiedSentences.DoesNotExist:
                    obj = ClassifiedSentences(sentence=s, classification=ClassificationChoices(c_value))
                    msg = "sentence was included with '%s' classification" % c

                obj.save()
                answer.append((s, msg))

            content = {"result": answer}

        return Response(content)