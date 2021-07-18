from http import HTTPStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from backend.foodgram.settings import PAGE_SIZE_CART, PAGE_SIZE_INDEX
from backend.recipes.models import (
    Cart, Recipe, RecipeIngredient, Tag, User
)

from .forms import RecipeForm
from .utils import form_ingredients_tags, recipe_ingredient_bulk_create


class RecipeListView(ListView):
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = PAGE_SIZE_INDEX
    page_title = None

    def get_queryset(self):
        tags_check = self.request.GET.get('tags')
        if tags_check is None:
            return self.queryset
        tags_check = tags_check.split(',')
        tags_check = Tag.objects.filter(slug__in=tags_check).distinct()
        recipes = self.queryset.filter(tags__in=tags_check).distinct()
        return recipes

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title()})
        tags = Tag.objects.all()
        kwargs.update({'tags_all': tags})
        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        return self.page_title


class IndexListView(RecipeListView):
    page_title = 'Рецепты'
    template_name = 'recipes/index.html'


class FavoriteListView(LoginRequiredMixin, RecipeListView):
    page_title = 'Избранное'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(following__user=self.request.user)
        return qs


class ProfileView(RecipeListView):
    context_object_name = 'profile_list'
    template_name = 'recipes/authorRecipe.html'

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs.get('username'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = Recipe.objects.filter(author=self.user)
        tags = self.request.GET.get('tags')
        if tags is None:
            return qs
        tags = tags.split(',')
        tags = Tag.objects.filter(slug__in=tags).distinct()
        qs = qs.filter(tags__in=tags).distinct()
        return qs

    def _get_page_title(self):
        return self.user.get_full_name() or self.user.username

    def get_context_data(self, **kwargs):
        kwargs.update({
            'page_title': self._get_page_title(),
            'author': self.user})
        context = super().get_context_data(**kwargs)
        return context


class RecipeDetailView(DetailView):
    queryset = Recipe.objects.all()
    template_name = 'recipes/singlePage.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .prefetch_related('recipe_ingredients__ingredient')
        )
        return qs


# class SubscriptionListView(LoginRequiredMixin, RecipeListView):
#     context_object_name = 'subscription_list'
#     template_name = 'recipes/myFollow.html'
#     page_title = 'Мои подписки'
#     queryset = Subscription.objects.all()
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.filter(user=self.request.user)
#         return qs


class CartListView(LoginRequiredMixin, RecipeListView):
    context_object_name = 'cart_list'
    template_name = 'recipes/shopList.html'
    page_title = 'Список покупок'
    paginate_by = PAGE_SIZE_CART
    queryset = Cart.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user)
        return qs


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    page_title = 'Создание рецепта'
    form_class = RecipeForm
    template_name = 'recipes/formRecipe.html'

    def form_valid(self, form):
        form_ingredients, form_tags = form_ingredients_tags(self.request.POST)
        if not form_tags or not form_ingredients:
            return super().form_invalid(form)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        form.save()
        self.object.tags.add(*form_tags)
        recipe_ingredient_bulk_create(form_ingredients, self.object)
        form.save_m2m()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        tags = Tag.objects.all()
        kwargs.update({'tags_all': tags})
        context = super().get_context_data(**kwargs)
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('index')


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    page_title = 'Создание рецепта'
    form_class = RecipeForm
    template_name = 'recipes/formChangeRecipe.html'

    def get_context_data(self, **kwargs):
        tags = Tag.objects.all()
        kwargs.update({'tags_all': tags})
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super().get_initial()
        tags = list(Tag.objects.filter(recipes=self.object))
        initial['tags'] = tags
        initial['recipe_ingredients'] = RecipeIngredient.objects.filter(
            recipe=self.object
        )
        initial['slug'] = self.object.slug
        return initial

    def form_valid(self, form):
        form_ingredients, form_tags = form_ingredients_tags(self.request.POST)
        self.object = form.save(commit=False)
        self.object.tags.set([])
        recipeingredients = RecipeIngredient.objects.filter(recipe=self.object)
        if recipeingredients:
            recipeingredients.delete()
        form.save()
        self.object.tags.add(*form_tags)
        recipe_ingredient_bulk_create(form_ingredients, self.object)
        return super().form_valid(form)


def shoping_list_view(request):
    carts = Cart.objects.filter(customer=request.user)

    recipes = Recipe.objects.filter(in_cart__in=carts)
    recipes_ingredients = RecipeIngredient.objects.filter(
        recipe__in=recipes
    )
    ingredients = (
        recipes_ingredients.values('ingredient__title').annotate(
            total_amount=Sum('amount')
        ).values_list(
            'ingredient__title',
            'total_amount',
            'ingredient__dimension')
    )
    out = []
    for item in ingredients:
        title, amount, dimension = item
        amount = str(float(amount))
        out.append(f'{title} {amount} {dimension}\n')
    out = ''.join(sorted(out))
    filename = 'my_shoping_list.txt'
    response = HttpResponse(out, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND
    )


def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


def about(request):
    return render(request, 'misc/about.html', status=HTTPStatus.OK)


def tech(request):
    return render(request, 'misc/tech.html', status=HTTPStatus.OK)
