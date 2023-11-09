# django.formsをインポート
from django import forms
from django.forms import ModelForm
from .models import BlogPost, BlogComment, BlogReply

class ContactForm(forms.Form):
    #
    name = forms.CharField(label="お名前")
    email = forms.EmailField(label="メールアドレス")
    title = forms.CharField(label="件名")
    message = forms.CharField(label="メッセージ", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        '''ContactFormのコンストラクター

        フィールドの初期設定を行う
        '''
        super().__init__(*args, **kwargs)
        # nameフィールドのplaceholderにメッセージを登録
        self.fields['name'].widget.attrs['placeholder'] = \
            'お名前を入力してください。'
        # nameフィールドを出力する<input>タグのclass属性を設定
        self.fields['name'].widget.attrs['class'] = 'form-control'

        # emailフィールドのplaceholderにメッセージを登録
        self.fields['email'].widget.attrs['placeholder'] = \
            'メールアドレスを入力してください'
        # emailフィールドを出力する<input>タグのclass属性を設定
        self.fields['email'].widget.attrs['class'] = 'form-control'

        # titleフィールドのplaceholderにメッセージを登録
        self.fields['title'].widget.attrs['placeholder'] = \
            'タイトルを入力してください'
        # titleフィールドを出力する<input>タグのclass属性を設定
        self.fields['title'].widget.attrs['class'] = 'form-control'

        # messageフィールドのplaceholdにメッセージを登録
        self.fields['message'].widget.attrs['placeholder'] = \
            'メッセージを入力してください'
        # messageフィールドを出力する<input>タグのclass属性を設定
        self.fields['message'].widget.attrs['class'] = 'form-control'

class BlogPostForm(ModelForm):
    '''ModelFormのサブクラス
    '''
    class Meta:
        '''ModelFormのインナークラス

        Attributes:
            model: モデルのクラス
            fields: フォームで使用するモデルのフィールドを指定
        '''
        model = BlogPost
        fields = ['category', 'title', 'content']


class BlogCommentCreateForm(forms.ModelForm):
    """コメントフォーム"""
    class Meta:
        model = BlogComment
        exclude = ('target', 'created_at')
        fields = ['writer', 'text', 'target', 'created_at']


class BlogReplyCreateForm(forms.ModelForm):
    """コメントフォーム"""
    class Meta:
        model = BlogReply
        exclude = ('target', 'created_at')