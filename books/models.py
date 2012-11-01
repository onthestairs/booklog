from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=500)
	isbn = models.CharField(max_length=13, unique=True)
	image = models.CharField(max_length=500)

	def keywords(self):
		keywords = self.title.lower().split()
		for a in self.authors():
			keywords += a.name.lower().split()
		return keywords

	def authors(self):
		return self.author_set.all()

	def authors_string(self):
		return ', '.join([author.name for author in self.author_set.all()])

	def __unicode__(self):
		return self.title

class Author(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length=500)
	books = models.ManyToManyField(Book)

class Brook(models.Model):
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	date_started = models.DateField()
	date_finished = models.DateField(null=True, blank=True)

class QuoteManager(models.Manager):
    def in_page_order(self, *args, **kwargs):
        qs = self.get_query_set().filter(*args, **kwargs)
        return sorted(qs, key=lambda q: int(q.page.split('-')[0]))

class Quote(models.Model):
	quote = models.TextField()
	page = models.CharField(max_length=10)
	brook = models.ForeignKey(Brook)
	objects = QuoteManager()


class Review(models.Model):
	review = models.TextField()
	brook = models.OneToOneField(Brook)

class Note(models.Model):
	order = models.IntegerField()
	note = models.TextField()
	name = models.CharField(max_length=200)
	brook = models.ForeignKey(Brook)
