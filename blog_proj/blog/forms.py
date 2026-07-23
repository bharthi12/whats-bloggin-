#we want to ceate a html form 
#To avoid the issues and execptions and make it more user friendly-
# cases of usecase like='" ",

from django import forms

class PostForm(forms.Form):
    title=forms.CharField(max_length=200)
    content=forms.CharField(
        widget=forms.Textarea
    )