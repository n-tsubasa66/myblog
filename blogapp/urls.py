from django.urls import path
from . import views
from .views import BlogDetail, BlogCommentView

#URLconfのURLパターンを逆引きできるようにアプリ名を登録
app_name = "blogapp"

#URLパターンを登録するためのリスト
urlpatterns = [
    #http(s)://ホスト名/以下のパスが''(無し)の場合
    #viewsモジュールのIndexViewを実行
    #URLパターン名は'index
    path('t-blog',views.IndexView.as_view(),name='t-blog'),

    # リクエストされたURLが「blog-detail/レコードのid/」の場合
    # viewsモジュールのBlogDetailを実行
    # URLパターン名は'blog_detail'
    path(
        # 詳細ページのURLは「blog-detail/レコードのid/」
        'blog-detail/<int:pk>/',
        # viewsモジュールのBlogDetailを実行
        views.BlogDetail.as_view(),
        # URLパターンの名前を'blog_detail'にする
        name='blog_detail'
        ),

    # scienceカテゴリの一覧ページのURLパターン
    path(
        # scienceカテゴリの一覧ページのURLは「science-list/」
        "science-list/",
        # viwesモジュールのBlogDetailを実行
        views.ScienceView.as_view(),
        # URLパターンの名前を"science_list"にする
        name="science_list"
        ),

    # dailylifeカテゴリの一覧ページのURLパターン
    path(
        # dailylifeカテゴリの一覧ページのURLは「dailylife-list/」
        "dailylife-list/",
        # viwesモジュールのDailylifeViewを実行
        views.DailylifeView.as_view(),
        # URLパターンの名前を"dailylife_list"にする
        name="dailylife_list"
        ),

    # musicカテゴリの一覧ページのURLパターン
    path(
        # scienceカテゴリの一覧ページのURLは「music-list/」
        "music-list/",
        # viwesモジュールのMusicViewを実行
        views.MusicView.as_view(),
        # URLパターンの名前を"music_list"にする
        name="music_list"
        ),

    # 問い合わせページのURLパターン
    path(
        # 問い合わせページのURLは「contact/」
        "contact/",
        # viewsモジュールのContactViewを実行
        views.ContactView.as_view(),
        # URLパターンの名前を"contact"にする
        name="contact"
        ),
    # 写真投稿ページへのアクセスはviewsモジュールのIndexViewを実行
    path('t-blogpost/', views.CreateBlogView.as_view(), name='t-blogpost'),

    # 投稿完了ページのアクセスはviewsモジュールのPostSuccessViewを実行
    path('blogpost_done/',
        views.BlogSuccessView.as_view(),
        name='blogpost_done'),

    # ユーザーの投稿一覧ページ
    # photo/<ユーザーテーブルのid値>にマッチング
    # <int:user>は辞書{user: id値(int)}としてCategoryViewに渡される
    path('bloguser-list/<int:user>',
        views.UserView.as_view(),
        name = 'bloguser_list'
        ),

    # マイページ
    # mypage/へのアクセスはMypageViewを実行
    path('blogmypage/', views.MypageView.as_view(), name = 'blogmypage'),

    # 投稿写真の削除
    # photo/<Photo postsテーブルのid値>/delete/にマッチング
    # <int:pk>は辞書{pk: id値(int)}としてDetailViewに渡される
    path('blogapp/<int:pk>/delete/',
        views.BlogDeleteView.as_view(),
        name = 'blogapp_delete'
        ),

    # 投稿写真の編集
    # photo/<Photo postsテーブルのid値>/delete/にマッチング
    # <int:pk>は辞書{pk: id値(int)}としてDetailViewに渡される
    path('blogapp/<int:pk>/update/',
        views.BlogUpdateView.as_view(),
        name = 'blogapp_update'
        ),

    path('like_for_blogpost/', views.like_for_blogpost, name='like_for_blogpost'),  # 追加

    # コメント機能
    path('blogcomment/<int:pk>/create/', views.BlogCommentView.as_view(), name='blogcomment_create'),


    # コメントに返信機能
    # path('blogreply/<int:pk>/create/', views.BlogReplyCreate.as_view(), name='blogreply_create'),

    #コメントの詳細表示
    path('blogcomment_detil/<int:pk>',
        views.BlogCommentDetailView.as_view(),
        name = 'blogcomment_detail'
        ),


    path('blogcomment/<int:pk>/delete/',
        views.BlogCommentDeleteView.as_view(),
        name = 'blogcomment_delete'
        ),
]
