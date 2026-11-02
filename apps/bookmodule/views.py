from django.shortcuts import render
from .models import Book
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min
from django.http import HttpResponse
from .models import Student, Address

# -------------------------
# Lab3 (saved for future use)
# -------------------------

# def index(request):
#     name = request.GET.get("name") or "world!"
#     return render(request, "bookmodule/index.html", {"name": name})

# def index2(request, val1=0):
#     return HttpResponse("value1 = " + str(val1))

# def viewbook(request, bookId):
#     book1 = {'id': 123, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
#     book2 = {'id': 456, 'title': 'Secrets of Reverse Engineering', 'author': 'E. Eilam'}
#     targetBook = None
#     if book1['id'] == bookId:
#         targetBook = book1
#     if book2['id'] == bookId:
#         targetBook = book2
#     context = {'book': targetBook}
#     return render(request, 'bookmodule/show.html', context)

# -------------------------
# Lab4 (active code)
# -------------------------

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, "bookmodule/list_books.html")

def viewbook(request, bookId):
    return render(request, "bookmodule/one_book.html")

def aboutus(request):
    return render(request, "bookmodule/aboutus.html")

def html_links(request):
    return render(request, 'bookmodule/html_links.html')

def text_formatting(request):
    return render(request, 'bookmodule/text_formatting.html')

def lists(request):
    return render(request, 'bookmodule/lists.html')

def tables(request):
    return render(request, 'bookmodule/tables.html')

def _getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J. Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = _getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')

from django.http import HttpResponse

def add_books(request):
    Book.objects.all().delete()

    books_data = [
    {
        "title": "Continuous and Delivery",
        "author": "J. Humble and D. Farley",
        "price": 90.00,   # price too low for complex
        "edition": 1      # edition too low for complex
    },
    {
        "title": "Data and Algorithms",
        "author": "Tom Anderson",
        "price": 150.00,
        "edition": 2
    },
    {
        "title": "Security and Cryptography",
        "author": "Bruce Schneier",
        "price": 70.00,
        "edition": 5
    },
    {
        "title": "Machine Learning and Deep Learning",
        "author": "A. Karim",
        "price": 80.00,
        "edition": 4
    },
    {
        "title": "Systems Networks",
        "author": "Mark Russinovich",
        "price": 130.00,
        "edition": 3
    },
    {
        "title": "Python Basics",
        "author": "Ali Ahmed",
        "price": 70.00,
        "edition": 1
    },
    {
        "title": "Computer Networks",
        "author": "Mark Russinovich",
        "price": 130.00,
        "edition": 5
    }
        
]

    for b in books_data:
        Book.objects.create(
            title=b["title"],
            author=b["author"],
            price=b["price"],
            edition=b["edition"]
        )

    return HttpResponse("Books added successfully!")


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False)\
                          .filter(title__icontains='and')\
                          .filter(edition__gte=2)\
                          .exclude(price__lte=100)[:10]

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))

    return render(
        request,
        'bookmodule/bookList.html',
        {
            'books': books,
            'title': 'Lab 8 - Task 1 (Price ≤ 80)'
        }
    )


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) &
        (Q(title__icontains='co') | Q(author__icontains='co'))
    )

    return render(
        request,
        'bookmodule/bookList.html',
        {
            'books': books,
            'title': 'Lab 8 - Task 2 (Edition > 3 and contains "co")'
        }
    )


def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) &
        ~(Q(title__icontains='co') | Q(author__icontains='co'))
    )

    return render(
        request,
        'bookmodule/bookList.html',
        {
            'books': books,
            'title': 'Lab 8 - Task 3 (Edition ≤ 3 and does NOT contain "co")'
        }
    )

def lab8_task4(request):

    books = Book.objects.order_by('title')

    return render(
        request,
        'bookmodule/bookList.html',
        {
            'books': books,
            'title': 'Lab 8 - Task 4 (Books Ordered By Title)'
        }
    )

def lab8_task5(request):

    stats = Book.objects.aggregate(
        total_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )

    return render(
        request,
        'bookmodule/task5.html',
        {'stats': stats}
    )


def add_students(request):

    Student.objects.all().delete()
    Address.objects.all().delete()

    riyadh = Address.objects.create(city="Riyadh")
    qassim = Address.objects.create(city="Qassim")
    jeddah = Address.objects.create(city="Jeddah")

    Student.objects.create(
        name="Ali",
        age=21,
        address=riyadh
    )

    Student.objects.create(
        name="Sara",
        age=22,
        address=qassim
    )

    Student.objects.create(
        name="Fahad",
        age=20,
        address=qassim
    )

    Student.objects.create(
        name="Noor",
        age=23,
        address=jeddah
    )

    return HttpResponse("Students added successfully!")


def lab8_task7(request):

    cities = Address.objects.annotate(
        student_count=Count('student')
    )

    return render(
        request,
        'bookmodule/task7.html',
        {'cities': cities}
    )