from django import template


register = template.Library()

bad_words = ['Супермен', 'супермен']

@register.filter()
def censor(text):
    censor_text = text
    for bad_word in bad_words:
        censor_text = censor_text.replace(bad_word, bad_word[:1] + '*' * (len(bad_word) - 1))

    return f'{censor_text}'