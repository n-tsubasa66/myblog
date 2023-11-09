from django.shortcuts import redirect, render
# djnago.views.genericからListView,DetailViewをインポート
from django.views.generic import ListView, DetailView, TemplateView
# モデルBlogPostをインポート
from .models import BlogComment, BlogPost, BlogReply
# django.views.genericからFormViewをインポート
from django.views.generic import FormView
# django.urlsからrevrse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからCntactFormをインポート
from .forms import BlogCommentCreateForm, ContactForm
# django.contribからmesseagesをインポート
from django.contrib import messages
# django.core.mailモジュールからEmailMessageをインポート
from django.core.mail import EmailMessage

# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import BlogPostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required

# django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView
# django.views.genericからDeleteViewをインポート
from django.views.generic import UpdateView
from django.contrib import messages


from django.http import JsonResponse  # 追加
from django.shortcuts import get_object_or_404  # 追加
from django.views import generic
from .models import LikeForBlogPost


from .forms import BlogCommentCreateForm, BlogReplyCreateForm
from django import forms


class IndexView(ListView):
    '''トップページのビュー

    投稿記事を一覧表示するのでListViewを継承する

    Attributes:
        template_name レンダリングするテンプレート
        context_object_name: oject_listキーの別名を設定
        queryset: データベースのクエリ
    '''
    # index.htmlをレンダリングする
    template_name = "index2.html"
    # object_listキーの別名を設定
    # context_object_name = "orderby_records"
    #モデルBlogPostのオブジェクトにorder_by()を適用して
    #BlogPostのレコードを投稿日時の降順で並べ替える
    queryset = BlogPost.objects.order_by("-posted_at")
    # 1ページに表示するレコードの件数を設定
    paginate_by = 4

class BlogDetail(DetailView):
    '''詳細ページのビュー

    投稿記事の詳細を表示するのでDetailViewを継承する

    Attributes:
        template_name: レンダリングするテンプレート
        Model: モデルのクラス
    '''
    
    # Post.htmlをレンダリングする
    template_name ='post.html'
    # クラス変数modelにモデルBlogPostを設定
    model = BlogPost


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_for_blogpost_count = self.object.likeforblogpost_set.count()
        # ポストに対するイイね数
        context['like_for_blogpost_count'] = like_for_blogpost_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.likeforblogpost_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_blogpost'] = True
        else:
            context['is_user_liked_for_blogpost'] = False

        return context


def like_for_blogpost(request):
    blogpost_pk = request.POST.get('blogpost_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    post = get_object_or_404(BlogPost, pk=blogpost_pk)
    like = LikeForBlogPost.objects.filter(target=post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=post, user=request.user)
        context['method'] = 'create'

    context['like_for_blogpost_count'] = post.likeforblogpost_set.count()

    return JsonResponse(context)





class ScienceView(ListView):
    '''科学(science)カテゴリの記事を一覧表示するビュー

    '''
    # science_list.htmlをレンダリングする
    template_name ="science_list.html"
    # クラス変数modelにモデルBlogPostを設定
    model = BlogPost
    #object_listキーの別名を設定
    context_object_name = "science_records"
    # category="science"のレコードを抽出して
    # 投稿日時の降順で並べる
    queryset = BlogPost.objects.filter(
        category="science").order_by("-posted_at")
    # 1ページに表示するレコードの件数
    paginate_by = 3

class DailylifeView(ListView):
    '''日常(dailylife)カテゴリの記事を一覧表示するビュー

    '''
    # dailylife_list.htmlをレンダリングする
    template_name ="dailylife_list.html"
    # クラス変数modelにモデルBlogPostを設定
    model = BlogPost
    # object_listキーの別名を設定
    context_object_name = "dailylife_records"
    # category="dailylife"のレコードを抽出して
    # 投稿日時の降順で並べる
    queryset = BlogPost.objects.filter(
        category="dailylife").order_by("-posted_at")
    # 1ページに表示するレコードの件数
    paginate_by = 3

class MusicView(ListView):
    '''音楽(music)カテゴリの記事を一覧表示するビュー

    '''
    # music_list.htmlをレンダリングする
    template_name ="music_list.html"
    # クラス変数modelにモデルBlogPostを設定
    model = BlogPost
    # object_listキーの別名を設定
    context_object_name = "music_records"
    # category="music"のレコードを抽出して
    # 投稿日時の降順で並べる
    queryset = BlogPost.objects.filter(
        category="music").order_by("-posted_at")
    #
    paginate_by = 3

class ContactView(FormView):
    '''問い合わせページを表示するビュー

    フォームで入力されたデータを取得し、メール作成と送信を行う
    '''
    # contact.htmlをレンダリングする
    template_name = "contact.html"
    # クラス変数form_classにforms.pyで定義したContactFormを設定
    form_class = ContactForm
    # 送信完了後にリダイレクトするページ
    success_url = reverse_lazy("blogapp:contact")

    def form_valid(self, form):
        '''FormViewクラスのform_valid()をオーバーライド

        フォームのバリデーションを通過したデータがPOSTされたときに呼ばれる
        メール送信を行う

        parameters:
            form(object): ContactFormのオブジェクト
        Return:
            HttpResposeRedirectのオブジェクト
            オブジェクトをインスタンス化するとsuccess_urlで
            設定されているURLでリダイレクトされる
        '''
        # フォームに入力されたデータをフィールド名を指定して取得
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        title = form.cleaned_data["title"]
        message = form.cleaned_data["message"]
        # メールのタイトル書式を設定
        subject = "お問い合わせ: {}".format(title)
        # フォームの入力データの書式を設定
        message = \
            "送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:\n{3}" \
            .format(name, email, title, message)
        # メールの送信元のアドレス
        from_email = "admin@example.com"
        # 送信先のメールアドレス
        to_list = ["admin@example.com"]
        # EmailMessageオブジェクトを生成
        message = EmailMessage(subject=subject,
                                body=message,
                                from_email=from_email,
                                to=to_list,
                                )
        # EmailMessageクラスのsend()でメールサーバーからメールを送信
        message.send()
        # 送信完了後に表示するメッセージ
        messages.success(
            self.request, "お問い合わせは正常に送信されました。")
        # 戻り値はスーパークラスのform_vaild()の戻り値(HttpResposeRedirect)
        return super().form_valid(form)


# デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreateBlogView(CreateView):
    '''写真投稿ページのビュー

    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する

    Attributes:
        form_class: モデルとフィールドが登録されたフォームクラス
        template_name: レンダリングするテンプレート
        success_url: データベースへの登録完了後のリダイレクト先
    '''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = BlogPostForm
    # レンダリングするテンプレート
    template_name = "post_blog.html"
    # フォームデータ登録完了後のリダイレクト
    success_url = reverse_lazy('blogapp:blogpost_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド

        フォームのバリエーションを通過したときに呼ばれる
        フォームデータの登録をここで行う

        parametes:
            form(django.forms.Form):
                form_classに格納されているPhotoPostFormオブジェクト
        Return:
            HttpResponseRedirectオブジェクト:
                スーパークラスのform_valid()の戻り値を返すことで、
                success_urlで設定されているURLにリダイレクトさせる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)

class BlogSuccessView(TemplateView):
    '''投稿完了ページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name = 'post_success2.html'

class UserView(ListView):
    '''ユーザーの投稿一覧ページのビュー
    Attributes:
        template_name: レンダリングするテンプレート
        pagination_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index2.html'
    # 1ページに表示するレコードの件数
    pagination_by = 9

    def get_queryset(self):
        '''クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、
        # userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs['user']
        # filter(フィールド名=id)で絞り込む
        user_list = BlogPost.objects.filter(
            user=user_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return user_list

class MypageView(ListView):
    '''マイページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
    '''
    # mypage.htmlをレンダリングする
    template_name ='mypage2.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        '''クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:
            クエリによって取得されたレコード
        '''
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている
        # filter(userフィールド=userオブジェクト)で絞り込む
        queryset = BlogPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return queryset

class BlogDeleteView(DeleteView):
    '''レコードの削除を行うレビュー

    Attributes:
        model: モデル
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
        success_url: 削除完了後のリダイレクト先のURL
    '''
    # 操作の対象はPhtoPostモデル
    model = BlogPost
    # photo_delete.htmlをレンダリングする
    template_name ='blog_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('blogapp:blogmypage')

    def delete(self, request, *args, **kwargs):
        '''レコードの削除を行う

        Parameters:
            self: PhotoDeleteViewオブジェクト
            request: WSGIRequest(HttpRequest)オブジェクト
            args: 引数として渡される辞書(dict)
            kwargs: キーワード付きの辞書(dict)
                    {'pk': 21}のようにレコードのidが渡される

        Returns:
            HttpResponseRedirect(success_url)を返して
            success_urlにリダイレクト
        '''
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)

class BlogUpdateView(UpdateView):
    '''レコードの削除を行うレビュー

    Attributes:
        model: モデル
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
        success_url: 削除完了後のリダイレクト先のURL
    '''
    form_class = BlogPostForm
    # 操作の対象はPhtoPostモデル
    model = BlogPost
    # photo_delete.htmlをレンダリングする
    template_name ='blogapp_update.html'
    def get_success_url(self):
    # 処理完了後にマイページにリダイレクト
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, '投稿を更新しました')
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)


class BlogCommentView(generic.CreateView):
    """コメント投稿ページのビュー"""
    template_name = 'comment_form.html'
    model = BlogComment
    form_class = BlogCommentCreateForm

    def form_valid(self, form):
        blogpost_pk = self.kwargs['pk']
        blogpost = get_object_or_404(BlogPost, pk=blogpost_pk)
        blogcomment = form.save(commit=False)
        blogcomment.target = blogpost
        blogcomment.save()
        return redirect('blogapp:blog_detail', pk=blogpost_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogpost'] = get_object_or_404(BlogPost, pk=self.kwargs['pk'])
        return context



# class BlogReplyCreate(generic.CreateView):
#     """コメント投稿ページのビュー"""
#     template_name = 'comment_form2.html'
#     model = BlogReply
#     form_class = BlogReplyCreateForm

#     def form_valid(self, form):
#         blogcomment_pk = self.kwargs['pk']
#         blogpost = get_object_or_404(BlogComment, pk=blogcomment_pk)
#         blogreply = form.save(commit=False)
#         blogreply.target = blogpost
#         blogreply.save()
#         return redirect('blogapp:blog_detail')


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         blogcomment_pk = self.kwargs['pk']
#         blogcomment = get_object_or_404(BlogComment, pk=blogcomment_pk)
#         context['blogpost'] = blogcomment.target
#         return context

# コメントの詳細表示
class BlogCommentDetailView(DetailView):

    template_name = 'blog_comment.html'
    model = BlogComment



class BlogCommentDeleteView(DeleteView):
    '''レコードの削除を行うレビュー
    '''
    # 操作の対象はPhtoPostモデル
    model = BlogComment
    # photo_delete.htmlをレンダリングする
    template_name ='blog_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('blogapp:t-blog')

    def delete(self, request, *args, **kwargs):
        '''レコードの削除を行う

        '''
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)