from django import forms
from django.forms import ModelForm, Textarea, DateInput
from books.models import *

class UserField(forms.CharField):
	def clean(self, value):
		super(UserField, self).clean(value)
		try:
			User.objects.get(username=value)
			raise forms.ValidationError("Someone is already using this username. Please pick an other.")
		except User.DoesNotExist:
			return value

class SignupForm(forms.Form):
	username = UserField(max_length=30)
	password = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat your password")

	def clean_password(self):
		if self.data['password'] != self.data['password2']:
			raise forms.ValidationError('Passwords are not the same')
		return self.data['password']
    
	def clean(self,*args, **kwargs):
		self.clean_password()
		return super(SignupForm, self).clean(*args, **kwargs)

class QuoteForm(ModelForm):
	# page = forms.CharField(required=False,max_length=10)
	# quote = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Quote
		fields = ('page', 'quote')
		widgets = {
            'quote': Textarea(attrs={'cols': 80, 'rows': 3}),
        }

class ReviewForm(ModelForm):
	review = forms.CharField(widget=Textarea(attrs={'cols': 100, 'rows': 8, 'classs': "review_box"}), label='')
	
	class Meta:
		model = Review
		fields = ('review',)

class NoteForm(ModelForm):
	# page = forms.CharField(required=False,max_length=10)
	# quote = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Note
		fields = ('name', 'note')
		widgets = {
            'note': Textarea(attrs={'cols': 80, 'rows': 4}),
        }

class DatesForm(ModelForm):

	class Meta:
		model = Brook
		fields = ('date_started', 'date_finished')
		widgets = {
			'date_started': DateInput(format='%d/%m/%y', attrs={'class':'datePicker', 'readonly':'true'}),
			'date_finished': DateInput(format='%d/%m/%y', attrs={'class':'datePicker', 'readonly':'true'})
		}