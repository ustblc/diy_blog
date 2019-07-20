from django.shortcuts import render
from django.views import generic
from .models import Blog, BlogAuthor, BlogComment
# Create your views here.
def index(request):
    return render(
        request,
        'index.html',
    )
class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 1

class BloggerListView(generic.ListView):
    model = BlogAuthor
    paginate_by = 2

class BlogDetailView(generic.DetailView):
    model = Blog

from django.shortcuts import get_object_or_404
class BlogListbyAuthorView(generic.ListView):
    model = Blog
    paginate_by = 1
    template_name = 'diy_blog/blog_list_by_author.html'
    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(BlogAuthor, pk=id)
        return Blog.objects.filter(author=target_author)
    def get_context_data(self, **kwargs):
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(BlogAuthor, pk=self.kwargs['pk'])
        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = BlogComment
    fields = ['description', ]

    def get_context_data(self, **kwargs):
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })