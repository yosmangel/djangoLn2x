from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from mezzanine.blog.models import BlogPost
import csv

class Command(BaseCommand):
    help = 'Import blog articles from a csv file'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        lallen = User.objects.filter(username='lallen')
        with open(options['filepath'], newline='', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                blogPost = BlogPost(
                        title=row[0],
                        content=row[1],
                        publish_date=row[2],
                        country=row[3],
                        city=row[4],
                        source=row[5],
                        user=lallen.first(),
                        )
                print(blogPost.publish_date)

                # blogPost.save()
            self.stdout.write(self.style.SUCCESS(
                    'Successfully imported file'))
