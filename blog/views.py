# blog/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count, Q
from .models import Category, Thread, Comment, ThreadReaction, Slide
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ThreadForm
from django.views.generic.edit import FormMixin
from django.contrib.auth import logout



class CategoryThreadList(LoginRequiredMixin, FormMixin, ListView):
    model = Thread
    template_name = "category_feed.html"
    context_object_name = "page_obj"
    paginate_by = 10

    form_class = ThreadForm
    login_url = "login"
    redirect_field_name = "next"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return (
            self.category.threads
                .annotate(
                    likes_count   = Count("reactions", filter=Q(reactions__value=1)),
                    dislikes_count= Count("reactions", filter=Q(reactions__value=-1)),
                    comments_count= Count("comments"),
                )
                .order_by("-created_at")
        )

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        ctx["category"] = self.category
        ctx["form"]     = ctx.get("form") or self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author   = request.user
            thread.category = self.category
            # auto-generate a title from body if needed
            thread.title    = thread.body[:50] + ("…" if len(thread.body) > 50 else "")
            thread.save()
            return redirect("category_feed", slug=self.category.slug)
        return self.get(request, form=form)

class ThreadCreate(CreateView):
    model = Thread
    fields = ["title", "body"]
    template_name = "thread_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])
        return super().form_valid(form)


class ThreadDetail(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = "thread_detail.html"
    context_object_name = "thread"
    login_url = "login"

    def get_context_data(self, **ctx):
        ctx = super().get_context_data(**ctx)
        thread = self.object
        # calculate counts here
        ctx["likes_count"]    = thread.reactions.filter(value=1).count()
        ctx["dislikes_count"] = thread.reactions.filter(value=-1).count()
        ctx["comments_count"] = thread.comments.count()
        return ctx

@login_required
def comment_on_thread(request, pk):
    thr = get_object_or_404(Thread, pk=pk)
    Comment.objects.create(
        thread=thr, author=request.user, body=request.POST["body"]
    )
    return redirect("thread_detail", pk=thr.pk)

def react_to_thread(request, pk):
    thr = get_object_or_404(Thread, pk=pk)
    val = int(request.POST.get("value"))  # 1 or -1
    ThreadReaction.objects.update_or_create(
        thread=thr, user=request.user, defaults={"value": val}
    )
    return redirect("thread_detail", pk=thr.pk)


def home(request):
    slides = Slide.objects.all()[:5]

    categories = Category.objects.all()   

    return render(request, "home.html", {
        "slides": slides,
        "categories": categories,
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "account/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")