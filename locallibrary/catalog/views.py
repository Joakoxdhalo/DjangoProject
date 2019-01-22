from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic  # To create the class-based generic list view


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    special_month_features = Book.objects.filter(author__last_name__exact='García Márquez').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'special_month_features': special_month_features,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'generic_book_list'   # Overwritting the list name
    queryset = Book.objects.filter(genre__icontains='fiction')[:5]  # Get 5 books containing the genre "fiction"
    template_name = 'books/generic_view_template.html'  # Overwritting the template file name

    # Option to overwrite the list object returned in the queryset:

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]

    # Option to add some context data in the "class based generic list view function":

    # def get_context_data(self, **kwargs):
    #         # Call the base implementation first to get the context
    #         context = super(BookListView, self).get_context_data(**kwargs)
    #         # Create any data and add it to the context
    #         context['some_data'] = 'This is just some data'
    #         return context
