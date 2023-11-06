import sys, os, django
from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wey_backend.settings")
django.setup()


from post.models import Post, Trend

def extract_hashtags(text, trends):
    for word in text.split():
        if word[0] == '#' and len(word) >= 2:
            trends.append(word[1:])

    return trends

for trend in Trend.objects.all():
    trend.delete()

posts = Post.objects.all()
trends = []

this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
twenty_four_hours = this_hour - timedelta(hours=24)

for post in Post.objects.filter(created_at__gte = twenty_four_hours):
    extract_hashtags(post.body, trends)

trends_counter = Counter(trends).most_common(10)

for trend in trends_counter:
        Trend.objects.create(hashtag = trend[0], occurences = trend[1])


