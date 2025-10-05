from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost

class PostListView(ListView):
    model = BlogPost
    template_name = "blogs/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by("-created_at")

class PostDetailView(DetailView):
    model = BlogPost
    template_name = "blogs/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        BlogPost.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        obj.refresh_from_db(fields=["views"])
        return obj

class PostCreateView(CreateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blogs/post_form.html"

class PostUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blogs/post_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blogs/post_confirm_delete.html"
    success_url = reverse_lazy("blogs:list")
