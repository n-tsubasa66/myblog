from django.db import models
# accountsアプリのmodelsモジュールからCustomUserをインポート
from accounts.models import CustomUser

from django.utils import timezone

class Category(models.Model):
    '''投稿する写真のカテゴリを管理するモデル
    '''
    # カテゴリ名のフィールド
    title = models.CharField(
        verbose_name='カテゴリ',    # フィールドのタイトル
        max_length=20)

    def __str__(self):
        '''オブジェクトを文字列に変換して返す

        Returns(str):カテゴリ名
        '''
        return self.title

class BlogPost(models.Model):
    '''モデルクラス'''
    # カテゴリに設定する項目を入れ子のタプルとして定義
    # タプルの第1要素はモデルが使用する値,
    #第2要素は管理サイトの選択メニューに表示する文字列
    CATEGORY = (("science", "科学のこと"),
                ("dailylife", "日常のこと"),
                ("music", "音楽のこと"))
    user = models.ForeignKey(
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
        )

    # category2 = models.ForeignKey(
    #     Category,
    #     # フィールドのタイトル
    #     verbose_name='カテゴリ',
    #     # カテゴリに関連付けられた投稿データが存在する場合は
    #     # そのカテゴリを削除できないようにする
    #     on_delete=models.PROTECT
    #     )



    # タイトル用のフィールド
    title = models.CharField(
        verbose_name="タイトル",    #フィールドのタイトル
        max_length=200              #最大文字数は200
        )
    # 本文用のフィールド
    content = models.TextField(
        verbose_name="本文"         #フィールドのタイトル
        )
    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name="投稿日時",    #フィールドのタイトル
        auto_now_add=True               #日時を自動追加
        )
    # カテゴリのフィールド
    category = models.CharField(
        verbose_name="カテゴリ",    #フィールドのタイトル
        max_length=50,              #最大文字は50
        choices=CATEGORY            #categoryフィールドにはCATEGORyの要素のみを登録
        )

    def __str__(self):
        '''Django管理サイトでデータの表示する際に識別名として
            投稿記事のタイトル（titleフィールドの値）を表示するために必要

        Returns(str):投稿記事のタイトル
        '''


        return self.title


class LikeForBlogPost(models.Model):
    """投稿に対するいいね"""

    target = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(default=timezone.now,)

class BlogComment(models.Model):
    """コメント"""
    writer = models.CharField('名前', default='名無し', max_length=32)
    text = models.TextField('本文')
    target = models.ForeignKey(BlogPost, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]


# 返信用
class BlogReply(models.Model):
    """コメント"""
    writer = models.CharField('名前', default='名無し', max_length=32)
    text = models.TextField('本文')
    target = models.ForeignKey(BlogPost, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]