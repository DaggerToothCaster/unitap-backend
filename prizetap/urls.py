from django.urls import path
from prizetap.views import *

urlpatterns = [
    path(
        "raffle-list/",
        RaffleListView.as_view(),
        name="raffle-list",
    ),
    path(
        "raffle-enrollment/<int:pk>/",
        RaffleEnrollmentView.as_view(),
        name="raflle-enrollment",
    ),
    path(
        "raffle-enrollment/detail/<int:pk>/",
        GetRaffleEntryView.as_view(),
        name="raflle-enrollment-detail",
    ),
    path(
        "set-enrollment-tx/<int:pk>/",
        SetEnrollmentTxView.as_view(),
        name="set-enrollment-tx",
    ),
    path(
        "set-claiming-prize-tx/<int:pk>/",
        SetClaimingPrizeTxView.as_view(),
        name="set-claiming-prize-tx",
    ),
    path(
        "get-raffle-constraints/<int:raffle_pk>/",
        GetRaffleConstraintsView.as_view(),
        name="get-raffle-constraints",
    ),
    path(
        "create-raffle/",
        CreateRaffleView.as_view(),
        name="create-raffle",
    ),
    path(
        "get-valid-chains/",
        ValidChainsView.as_view(),
        name="get-valid-chains",
    ),
    path(
        "get-user-raffles/",
        UserRafflesListView.as_view(),
        name="get-user-raffles",
    ),
    path(
        "get-constraints/",
        ConstraintsListView.as_view(),
        name="get-constraints",
    ),
    path(
        "set-raffle-tx/<int:pk>/",
        SetRaffleTXView.as_view(),
        name="set-raffle-tx",
    ),
    path(
        "get-linea-entries/",
        LineaRaffleView.as_view(),
        name="get-linea-entries",
    )
]
