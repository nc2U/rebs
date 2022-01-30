from django import forms

from board.models import Post, Link, File, LawsuitCase

LinkInlineFormSet = forms.models.inlineformset_factory(
    Post,
    Link,
    fields=['link'],
    extra=3,
    can_delete=True,
    can_delete_extra=False
)

FileInlineFormSet = forms.models.inlineformset_factory(
    Post,
    File,
    fields=['file'],
    extra=1,
    can_delete=True,
    can_delete_extra=False
)


class LawsuitPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('is_notice', 'lawsuit', 'title', 'execution_date', 'content')

    def __init__(self, project, *args, **kwargs):
        super(LawsuitPostForm, self).__init__(*args, **kwargs)
        self.fields['lawsuit'].queryset = LawsuitCase.objects.filter(project=project)


class LawsuitCaseFrom(forms.ModelForm):
    class Meta:
        model = LawsuitCase
        exclude = ('project', 'register')
