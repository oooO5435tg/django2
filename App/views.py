from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import TemplateView
from .forms import RegisterUserForm, RequestForm, CategoryForm, RequestStatusCompleted, RequestStatusAcceptWork
from .models import User, Request, Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def index(request):
    request_list = Request.objects.filter(status='Выполнено').order_by('-created_at')[:4]
    request_count = Request.objects.filter(status='Принято в работу').count()
    return render(request, 'main/index.html', {'request_list': request_list, 'request_count': request_count})


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class DesignLoginView(LoginView):
    template_name = 'main/login.html'


class DesignLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class RegisterUserView(CreateView):
    model = User
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('App:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/profile.html'


def my_requests(request):
    requests = Request.objects.filter(username=request.user)
    return render(request, 'main/profile_request_add.html', {'requests': requests})


@login_required
def profile(request):
    status = request.GET.get('status', '')
    current_user = request.user
    request_list = Request.objects.filter(user=current_user)
    context = {'status': status, 'request_list': request_list}
    return render(request, 'main/profile.html', context)


@login_required
def profile_request_add(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            Request = form.save(commit=False)
            # formset = RequestForm(request.POST, request.FILES, instance=Request)
            # if formset.is_valid():
            #     formset.save()
            #     messages.add_message(request, messages.SUCCESS, 'Заявка добавлена')
            Request.user = request.user
            Request.save()
            messages.add_message(request, messages.SUCCESS, 'Заявка добавлена')
            return redirect('App:profile')
    else:
        form = RequestForm(initial={'author': request.user.pk})
    #     formset = RequestForm()
    # context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_request_add.html', {'form': form})

class DeleteRequestView(LoginRequiredMixin, DeleteView):
   model = Request
   template_name = 'main/profile_request_delete.html'
   success_url = reverse_lazy('App:index')

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # Create User object
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                last_name=form.cleaned_data['last_name'],
                first_name=form.cleaned_data['first_name'],
                patronymic=form.cleaned_data['patronymic'],
            )
            messages.success(request, 'Registration successful.')
            return render(request, 'main/index.html')
    else:
        form = RegisterUserForm()
    return render(request, 'main/register_user.html', {'form': form})


def admin_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Категория добавлена')
            return redirect('App:category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/admin_add_category.html', {'form': form})

def category_list(request):
    category_list = Category.objects.all()
    return render(request, 'admin/category_list.html', {'category_list': category_list})

# def admin_category_delete(category_id):
#     category = get_object_or_404(Category, id=category_id)
#     category.delete()
#     return redirect('App;:ategory_list')

class AdminCategoryDelete(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'id'
    model = Category
    template_name = 'admin/admin_category_delete.html'
    success_url = reverse_lazy('App:category_list')

# def change_status(request):

def request_all(request):
    reque = Request.objects.all()
    return render(request, 'admin/request_all.html', {'reque': reque})


class ChangeStatusAcceptWork(View):
    def get(self, request, id):
        design_request = Request.objects.get(id=id)
        form = RequestStatusAcceptWork(instance=design_request)
        return render(request, 'admin/change_status_accept_work.html', {'form': form})

    def post(self, request, id):
        design_request = Request.objects.get(id=id)
        form = RequestStatusAcceptWork(request.POST, request.FILES, instance=design_request)
        if form.is_valid():
            design_request.status = 'Принято в работу'
            design_request.comment = form.cleaned_data['comment']
            form.save()
            return redirect('App:request_all')
        return render(request, 'admin/change_status_accept_work.html', {'form': form})

class ChangeStatusCompleted(View):
    def get(self, request, id):
        design_request = Request.objects.get(id=id)
        form = RequestStatusCompleted(instance=design_request)
        return render(request, 'admin/change_status_completed.html', {'form': form})

    def post(self, request, id):
        design_request = Request.objects.get(id=id)
        form = RequestStatusCompleted(request.POST, instance=design_request)
        if form.is_valid():
            design_request.status = 'Выполнено'
            design_request.design_image = form.cleaned_data['image_design']
            form.save()
            return redirect('App:request_all')
        return render(request, 'admin/change_status_completed.html', {'form': form})