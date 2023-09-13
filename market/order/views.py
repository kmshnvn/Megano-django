from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from .forms import ProfileForm, DeliveryStep2Form, DeliveryStep3Form
from order.services.make_order import MakeOrder
from django.contrib.auth.mixins import LoginRequiredMixin


class MakeOrderStepOne(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг первый
    """

    def get(self, request: HttpRequest) -> HttpRequest:
        context = {
            "form_profile": ProfileForm,
        }
        return  render(request, "order/make-order-step1.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProfileForm(request.POST)
        if form.is_valid():
            make_order = MakeOrder(request=request)
            make_order.writing_data_order_in_session(key="step_1", cleaned_data=form.cleaned_data)
        return redirect(to="order:make_order_step_2")


class MakeOrderStepTwo(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг второй
    """
    def get(self, request: HttpRequest) -> HttpRequest:
        context = {
            "form_delivery": DeliveryStep2Form,
        }
        return  render(request, "order/make-order-step2.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DeliveryStep2Form(request.POST)
        if form.is_valid():
            make_order = MakeOrder(request=request)
            make_order.writing_data_order_in_session(key="step_2", cleaned_data=form.cleaned_data)
        return redirect(to="order:make_order_step_3")


class MakeOrderStepThree(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг третий
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form_delivery": DeliveryStep3Form,
        }
        return render(request, "order/make-order-step3.jinja2", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form= DeliveryStep3Form(request.POST)
        if form.is_valid():
            make_order = MakeOrder(request=request)
            make_order.writing_data_order_in_session(key="step_3", cleaned_data=form.cleaned_data)
        return redirect(to="order:make_order_step_4")


class MakeOrderStepFour(LoginRequiredMixin, View):
    """
    Класс создания заказа шаг четвертый - подтверждение и оплата заказа
    При неполноте данных, недостаточном балансе или отсутствия товара рендерит страницу-ошибку
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        order = MakeOrder(request=request)
        error = order.cheking_func()
        if not error:
            return redirect(to="basket:basket_view")
        return render(request, "order/page-error.jinja2", {"error": error})
