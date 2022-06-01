from django.db import models

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

from datetime import date


class Author(models.Model):
    name = models.CharField(max_length=255)
    graduation_year = models.SmallIntegerField()
    email = models.EmailField(blank=True)
    alias = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Scriptum(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    text = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD)
    text_rendered = RenderedMarkdownField()

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'scripta'

    def __str__(self):
        return self.title

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]

class Magazine(models.Model):
    editor_note = MarkdownField(rendered_field='editor_note_rendered', validator=VALIDATOR_STANDARD)
    editor_note_rendered = RenderedMarkdownField()

    scripta = models.ManyToManyField(Scriptum)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, editable=False, default='d')
    publication_date = models.DateField(editable=False, null=True, default=None)
    volume = models.SmallIntegerField(editable=False, null=True, default=None)
    issue = models.SmallIntegerField(editable=False, null=True, default=None)

    class Meta:
        ordering = ['volume', 'issue']

    def __str__(self):
        return f'Vol. {self.volume} Iss. {self.issue}' if self.status != 'd' else 'Draft'

    def publish(self):
        """Mark the Magazine as published and set the publication date,
        volume, and issue if it was previously a draft
        """

        # TODO: prevent status from switching back to 'd' if mag was EVER published
        match self.status:
            case 'd':
                self.publication_date = date.today()

                magazines_published_in_current_year = Magazine.objects.filter(
                    status='p', publication_date__year=self.publication_date.year
                )

                try:
                    latest_publication = Magazine.objects.filter(status='p').latest('publication_date')
                except Magazine.DoesNotExist:
                    latest_publication = None

                if latest_publication is None:
                    self.volume = 1
                    self.issue = 1
                elif magazines_published_in_current_year.count() > 0:
                    # If a magazine has been published this year,
                    # keep the same volume and increment issue,
                    self.volume = latest_publication.volume
                    self.issue = latest_publication.issue + 1
                else:
                    # otherwise, increment volume and reset issue
                    self.volume = latest_publication.volume + 1
                    self.issue = 1

                self.status = 'p'

            case 'p':
                # TODO: implement + test cases
                pass
            case 'w':
                # TODO: implement + test cases
                pass
        
        super(Magazine, self).save()
