from django.urls import path

from Fiszki import views

urlpatterns =[
    path('', views.view_home.home, name='home'),
    path('home', views.view_home.home, name='home'),

    path('flashcard/<str:SOFId>', views.view_home.flashcard, name='flashcard'),

    path('user-flashcards', views.view_user_flashcards.userFlashcards, name='user-flashcards'),
    path('user-flashcard/<str:SOUFId>', views.view_user_flashcards.userFlashcard, name='user-flashcard'),

    path('manage-flashcards', views.view_manage_flashcards.setsOfFlashcards, name='manage-flashcards'),
    path('manage-flashcard/<str:SOFId>', views.view_manage_flashcards.flashcardDetails, name='manage-flashcard'),
    path('manage-flashcard/<str:SOFId>/<str:cardId>', views.view_manage_flashcards.flashcardEdit, name='edit-flashcard'),

    path('user-manage-flashcards', views.view_user_manage_flashcards.setsOfUserFlashcards, name='user-manage-flashcards'),
    path('user-manage-flashcard/<str:SOUFId>', views.view_user_manage_flashcards.userFlashcardDetails, name='user-manage-flashcard'),
    path('user-manage-flashcard/<str:SOUFId>/<str:cardId>', views.view_user_manage_flashcards.userFlashcardEdit, name='user-edit-flashcard'),

    path('signup', views.view_registration.sign_up, name='signup'),

    path('tos', views.view_site_tos.TOS_page, name='tos'),
    # path('profile/<str:userid>', views.view_user.profile, name='profile'),
    # path('followers', views.view_follower.followers_page, name='followers'),
    # path('edit-profile', views.view_user.edit_profile, name='edit-profile'),
    # path('post/<str:post_id>', views.view_post.post_full, name='post'),
]