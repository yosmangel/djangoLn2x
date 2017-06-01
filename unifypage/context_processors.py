from .models import MultilangKeyword

def all_multilang_keywords(request):
    all_multilang_keywords = MultilangKeyword.objects.all()
    return {'all_multilang_keywords': all_multilang_keywords}
