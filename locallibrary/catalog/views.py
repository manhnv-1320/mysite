from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Book, BookInstance, Author


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


class BookListView(generic.ListView):
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
