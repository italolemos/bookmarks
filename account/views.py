# Create your views here.
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from actions.models import Action
from actions.utils import create_action
from common.decorators import ajax_required
from .forms import BookForm, BookFormset
from .forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm, BookModelForm, TurmaForm
from .models import Contact
from .models import Profile, Book


class CreateTurma(CreateView):
    form_class = TurmaForm
    template_name = 'account/create_turma.html'


def create_book_normal(request):
    template_name = 'account/create_normal.html'
    heading_message = 'Formset Demo'

    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        print(formset.errors)
        if formset.is_valid():
            for form in formset:
                # extract name from each form and save
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    Book(name=name).save()
            # once all books are saved, redirect to book list view
            return redirect('book_list')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })


def create_book(request):
    books = Book.objects.all()
    response_data = {}
    print(request.POST)
    if request.POST.get('action') == 'post':
        title = request.POST.get('title')
        description = request.POST.get('description')

        response_data['title'] = title
        response_data['description'] = description

        Book.objects.create(
            title=title,
            description=description,
        )
        print(response_data)
        return JsonResponse(response_data)

    return render(request, 'account/index.html', {'books': books})


def book_list(request):
    books = Book.objects.all()

    return render(request, 'account/book_list.html', {'books': books})


def save_book_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()
            data['form_is_valid'] = True

            books = Book.objects.all()
            data['html_book_list'] = render_to_string(
                'account/includes/partial_book_list.html', {
                    'books': books
                })
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name,
                                         context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()

    return save_book_form(request, form,
                          'account/includes/partial_book_create.html')


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)

    return save_book_form(request, form,
                          'account/includes/partial_book_update.html')


def books(request):
    data = dict()
    if request.method == 'GET':
        books = Book.objects.all()
        print(books)
        data['table'] = render_to_string('_book_table.html', {'books': books},
                                         request=request)

        return JsonResponse(data)


class BookCreateView(BSModalCreateView):
    template_name = 'account/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('dashboard')


class BookUpdateView(BSModalUpdateView):
    model = Book
    template_name = 'account/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was updated.'
    success_url = reverse_lazy('index')


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)

    return render(request, 'account/user/list.html', {'section': 'people',
                                                      'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    return render(request, 'account/user/detail.html', {'section': 'people',
                                                        'user': user})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfuly')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user obj but avoid savind it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the user obj
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.value_list('id', flat=True)

    if following_ids:
        # If user is following other, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related(
        'user', 'user__profile').prefetch_related('target')[:10]

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disable Account')
            else:
                return HttpResponse('Login Inválido')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
