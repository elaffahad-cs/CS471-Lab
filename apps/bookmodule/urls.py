from django.urls import path
from . import views

urlpatterns = [

    # -------------------------
    # Lab3 (saved for future use)
    # -------------------------

    # path('', views.index),
    # path('index2/<int:val1>/', views.index2),
    # path('<int:bookId>', views.viewbook),

    # -------------------------
    # Lab4 (active code)
    # -------------------------

    path('', views.index, name="books.index"),
    path('list_books/', views.list_books, name="books.list_books"),
    path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
    path('aboutus/', views.aboutus, name="books.aboutus"),
    path('html5/links/', views.html_links, name='books.html_links'),
    path('html5/text/formatting/', views.text_formatting, name='books.text_formatting'),
    path('html5/lists/', views.lists, name='books.lists'),
    path('html5/tables/', views.tables, name='books.tables'),
]
