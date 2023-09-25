from django import forms
from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'subtitle', 'description', 'starting_bid', 'image_url', 'category']
        

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['offer']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        