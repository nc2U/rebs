import math
from django.db.models import Q
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Board, Category, LawsuitCase, Post, File, Link
from project.models import Project
from .forms import LinkInlineFormSet, FileInlineFormSet, LawsuitPostForm, LawsuitCaseFrom


class CompanyGeneralDocsLV(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15

    def get_board(self):
        return Board.objects.first()

    def get_post_list(self):
        posts = self.model.objects.filter(board=self.get_board())
        return posts

    def get_context_data(self, **kwargs):
        context = super(CompanyGeneralDocsLV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '1'
        context['this_board'] = self.get_board()
        context['categories'] = Category.objects.filter(board=self.get_board()).order_by('order', 'id')
        context['notices'] = self.get_post_list().filter(is_notice=True, project=None)
        post_num = self.get_queryset().count()  # 총 게시물 수
        page = self.request.GET.get('page')  # 현재 페이지
        page_num = int(page) if page else 1  # 현재 페이지 수
        first_page_mod = post_num % self.paginate_by  # 첫 페이지 나머지
        total_page = math.ceil(post_num / self.paginate_by)  # 총 페이지 수
        add_num = (total_page - page_num) * self.paginate_by - (self.paginate_by - first_page_mod)
        context['add_num'] = add_num if add_num >= 0 else 0
        return context

    def get_queryset(self):
        project = self.request.GET.get('project')
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        order = self.request.GET.get('order')

        objects = self.get_post_list().filter(is_notice=False)
        if project:
            if project == 'co':
                objects = objects.filter(project=None)
            else:
                objects = objects.filter(project=project)
        if category:
            objects = objects.filter(category=category)
        if q:
            if not filter or filter == '1':  # 제목+내용
                objects = objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
            elif filter == '2':  # 제목
                objects = objects.filter(Q(title_icontains=q))
            elif filter == '3':  # 내용
                objects = objects.filter(Q(content__icontains=q))
            elif filter == '4':  # 작성자
                objects = objects.filter(user__username__icontains=q)
        if order:
            if order == '1':  # 작성일자
                objects = objects.order_by('-created')
            if order == '2':  # 시행일자
                objects = objects.order_by('-execution_date')
            if order == '3':  # 조회수
                objects = objects.order_by('-hit')
            if order == '4':  # 추천수
                objects = objects.order_by('-like')
        return objects


class CompanyGeneralDocsDV(LoginRequiredMixin, DetailView):
    model = Post

    def get_object(self):
        post = super().get_object()
        post.hit += 1
        post.save()
        return post

    def get_posts(self):
        return self.model.objects.filter(board=Board.objects.first())

    def get_prev(self):
        instance = self.get_posts().filter(id__lt=self.object.id).order_by('-id', ).first()
        return reverse_lazy('rebs:docs:co.general_detail', args=[instance.id]) if instance else None

    def get_next(self):
        instance = self.get_posts().filter(id__gt=self.object.id).order_by('id', ).first()
        return reverse_lazy('rebs:docs:co.general_detail', args=[instance.id]) if instance else None

    def get_context_data(self, **kwargs):
        context = super(CompanyGeneralDocsDV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        context['prev'] = self.get_prev() if self.get_prev() else ''
        context['next'] = self.get_next() if self.get_next() else ''
        return context


class CompanyGeneralDocsCV(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['is_notice', 'category', 'title', 'execution_date', 'content']
    success_message = "새 게시물이 등록되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:co.general_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(CompanyGeneralDocsCV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        context['link_formset'] = LinkInlineFormSet(queryset=Link.objects.none(), )
        context['file_formset'] = FileInlineFormSet(queryset=File.objects.none(), )
        return context

    def form_valid(self, form):
        form.instance.board = Board.objects.first()
        form.instance.user = self.request.user

        link_formset = LinkInlineFormSet(self.request.POST, )
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            self.object = form.save()

            if link_formset.is_valid():
                link_formset.instance = self.object
                link_formset.save()

            if file_formset.is_valid():
                file_formset.instance = self.object
                file_formset.save()

        return super(CompanyGeneralDocsCV, self).form_valid(form)


class CompanyGeneralDocsUV(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['is_notice', 'category', 'title', 'execution_date', 'content']
    success_message = "수정 사항이 적용되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:co.general_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(CompanyGeneralDocsUV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        context['link_formset'] = LinkInlineFormSet(
            instance=self.object,
            queryset=Link.objects.filter(post=self.object, ))
        context['file_formset'] = FileInlineFormSet(
            instance=self.object,
            queryset=File.objects.filter(post=self.object, ))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        link_formset = LinkInlineFormSet(self.request.POST, instance=self.object)
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)

        with transaction.atomic():
            if link_formset.is_valid():
                link_formset.save()

            if file_formset.is_valid():
                file_formset.save()

        return super(CompanyGeneralDocsUV, self).form_valid(form)


class CompanyGeneralDocsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('rebs:docs:co.general_list')

    def get_context_data(self, **kwargs):
        context = super(CompanyGeneralDocsDelete, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        return context


class CompanyLawsuitDocsLV(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15

    def get_board(self):
        return Board.objects.get(pk=2)

    def get_post_list(self):
        posts = self.model.objects.filter(board=self.get_board())
        return posts

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitDocsLV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        context['this_board'] = self.get_board()
        context['categories'] = Category.objects.filter(board=self.get_board()).order_by('order', 'id')
        context['notices'] = self.get_post_list().filter(is_notice=True, project=None)
        post_num = self.get_queryset().count()  # 총 게시물 수
        page = self.request.GET.get('page')  # 현재 페이지
        page_num = int(page) if page else 1  # 현재 페이지 수
        first_page_mod = self.get_queryset().count() % self.paginate_by  # 첫 페이지 나머지
        total_page = math.ceil(post_num / self.paginate_by)  # 총 페이지 수
        add_num = (total_page - page_num) * self.paginate_by - (self.paginate_by - first_page_mod)
        context['add_num'] = add_num if add_num >= 0 else 0
        return context

    def get_queryset(self):
        project = self.request.GET.get('project')
        category = self.request.GET.get('category')
        q = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        order = self.request.GET.get('order')

        objects = self.get_post_list().filter(is_notice=False)
        if project:
            if project == 'co':
                objects = objects.filter(project=None)
            else:
                objects = objects.filter(project=project)
        if category:
            objects = objects.filter(category=category)
        if q:
            if not filter or filter == '1':  # 제목+내용
                objects = objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
            elif filter == '2':  # 제목
                objects = objects.filter(Q(title_icontains=q))
            elif filter == '3':  # 내용
                objects = objects.filter(Q(content__icontains=q))
            elif filter == '4':  # 작성자
                objects = objects.filter(user__username__icontains=q)
        if order:
            if order == '1':  # 작성일자
                objects = objects.order_by('-created')
            if order == '2':  # 시행일자
                objects = objects.order_by('-execution_date')
            if order == '3':  # 조회수
                objects = objects.order_by('-hit')
            if order == '4':  # 추천수
                objects = objects.order_by('-like')
        return objects


class CompanyLawsuitDocsDV(LoginRequiredMixin, DetailView):
    model = Post

    def get_object(self):
        post = super().get_object()
        post.hit += 1
        post.save()
        return post

    def get_post_list(self):
        return self.model.objects.filter(board=Board.objects.get(id=2))

    def get_prev(self):
        instance = self.get_post_list().filter(id__lt=self.object.id).order_by('-id', ).first()
        return reverse_lazy('rebs:docs:co.lawsuit_detail', args=[instance.id]) if instance else None

    def get_next(self):
        instance = self.get_post_list().filter(id__gt=self.object.id).order_by('id', ).first()
        return reverse_lazy('rebs:docs:co.lawsuit_detail', args=[instance.id]) if instance else None

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitDocsDV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(pk=2)
        context['prev'] = self.get_prev() if self.get_prev() else ''
        context['next'] = self.get_next() if self.get_next() else ''
        return context


class CompanyLawsuitDocsCV(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = LawsuitPostForm
    success_message = "새 게시물이 등록되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:co.lawsuit_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(CompanyLawsuitDocsCV, self).get_form_kwargs()
        kwargs['project'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitDocsCV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(pk=2)
        context['link_formset'] = LinkInlineFormSet(queryset=Link.objects.none(), )
        context['file_formset'] = FileInlineFormSet(queryset=File.objects.none(), )
        return context

    def form_valid(self, form):
        form.instance.board = Board.objects.get(pk=2)
        form.instance.user = self.request.user

        link_formset = LinkInlineFormSet(self.request.POST, )
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            self.object = form.save()

            if link_formset.is_valid():
                link_formset.instance = self.object
                link_formset.save()

            if file_formset.is_valid():
                file_formset.instance = self.object
                file_formset.save()

        return super(CompanyLawsuitDocsCV, self).form_valid(form)


class CompanyLawsuitDocsUV(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = LawsuitPostForm
    success_message = "수정 사항이 적용되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:co.lawsuit_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(CompanyLawsuitDocsUV, self).get_form_kwargs()
        kwargs['project'] = None
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitDocsUV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(pk=2)
        context['link_formset'] = LinkInlineFormSet(
            instance=self.object,
            queryset=Link.objects.filter(post=self.object, ))
        context['file_formset'] = FileInlineFormSet(
            instance=self.object,
            queryset=File.objects.filter(post=self.object, ))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        link_formset = LinkInlineFormSet(self.request.POST, instance=self.object)
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)

        with transaction.atomic():
            if link_formset.is_valid():
                link_formset.save()

            if file_formset.is_valid():
                file_formset.save()

        return super(CompanyLawsuitDocsUV, self).form_valid(form)


class CompanyLawsuitDocsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('rebs:docs:co.lawsuit_list')

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitDocsDelete, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(pk=2)
        return context


class CompanyLawsuitCaseLV(LoginRequiredMixin, ListView):
    model = LawsuitCase
    paginate_by = 15

    def get_queryset(self):
        queryset = self.model.objects.all()
        related = self.request.GET.get('related')
        if related:
            queryset = queryset.filter(Q(pk=related) | Q(related_case=related))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitCaseLV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        context['lawcases'] = self.model.objects.all()
        return context


class CompanyLawsuitCaseCV(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LawsuitCase
    form_class = LawsuitCaseFrom
    success_message = '소송 사건 정보가 등록되었습니다.'
    success_url = reverse_lazy('rebs:docs:co.case_list')

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitCaseCV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        return context

    def form_valid(self, form):
        form.instance.register = self.request.user
        return super(CompanyLawsuitCaseCV, self).form_valid(form)


class CompanyLawsuitCaseUV(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LawsuitCase
    form_class = LawsuitCaseFrom
    success_message = '수정 사항이 적용되었습니다.'
    success_url = reverse_lazy('rebs:docs:co.case_list')

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitCaseUV, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        return context

    def form_valid(self, form):
        form.instance.register = self.request.user
        return super(CompanyLawsuitCaseUV, self).form_valid(form)


class CompanyLawsuitCaseDelete(LoginRequiredMixin, DeleteView):
    model = LawsuitCase
    success_url = reverse_lazy('rebs:docs:co.case_list')

    def get_context_data(self, **kwargs):
        context = super(CompanyLawsuitCaseDelete, self).get_context_data(**kwargs)
        context['co'] = True
        context['menu_order'] = '2'
        return context


class ProjectGeneralDocsLV(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15

    def get_project(self):
        try:
            project = self.request.user.staffauth.assigned_project
        except:
            project = Project.objects.first()
        gp = self.request.GET.get('project')
        project = Project.objects.get(pk=gp) if gp else project
        return project

    def get_board(self):
        return Board.objects.first()

    def get_post_list(self):
        return self.model.objects.filter(board=self.get_board(), project__isnull=False, project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super(ProjectGeneralDocsLV, self).get_context_data(**kwargs)
        context['menu_order'] = '1'
        user = self.request.user
        context['project_list'] = Project.objects.all() if user.is_superuser else user.staffauth.allowed_projects.all()
        context['this_project'] = self.get_project()
        context['this_board'] = self.get_board()
        context['categories'] = Category.objects.filter(board=self.get_board()).order_by('order', 'id')
        context['notices'] = self.get_post_list().filter(is_notice=True)
        post_num = self.get_queryset().count()  # 총 게시물 수
        page = self.request.GET.get('page')  # 현재 페이지
        page_num = int(page) if page else 1  # 현재 페이지 수
        first_page_mod = self.get_queryset().count() % self.paginate_by  # 첫 페이지 나머지
        total_page = math.ceil(post_num / self.paginate_by)  # 총 페이지 수
        add_num = (total_page - page_num) * self.paginate_by - (self.paginate_by - first_page_mod)
        context['add_num'] = add_num if add_num >= 0 else 0
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        order = self.request.GET.get('order')

        objects = self.get_post_list().filter(is_notice=False)
        if self.request.GET.get('category'):
            objects = objects.filter(category=self.request.GET.get('category'))
        if q:
            if not filter or filter == '1':  # 제목+내용
                objects = objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
            elif filter == '2':  # 제목
                objects = objects.filter(Q(title_icontains=q))
            elif filter == '3':  # 내용
                objects = objects.filter(Q(content__icontains=q))
            elif filter == '4':  # 작성자
                objects = objects.filter(user__username__icontains=q)
        if order:
            if order == '1':  # 작성일자
                objects = objects.order_by('-created')
            if order == '2':  # 시행일자
                objects = objects.order_by('-execution_date')
            if order == '3':  # 조회수
                objects = objects.order_by('-hit')
            if order == '4':  # 추천수
                objects = objects.order_by('-like')
        return objects


class ProjectGeneralDocsDV(LoginRequiredMixin, DetailView):
    model = Post

    def get_object(self):
        post = super().get_object()
        post.hit += 1
        post.save()
        return post

    def get_project(self):
        return Project.objects.get(pk=self.object.project.pk)

    def get_posts(self):
        return self.model.objects.filter(board=Board.objects.first(),
                                         project__isnull=False,
                                         project=self.get_project())

    def get_prev(self):
        instance = self.get_posts().filter(id__lt=self.object.id).order_by('-id', ).first()
        return reverse_lazy('rebs:docs:pr.general_detail', args=[instance.id]) if instance else None

    def get_next(self):
        instance = self.get_posts().filter(id__gt=self.object.id).order_by('id', ).first()
        return reverse_lazy('rebs:docs:pr.general_detail', args=[instance.id]) if instance else None

    def get_context_data(self, **kwargs):
        context = super(ProjectGeneralDocsDV, self).get_context_data(**kwargs)
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = self.get_project()
        context['prev'] = self.get_prev() if self.get_prev() else ''
        context['next'] = self.get_next() if self.get_next() else ''
        return context


class ProjectGeneralDocsCV(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['is_notice', 'category', 'title', 'execution_date', 'content']
    success_message = "새 게시물이 등록되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:pr.general_detail', args=(self.object.id,))

    def get_project(self):
        try:
            project = self.request.user.staffauth.assigned_project
        except:
            project = Project.objects.first()
        gp = self.request.GET.get('project')
        project = Project.objects.get(pk=gp) if gp else project
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectGeneralDocsCV, self).get_context_data(**kwargs)
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        user = self.request.user
        context['project_list'] = Project.objects.all() if user.is_superuser else user.staffauth.allowed_projects.all()
        context['this_project'] = self.get_project()
        context['link_formset'] = LinkInlineFormSet(queryset=Link.objects.none(), )
        context['file_formset'] = FileInlineFormSet(queryset=File.objects.none(), )
        return context

    def form_valid(self, form):
        form.instance.board = Board.objects.first()
        form.instance.project = self.get_project()
        form.instance.user = self.request.user

        link_formset = LinkInlineFormSet(self.request.POST, )
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            self.object = form.save()

            if link_formset.is_valid():
                link_formset.instance = self.object
                link_formset.save()

            if file_formset.is_valid():
                file_formset.instance = self.object
                file_formset.save()

        return super(ProjectGeneralDocsCV, self).form_valid(form)


class ProjectGeneralDocsUV(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['is_notice', 'category', 'title', 'execution_date', 'content']
    success_message = "수정 사항이 적용되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:pr.general_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(ProjectGeneralDocsUV, self).get_context_data(**kwargs)
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = Project.objects.get(pk=self.object.project.pk)
        context['link_formset'] = LinkInlineFormSet(
            instance=self.object,
            queryset=Link.objects.filter(post=self.object, ))
        context['file_formset'] = FileInlineFormSet(
            instance=self.object,
            queryset=File.objects.filter(post=self.object, ))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        link_formset = LinkInlineFormSet(self.request.POST, instance=self.object)
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)

        with transaction.atomic():
            if link_formset.is_valid():
                link_formset.save()

            if file_formset.is_valid():
                file_formset.save()

        return super(ProjectGeneralDocsUV, self).form_valid(form)


class ProjectGeneralDocsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('rebs:docs:pr.general_list')

    def get_context_data(self, **kwargs):
        context = super(ProjectGeneralDocsDelete, self).get_context_data(**kwargs)
        context['menu_order'] = '1'
        context['this_board'] = Board.objects.first()
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = Project.objects.get(pk=self.object.project.pk)
        return context


class ProjectLawsuitDocsLV(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 15

    def get_project(self):
        try:
            project = self.request.user.staffauth.assigned_project
        except:
            project = Project.objects.first()
        gp = self.request.GET.get('project')
        project = Project.objects.get(pk=gp) if gp else project
        return project

    def get_board(self):
        return Board.objects.get(pk=2)

    def get_post_list(self):
        return self.model.objects.filter(board=self.get_board(), project__isnull=False, project=self.get_project())

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitDocsLV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        user = self.request.user
        context['project_list'] = Project.objects.all() if user.is_superuser else user.staffauth.allowed_projects.all()
        context['this_project'] = self.get_project()
        context['this_board'] = self.get_board()
        context['categories'] = Category.objects.filter(board=self.get_board()).order_by('order', 'id')
        context['notices'] = self.get_post_list().filter(is_notice=True)
        post_num = self.get_queryset().count()  # 총 게시물 수
        page = self.request.GET.get('page')  # 현재 페이지
        page_num = int(page) if page else 1  # 현재 페이지 수
        first_page_mod = self.get_queryset().count() % self.paginate_by  # 첫 페이지 나머지
        total_page = math.ceil(post_num / self.paginate_by)  # 총 페이지 수
        add_num = (total_page - page_num) * self.paginate_by - (self.paginate_by - first_page_mod)
        context['add_num'] = add_num if add_num >= 0 else 0
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        order = self.request.GET.get('order')

        objects = self.get_post_list().filter(is_notice=False)
        if self.request.GET.get('category'):
            objects = objects.filter(category=self.request.GET.get('category'))
        if q:
            if not filter or filter == '1':  # 제목+내용
                objects = objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
            elif filter == '2':  # 제목
                objects = objects.filter(Q(title_icontains=q))
            elif filter == '3':  # 내용
                objects = objects.filter(Q(content__icontains=q))
            elif filter == '4':  # 작성자
                objects = objects.filter(user__username__icontains=q)
        if order:
            if order == '1':  # 작성일자
                objects = objects.order_by('-created')
            if order == '2':  # 시행일자
                objects = objects.order_by('-execution_date')
            if order == '3':  # 조회수
                objects = objects.order_by('-hit')
            if order == '4':  # 추천수
                objects = objects.order_by('-like')
        return objects


class ProjectLawsuitDocsDV(LoginRequiredMixin, DetailView):
    model = Post

    def get_object(self):
        post = super().get_object()
        post.hit += 1
        post.save()
        return post

    def get_project(self):
        return Project.objects.get(pk=self.object.project.pk)

    def get_posts(self):
        return self.model.objects.filter(board=Board.objects.get(id=2),
                                         project__isnull=False,
                                         project=self.get_project())

    def get_prev(self):
        instance = self.get_posts().filter(id__lt=self.object.id).order_by('-id', ).first()
        return reverse_lazy('rebs:docs:pr.lawsuit_detail', args=[instance.id]) if instance else None

    def get_next(self):
        instance = self.get_posts().filter(id__gt=self.object.id).order_by('id', ).first()
        return reverse_lazy('rebs:docs:pr.lawsuit_detail', args=[instance.id]) if instance else None

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitDocsDV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(id=2)
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = self.get_project()
        context['prev'] = self.get_prev() if self.get_prev() else ''
        context['next'] = self.get_next() if self.get_next() else ''
        return context


class ProjectLawsuitDocsCV(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = LawsuitPostForm
    success_message = "새 게시물이 등록되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:pr.lawsuit_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(ProjectLawsuitDocsCV, self).get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs

    def get_project(self):
        try:
            project = self.request.user.staffauth.assigned_project
        except:
            project = Project.objects.first()
        gp = self.request.GET.get('project')
        project = Project.objects.get(pk=gp) if gp else project
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitDocsCV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(id=2)
        user = self.request.user
        context['project_list'] = Project.objects.all() if user.is_superuser else user.staffauth.allowed_projects.all()
        context['this_project'] = self.get_project()
        context['link_formset'] = LinkInlineFormSet(queryset=Link.objects.none(), )
        context['file_formset'] = FileInlineFormSet(queryset=File.objects.none(), )
        return context

    def form_valid(self, form):
        form.instance.board = Board.objects.get(id=2)
        form.instance.project = self.get_project()
        form.instance.user = self.request.user

        link_formset = LinkInlineFormSet(self.request.POST, )
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES)

        with transaction.atomic():
            self.object = form.save()

            if link_formset.is_valid():
                link_formset.instance = self.object
                link_formset.save()

            if file_formset.is_valid():
                file_formset.instance = self.object
                file_formset.save()

        return super(ProjectLawsuitDocsCV, self).form_valid(form)


class ProjectLawsuitDocsUV(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = LawsuitPostForm
    success_message = "수정 사항이 적용되었습니다."

    def get_success_url(self):
        return reverse_lazy('rebs:docs:pr.lawsuit_detail', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super(ProjectLawsuitDocsUV, self).get_form_kwargs()
        kwargs['project'] = Project.objects.get(pk=self.object.project.pk)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitDocsUV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(id=2)
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = Project.objects.get(pk=self.object.project.pk)
        context['link_formset'] = LinkInlineFormSet(
            instance=self.object,
            queryset=Link.objects.filter(post=self.object, ))
        context['file_formset'] = FileInlineFormSet(
            instance=self.object,
            queryset=File.objects.filter(post=self.object, ))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        link_formset = LinkInlineFormSet(self.request.POST, instance=self.object)
        file_formset = FileInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)

        with transaction.atomic():
            if link_formset.is_valid():
                link_formset.save()

            if file_formset.is_valid():
                file_formset.save()

        return super(ProjectLawsuitDocsUV, self).form_valid(form)


class ProjectLawsuitDocsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('rebs:docs:pr.lawsuit_list')

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitDocsDelete, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        context['this_board'] = Board.objects.get(id=2)
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = Project.objects.get(pk=self.object.project.pk)
        return context


class ProjectLawsuitCaseLV(LoginRequiredMixin, ListView):
    model = LawsuitCase
    paginate_by = 15

    def get_project(self):
        try:
            project = self.request.user.staffauth.assigned_project
        except:
            project = Project.objects.first()
        gp = self.request.GET.get('project')
        project = Project.objects.get(pk=gp) if gp else project
        return project

    def get_queryset(self):
        queryset = self.model.objects.filter(project=self.get_project())
        related = self.request.GET.get('related')
        if related:
            queryset = queryset.filter(Q(pk=related) | Q(related_case=related))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitCaseLV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        user = self.request.user
        context['project_list'] = Project.objects.all() if user.is_superuser else user.staffauth.allowed_projects.all()
        context['this_project'] = self.get_project()
        context['lawcases'] = self.model.objects.filter(project=self.get_project())
        return context


class ProjectLawsuitCaseCV(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LawsuitCase
    form_class = LawsuitCaseFrom
    success_message = '소송 사건 정보가 등록되었습니다.'

    def get_success_url(self):
        project_str = '?project=' + str(self.get_project().pk) if self.request.GET.get('project') else ''
        return reverse_lazy('rebs:docs:pr.case_list') + project_str

    def get_project(self):
        try:
            project = self.request.user.staffauth.assigned_project
        except:
            project = Project.objects.first()
        gp = self.request.GET.get('project')
        project = Project.objects.get(pk=gp) if gp else project
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitCaseCV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        user = self.request.user
        context['project_list'] = Project.objects.all() if user.is_superuser else user.staffauth.allowed_projects.all()
        context['this_project'] = self.get_project()
        return context

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.register = self.request.user
        return super(ProjectLawsuitCaseCV, self).form_valid(form)


class ProjectLawsuitCaseUV(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LawsuitCase
    success_message = '수정 사항이 적용되었습니다.'
    form_class = LawsuitCaseFrom

    def get_success_url(self):
        project_str = '' if self.get_project().pk == 1 else '?project=' + str(self.get_project().pk)
        return reverse_lazy('rebs:docs:pr.case_list') + project_str

    def get_project(self):
        project = Project.objects.get(pk=self.object.project.pk)
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitCaseUV, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = self.get_project()
        return context

    def form_valid(self, form):
        form.instance.project = self.get_project()
        form.instance.register = self.request.user
        return super(ProjectLawsuitCaseUV, self).form_valid(form)


class ProjectLawsuitCaseDelete(LoginRequiredMixin, DeleteView):
    model = LawsuitCase

    def get_success_url(self):
        project_str = '' if self.get_project().pk == 1 else '?project=' + str(self.get_project().pk)
        return reverse_lazy('rebs:docs:pr.case_list') + project_str

    def get_project(self):
        project = Project.objects.get(pk=self.object.project.pk)
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectLawsuitCaseDelete, self).get_context_data(**kwargs)
        context['menu_order'] = '2'
        context['project_list'] = Project.objects.filter(pk=self.object.project.pk)
        context['this_project'] = self.get_project()
        return context


def link_hit(self, pk):
    link = get_object_or_404(Link, pk=pk)
    link.hit += 1
    link.save()
    return redirect(str(link))


def file_download(self, pk):
    file = get_object_or_404(File, pk=pk)
    file.hit += 1
    file.save()
    return redirect(str(file) + str(file.file.name))
