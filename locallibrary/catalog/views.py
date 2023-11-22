import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import RenewBookForm
from .models import Book, BookInstance, Author


@login_required
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        context['page_title'] = 'Books'
        return context


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    context = {
        'book': book,
    }

    return render(request, 'catalog/book_detail.html', context=context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'bookinstance_list'
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 1

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AllBorrowedBooksListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    def test_func(self):
        return self.request.user.is_staff

    model = BookInstance
    context_object_name = 'allborrow_list'
    template_name = 'catalog/allborrow_list.html'
    paginate_by = 1

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)

        context['page_title'] = 'Authors'
        return context


def author_detail():
    pass


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death'
    ]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
