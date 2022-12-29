from django import forms



class AuctionListingForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Title for your listing'
        }
        )
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us more your product',
            'rows': '3'
        }
        )
    )
    # This is the first price established when the user creates the listing.
    price = forms.DecimalField(
        label='Price',
        required=True,
        initial=0.00,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Starting price for listing',
            'min': '0.01',
            'step': '0.01'
        }
        )
    )

    import auctions.models

    category = forms.ChoiceField(choices=auctions.models.category_choices,
        label='Listing category',
        required=False,
        )

    image_url = forms.URLField(
        label='Image URL for your listing',
        required=False,
        initial='https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Symbol_thumbs_up.svg/185px-Symbol_thumbs_up.svg.png',
        widget=forms.TextInput(attrs={
            'placeholder': 'Image URL (optional)',
        }
        )
    )

    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     return category.lower()



    # def clean_starting_bid(self):
    #     amount = float(self.cleaned_data.get('starting_bid'))
    #     if isinstance(amount, float) and amount > 0:
    #         return amount
    #     print(amount)
    #     raise forms.ValidationError('Should be a number larger than zero!')


class CommentForm(forms.Form):
    text = forms.CharField(
        label='',
        initial='',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '50'
        }
        )
    )


class BidForm(forms.Form):
    bid = forms.DecimalField(required=True,
                             label='',
                             initial=0.00,
                             widget=forms.NumberInput(attrs={'placeholder': '',
                                                             'min': '0.01',
                                                             'step': '0.01'}))
