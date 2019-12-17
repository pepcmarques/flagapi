import nltk

from collections import namedtuple

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from flagapi import settings

nltk.download('gutenberg')
nltk.download('punkt')

TASKS = ("flag_it",)

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


class FirstApi(APIView):
    """
    A view that returns the count of active users in JSON.
    """
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
