from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, TemplateView, FormView

from store.forms import FilterForm, RegisterForm, LoginForm
from store.models import Product, Category, Tag
from order.models import Cart

from django.contrib.auth import get_user_model

User = get_user_model()


class IndexView(TemplateView):
    template_name = 'index.html'


@cache_page(60 * 3)
class CategoryView(View):
    def get(self, request, slug=None):
        tag = request.GET.get('tag')
        price = request.GET.get('rangeInput')
        if price is None or int(price) == 0:
            price = 999999999

        context = {'child_categories': [], 'paginator': None, 'tags': [], 'category': ""}
        products = []

        if slug is None:
            cats = Category.objects.prefetch_related('parent')
            products = Product.objects.prefetch_related('tags').filter(price__lte=price).all()

            result = []

            if tag is not None:
                for prod in products:
                    tags = prod.tags.all()
                    for t in tags:
                        if t.title == tag:
                            result.append(prod)

                products = result

            children = cats.filter(parent_category_id=None).all()
            context['child_categories'] = children

        else:
            cats = Category.objects.prefetch_related('products', 'parent')
            parent_cat = cats.get(title=slug)
            context['category'] = parent_cat.title

            cat_id = parent_cat.id
            children = cats.filter(parent_category_id=cat_id)
            context['child_categories'] = children
            cats_queue = [slug]

            for prod in parent_cat.products.filter(price__lte=price).all():
                products.append(prod)

            while len(cats_queue) > 0:
                cat = cats_queue.pop(0)
                cat_id = cats.filter(title=cat).first().id
                children = cats.filter(parent_category_id=cat_id)

                for child in children:
                    prods = child.products.filter(price__lte=price).all()
                    for prod in prods:
                        if prod not in products:
                            products.append(prod)

                    cats_queue.append(child.title)

        tags = Tag.objects.all()
        tag_choices = [(tag.title, tag.title) for tag in tags]
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context['paginator'] = page_obj

        cart, created = Cart.objects.prefetch_related('items').get_or_create(id=1)
        context['items_in_cart'] = len(list(cart.items.all())) if not created else 0

        filter_form = FilterForm()
        filter_form.fields['tag'].choices = tag_choices
        context['filter_form'] = filter_form

        return render(request, 'category.html', context)


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactView(TemplateView):
    template_name = 'contact.html'


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # Creates the new user and saves it to the database
        messages.success(self.request, 'Registration successful.')
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'  # Template for the login page
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Logged in successfully.')
            # Check for 'next' parameter to redirect
            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)  # Redirect to the next URL if provided
            return super().form_valid(form)  # Fallback to default success URL
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)


class Logout(LogoutView):
    next_page = reverse_lazy('index')  # Redirect after logout
