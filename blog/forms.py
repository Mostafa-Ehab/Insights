from django import forms
from .models import Blog, Tag
from django.utils.text import slugify
from tinymce.widgets import TinyMCE
from user_profile.models import User

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 6,
        "id": "message",
        "placeholder": "Type your comment",
    }), required=True, label=False)

class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea(attrs={
        "rows": 3,
        "id": "message",
        "placeholder": "Type your reply",
    }), required=True, label=False)

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")

        widgets = {
            # "username": forms.TextInput(attrs={
            #     "class": "form-control",
            #     "placeholder": "Enter your username (optional)"
            # }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your first name (optional)"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your last name (optional)"
            })
        }

    # def clean_username(self):
    #     if not (username := self.cleaned_data.get("username")):
    #         return None
        
    #     model = self.Meta.model
    #     user = model.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)

    #     if user.exists():
    #         raise forms.ValidationError("A user with that name already exist")

    #     return username

class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your new password"
    }), required=True)

    conf_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Confirm your new password"
    }), required=True)
    
    class Meta:
        model = User
        fields = ["password"]
            
        widgets = {
            "password": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your password"
            })
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not self.instance.check_password(password):
            raise forms.ValidationError("Incorrect password")
        
        return password

    def clean(self):
        if self.is_valid():
            password = self.cleaned_data.get("new_password")
            password2 = self.cleaned_data.get("conf_password")
            if password != password2:
                raise forms.ValidationError("Passwords don't match")
            
        return self.cleaned_data


class ProfileImageForm(forms.Form):
    profile_image = forms.ImageField(required=True)


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "category", "content", "banner"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the post title"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "content": TinyMCE(attrs={
                "class": "form-control",
                "placeholder": "An awesome article..."
            }),
            "banner": forms.FileInput(attrs={
                "class": "form-control h-100"
            }),
            # "tags": forms.HiddenInput(),
        }

    # def clean_tags(self):
    #     print("Got")
    #     # tags_list = [tag.strip() for tag in self.cleaned_data.get("tags").split(",")]

    #     # for tag in tags_list:
    #     #     if tag != "" and (tag_input := Tag.objects.filter(slug=slugify(tag))):
    #     #         tag_input = Tag(title = tag)
    #     #         tag_input.save()

    #     return [tag.strip() for tag in self.cleaned_data.get("tags").split(",")]
