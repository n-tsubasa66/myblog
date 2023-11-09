from django.contrib import admin
from django.urls import path, include # include追加
# auth.viewsをインポートしてauth_viewという名前で利用する
# from django.contrib.auth import views as auth_views

# settingsを追加
from django.conf import settings
# staticを追加
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # photo.urlsへのURlパターン
    path('', include('photo.urls')),

    # accounts.urlsへのパターン
    path('', include('accounts.urls')),

    #http(s)://ホスト名/へのアクセスはblogappの
    # URLconf(urls.py)を呼び出す
    path('',include('blogapp.urls')),

    # パスワードリセットのためのURLパターン
    # PasswordResetConfirmViewがプロジェクトのurls.pyを参照するのでここに記載
    # パスワードリセット申し込みページ
    # path('password_reset/',
    #     auth_views.PasswordResetView.as_view(
    #         template_name = "password_reset.html"),
    #     name ='password_reset'),

    # # メール送信完了ページ
    # path('password_reset/done/',
    #     auth_views.PasswordResetDoneView.as_view(
    #         template_name = "password_reset_sent.html"),
    #     name ='password_reset_done'),

    # # パスワードリセットページ
    # path('reset/<uidb64>/<token>',
    #     auth_views.PasswordResetConfirmView.as_view(
    #         template_name = "password_reset_form.html"),
    #     name ='password_reset_confirm'),

    # # パスワードリセット完了ページ
    # path('reset/done/',
    #     auth_views.PasswordResetCompleteView.as_view(
    #         template_name = "password_reset_done.html"),
    #     name ='password_reset_complate'),
]

# urlpatternsにmediaフォルダーのURLパターンを追加
urlpatterns += static(
    # MEDIA_URL = 'media/'
    settings.MEDIA_URL,
    # MEDIA_ROOTにリダイレクト
    document_root=settings.MEDIA_ROOT
)