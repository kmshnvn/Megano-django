from django.urls import path
from .views import (
    MakeOrderStepOne,
    MakeOrderStepTwo,
    MakeOrderStepThree,
                    MakeOrderStepFour,
                    )


app_name = "order"

urlpatterns = [
    path("step_1/", MakeOrderStepOne.as_view(), name="make_order_step_1"),
    path("step_2/", MakeOrderStepTwo.as_view(), name="make_order_step_2"),
    path("step_3/", MakeOrderStepThree.as_view(), name="make_order_step_3"),
    path("step_4/", MakeOrderStepFour.as_view(), name="make_order_step_4"),
]