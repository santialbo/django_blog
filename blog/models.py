from django.db import models
from markdown2 import markdown

class Author(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.name


class Entry(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length = 100)
    text = models.TextField()
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)

    def text_html(self):
        return markdown(self.text)

    def comments(self):
        return Comment.objects.filter(entry_id = self.id).order_by('-date')

    def summary_html(self):
        if len(self.text) > 400:
            return markdown(self.text[:400] + "...")
        else:
            return markdown(self.text)

    def __unicode__(self):
        date = str(self.date.day) + "/" + str(self.date.month) + "/" + str(self.date.year)
        return self.title + " by " + self.author.name + " on " + date


class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    name = models.CharField(max_length = 50)
    comment = models.TextField()
    date = models.DateTimeField()

    def __unicode__(self):
        date = str(self.date.day) + "/" + str(self.date.month) + "/" + str(self.date.year)
        return self.name + " on " + date + ": " + self.comment[:100]
