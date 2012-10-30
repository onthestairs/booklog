from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from books.models import *
from books.forms import *
import openlibrary

def index(request):
	user = request.user
	if user.is_authenticated():
		return HttpResponseRedirect(reverse('books.views.brooks'))
	return render(request, 'home.html')

def register(request):
	if request.method == 'POST':
		signup_form = SignupForm(request.POST)
		if signup_form.is_valid():
			clean = signup_form.cleaned_data
			username = clean['username']
			password = clean['password']
			new_user = User.objects.create_user(username, password=password)
			new_user.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				user = login(request, user)
				return HttpResponseRedirect(reverse('books.views.brooks'))
			return HttpResponseRedirect(reverse('books.views.register'))
	else: 
		signup_form = SignupForm()
	return render(request, 'register.html', {'signup_form':signup_form})

@login_required
def brooks(request):
	user = request.user
	brooks = user.brook_set.all().order_by('-date_finished','-date_started')
	currently_reading = []
	years = {}
	for brook in brooks:
		if not brook.date_finished:
			currently_reading.append(brook)
		else:
			year = brook.date_finished.strftime('%Y')
			if year in years:
				years[year].append(brook)
			else:
				years[year] = [brook]
	return render(request, 'brooks.html', {'currently_reading':currently_reading, 'years':years} )
				
# here is a decorater to see if a user can access a brook
def user_brook_ok_decorator(f):
	def user_brook_ok(request, brook_id, *args, **kwarss):
		brook = get_object_or_404(Brook, pk=brook_id)
		##if the logged in user is not
		if not brook.user.id == request.user.id:
			return HttpResponseRedirect('/login/')
		else:
			return f(request,brook_id)
	return user_brook_ok

@login_required
@user_brook_ok_decorator
def brook(request, brook_id):
	brook = get_object_or_404(Brook, pk=brook_id)
	quotes = brook.quote_set.in_page_order()
	
	notes = brook.note_set.all().order_by('order')
	quote_form = QuoteForm()
	note_form = NoteForm()
	dates_form = DatesForm(instance=brook)
	
	try:
		review = brook.review
	except:
		review = None
		review_form = ReviewForm()
	else:
		review_form = ReviewForm(instance=review)

	return render(request, 'brook.html',{'brook':brook, 'quotes':quotes, 'review':review, 'notes':notes, 'QuoteForm':quote_form, 'NoteForm':note_form, 'ReviewForm':review_form, 'DatesForm':dates_form})

@login_required
@user_brook_ok_decorator
def add_quote(request, brook_id):
	if not request.method == 'POST':
		return HttpResponseRedirect('/brook/'+brook_id)
	brook = get_object_or_404(Brook, pk=brook_id)
	quote_form = QuoteForm(request.POST)
	if quote_form.is_valid():
		quote = quote_form.save(commit=False)
		brook.quote_set.add(quote)
	return HttpResponseRedirect('/brook/'+brook_id)

@login_required
@user_brook_ok_decorator
def add_note(request, brook_id):
	if not request.method == 'POST':
		return HttpResponseRedirect('/brook/'+brook_id)
	brook = get_object_or_404(Brook, pk=brook_id)
	NotesForm = NoteForm(request.POST)
	if NotesForm.is_valid():
		note = NotesForm.save(commit=False)
		note.order = brook.note_set.all().count() + 1
		brook.note_set.add(note)
	return HttpResponseRedirect('/brook/'+brook_id)

@login_required
@user_brook_ok_decorator
def add_review(request, brook_id):
	if not request.method == 'POST':
		return HttpResponseRedirect('/brook/'+brook_id)
	brook = get_object_or_404(Brook, pk=brook_id)
	review_form = ReviewForm(request.POST)
	if review_form.is_valid():
		review = review_form.save(commit=False)
		review.brook = brook
		review.save()
	return HttpResponseRedirect('/brook/'+brook_id)

@login_required
@user_brook_ok_decorator
def edit_review(request, brook_id):
	if not request.method == 'POST':
		return HttpResponseRedirect('/brook/'+brook_id)
	brook = get_object_or_404(Brook, pk=brook_id)
	review_form = ReviewForm(request.POST,instance=brook.review)
	if review_form.is_valid():
		review = review_form.save()
		# review.brook = brook
		# review.save()
	return HttpResponseRedirect('/brook/'+brook_id)

@login_required
@user_brook_ok_decorator
def brook_finished(request, brook_id):
	brook = get_object_or_404(Brook, pk=brook_id)
	dates_form = DatesForm(request.POST,instance=brook)
	if dates_form.is_valid():
		brook = dates_form.save()
	return HttpResponseRedirect('/brook/'+brook_id)

@login_required
@user_brook_ok_decorator
def change_brook_dates(request, brook_id):
	if not request.method == 'POST':
		return HttpResponseRedirect('/brook/'+brook_id)
	brook = get_object_or_404(Brook, pk=brook_id)
	dates_form = DatesForm(request.POST,instance=brook)
	if dates_form.is_valid():
		brook = dates_form.save()
	print dates_form.errors
	return HttpResponseRedirect('/brook/'+brook_id)

@login_required
def add_brook(request):
	if not request.method == 'POST':
		return HttpResponseRedirect(reverse('books.views.brooks'))
	isbn = request.POST['isbn']
	api = openlibrary.Api()
	#check if already in db
	try:
		book = Books.objects.get(isbn=isbn)
	except:
		try:
			ol_book = api.get_book(isbn)
		except KeyError:
			print "NO BOOK FOUND FFS"
			return HttpResponseRedirect(reverse('books.views.brooks'))
		if ol_book.cover is not None:
			image = ol_book.cover['medium']
		else:
			image = ''
		book = Book(isbn=isbn, title=ol_book.title, image=image)
		book.save()
		for a in ol_book.authors:
			try:
				author = Author.objects.get(name=a)
			except:
				author = Author(name=a)
				author.save()
			book.author_set.add(author)

	#create a brook from the book
	brook = Brook(user=request.user, book=book, date_started=timezone.now())
	brook.save()
	return HttpResponseRedirect(reverse('books.views.brook', args=(brook.id,)))

