from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic  # To create the class-based generic list view
from django.db.models import Q
from services import services


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


#  This is a "class based generic **list** view"
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'generic_book_list'   # Overwritting the list name
    queryset = Book.objects.all()
    # The following is, when we want to see book, applying some filters:
    # queryset = Book.objects.filter(title__icontains='Colombia')[:5]  # Get 5 books containing the word "Colombia" in the title
    template_name = 'books/generic_view_books_template.html'  # Overwritting the template file name

    # Option to add some context data in the "class based generic list view function":
    # def get_context_data(self, **kwargs):
    #         # Call the base implementation first to get the context
    #         context = super(BookListView, self).get_context_data(**kwargs)
    #         # Create any data and add it to the context
    #         context['some_data'] = 'This is just some data'
    #         return context
    paginate_by = 8


#  This is a "class based generic **detail** view"
class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'generic_detailed_book'
    template_name = 'book_detail/generic_view_book_detail_template.html'


class AuthorsListView(generic.ListView):
    model = Author
    context_object_name = 'authors_list'
    template_name = 'authors/authors_template.html'

    # Option to overwrite the list object returned in the queryset:
    def get_queryset(self):
        return Author.objects.all()

    paginate_by = 5


# Remember, this class pass as a context variable only one author value
class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'detailed_author'
    template_name = 'author_detail/author_detail_template.html'


# Just change the "class" by the "def" and the "generic.DetailView" by the "request"
# to pass from a generic view to a function view

def BookSearch(request):
    book_default_list = Book.objects.all()
    search_box_field = request.GET.get('search_box')
    check_boxes_active = request.GET.getlist('check_boxes')
    summaries_list = []
    books_by_summary_list = []
    redundance = "redundancy" in check_boxes_active

    if search_box_field is not None and search_box_field != "":
        title_and_author_query = Q(pk__icontains="None")
        summary_query = Q(pk__icontains="None")
        if "author" in check_boxes_active:
            title_and_author_query.add(Q(author__first_name__icontains=search_box_field), Q.OR)
            title_and_author_query.add(Q(author__last_name__icontains=search_box_field), Q.OR)
        if "title" in check_boxes_active:
            title_and_author_query.add(Q(title__icontains=search_box_field), Q.OR)
        if "word" in check_boxes_active:
            summary_query.add(Q(summary__icontains=search_box_field), Q.OR)

        summary_query = book_default_list.filter(summary_query)
        book_default_list = book_default_list.filter(title_and_author_query)

        for book in summary_query.all():
            if redundance and (book in book_default_list.all()):
                continue
            books_by_summary_list.append(book)
            original_string = book.summary
            summary_string_lower = original_string.lower()
            original_string_words_list = original_string.split()
            lower_case_words_summary_list = summary_string_lower.split()

            for word in lower_case_words_summary_list:
                if search_box_field in word:
                    the_string = "..."
                    lower_index = lower_case_words_summary_list.index(word) - 8
                    upper_index = lower_case_words_summary_list.index(word) + 8
                    summary_first_word_index = lower_index if lower_index > 0 else 0
                    summary_last_word_index = upper_index if upper_index < len(lower_case_words_summary_list) else len(lower_case_words_summary_list)

                    for i in range(summary_first_word_index, summary_last_word_index, 1):
                        the_string = "{} {}".format(the_string, original_string_words_list[i])
                    the_string = "{}{}".format(the_string, "...")
                    summaries_list.append(the_string)

    summary_search = dict(zip(books_by_summary_list, summaries_list))

    context = {
        'title_and_author_books': book_default_list,
        'summary_search_result': summary_search,
        'the_search': search_box_field,
        'check_boxes': check_boxes_active,
    }

    return render(request, 'search/book_search.html', context=context)


def GoogleSearch(request):
    search_box_field = request.GET.get('google_search_box')
    books_list = services.get_books(search_box_field)
    context = {
        'results': books_list,
    }
    return render(request, 'google/google_search.html', context=context)
