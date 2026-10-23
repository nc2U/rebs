from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ImageFormSet
from .models import Book, Subject, Image


class BooksListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(author__icontains=q) |
                Q(translator__icontains=q) |
                Q(description__icontains=q)
            ).distinct()

        return queryset


class BooksDetailView(LoginRequiredMixin, DetailView):
    model = Book


class BooksCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Book
    fields = ('title', 'disclosure', 'author', 'translator', 'publisher', 'pub_date', 'description')
    success_message = "새 게시물이 등록되었습니다."

    def get_success_url(self):
        return reverse_lazy('book:detail', args=[self.object.id])

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class BooksUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Book
    fields = ('title', 'disclosure', 'author', 'translator', 'publisher', 'pub_date', 'description')
    success_message = "수정하신 내용이 저장되었습니다."

    def get_success_url(self):
        return reverse_lazy('book:detail', args=[self.object.id])


class BooksDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book:index')


class Breadcrumb:
    def get_breadcrumb(self):
        breadcrumb = []
        book_id = self.kwargs.get('book')
        pk = self.kwargs.get('pk')

        sub = None
        if pk:
            try:
                sub = Subject.objects.get(book_id=book_id, id=pk)
            except (Subject.DoesNotExist, KeyError):
                pass
        if not sub:
            sub = Subject.objects.filter(book_id=book_id).order_by('seq').first()

        if sub:
            for i in range(1, int(sub.level) + 1):
                bread_subs = Subject.objects.filter(book_id=book_id, level=i, seq__lte=sub.seq)
                bread_sub = bread_subs.order_by('-seq').first() if sub.level != i else sub
                if not bread_sub:
                    continue
                url = bread_sub.get_absolute_url()
                label = bread_sub.title
                is_current = (sub.level == i)
                cls1 = 'active' if is_current else ''
                cls2 = 'aria-current=page' if is_current else ''

                breadcrumb.append({'url': url, 'label': label, 'cls1': cls1, 'cls2': cls2})
        return breadcrumb


class SearchResult:
    def get_search_list(self):
        q = self.request.GET.get('q')

        if q:
            return Subject.objects.filter(
                Q(book_id=self.kwargs['book']) &
                (Q(title__icontains=q) | Q(content__icontains=q))
            ).distinct()
        return Subject.objects.none()


class SubjectsIndexView(LoginRequiredMixin, TemplateView, Breadcrumb, SearchResult):
    template_name = 'book/subjects/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, id=self.kwargs['book'])
        subjects = Subject.objects.filter(book=book)
        context['book'] = book
        context['subjects'] = subjects
        context['total'] = subjects.count()
        context['object'] = subjects.first()
        context['breadcrumb'] = self.get_breadcrumb()
        context['search_list'] = self.get_search_list()
        return context


class SubjectsDetailView(LoginRequiredMixin, DetailView, Breadcrumb, SearchResult):
    model = Subject
    template_name = 'book/subjects/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, id=self.kwargs['book'])
        subjects = Subject.objects.filter(book=book)
        context['book'] = book
        context['subjects'] = subjects
        context['total'] = subjects.count()
        context['breadcrumb'] = self.get_breadcrumb()
        context['search_list'] = self.get_search_list()
        return context


class SubjectsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Subject
    fields = ('title', 'level', 'content')
    success_message = "새 게시물이 등록되었습니다."
    template_name = 'book/subjects/subject_form.html'

    def get_success_url(self):
        return reverse('book:subject_detail', args=(self.kwargs['book'], self.object.id))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, id=self.kwargs['book'])
        subjects = Subject.objects.filter(book=book)
        context['book'] = book
        context['last_level'] = subjects.last().level if subjects.exists() else 0
        if self.request.POST:
            context['formset'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = ImageFormSet(queryset=Image.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        book = get_object_or_404(Book, id=self.kwargs['book'])

        if not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            form.instance.creator = self.request.user
            form.instance.book = book
            max_seq = Subject.objects.filter(book=book).aggregate(Max('seq'))['seq__max'] or 0
            form.instance.seq = max_seq + 1
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()

        return response


class SubjectsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Subject
    fields = ('title', 'level', 'content')
    success_message = "수정하신 내용이 저장되었습니다."
    template_name = 'book/subjects/subject_form.html'

    def get_success_url(self):
        return reverse('book:subject_detail', args=(self.kwargs['book'], self.kwargs['pk']))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, id=self.kwargs['book'])
        subjects = Subject.objects.filter(book=book)
        context['book'] = book
        context['last_level'] = subjects.last().level if subjects.exists() else 0
        if self.request.POST:
            context['formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ImageFormSet(instance=self.object, queryset=Image.objects.filter(subject=self.object))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()

        return response


class SubjectsDeleteView(LoginRequiredMixin, DeleteView, Breadcrumb, SearchResult):
    model = Subject
    template_name = 'book/subjects/index.html'

    def get_success_url(self):
        return reverse('book:subject_index', args=[self.kwargs['book']])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(Book, id=self.kwargs['book'])
        subjects = Subject.objects.filter(book=book)
        context['book'] = book
        context['subjects'] = subjects
        context['total'] = subjects.count()
        context['breadcrumb'] = self.get_breadcrumb()
        context['search_list'] = self.get_search_list()
        return context
