from django.shortcuts import redirect, render
from django.urls import path

from myapp.views import (
    actionPage,
    addProduct,
    editProfile,
    prompt_api,
    prompt_eval,
    test_case_api,
    userLogin,
    userProfile,
    userRegist,
)

from .views import aboutUs, contact, home, showContact

urlpatterns = [
    path("", home, name="home-page"),
    path("about/", aboutUs, name="about-page"),
    path("contact/", contact, name="contact-page"),
    # path("login/", views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path("showcontact/", showContact, name="showcontact-page"),
    path("register/", userRegist, name="register-page"),
    path("profile", userProfile, name="profile-page"),
    path("editprofile/", editProfile, name="editprofile-page"),
    path("action/<int:cid>", actionPage, name="action-page"),
    path("addproduct/", addProduct, name="addproduct-page"),
    path("prompt-eval/", prompt_eval, name="prompt-eval-page"),
    path("prompt-eval/api/prompts/", prompt_api, name="prompt-api"),
    path(
        "prompt-eval/api/prompts/<int:prompt_id>/test-cases/",
        test_case_api,
        name="test-case-api",
    ),
]
