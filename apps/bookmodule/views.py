from django.shortcuts import render,redirect,get_object_or_404
from .models import Book
from django.db.models import Count, Sum, Avg, Max, Min, Value, OuterRef, Subquery,Q
from django.http import HttpResponse
from .models import Student, Address
from django.utils import timezone
from .models import Publisher, Author, Lab9Book
from django.db.models.functions import Coalesce
from .forms import BookForm
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


from datetime import timedelta

def add_lab9_data(request):
    Publisher.objects.all().delete()
    Author.objects.all().delete()
    Lab9Book.objects.all().delete()

    # ---------- PUBLISHERS ----------
    p1 = Publisher.objects.create(name="O'Reilly",    location="USA")
    p2 = Publisher.objects.create(name="Pearson",     location="UK")
    p3 = Publisher.objects.create(name="McGraw Hill", location="Canada")
    p4 = Publisher.objects.create(name="Springer",    location="Germany")
    p5 = Publisher.objects.create(name="Apollo Press", location="Egypt")   # no books → tests Coalesce / None

    # ---------- AUTHORS ----------
    a1 = Author.objects.create(name="Ali Ahmed")
    a2 = Author.objects.create(name="Sara Khalid")
    a3 = Author.objects.create(name="Fahad Saleh")
    a4 = Author.objects.create(name="Mona Hassan")

    now = timezone.now()

    # ---------- BOOKS ----------
    # p1 – O'Reilly (2 books, different dates)
    b1 = Lab9Book.objects.create(
        title="Python Basics", price=40, quantity=7, rating=4,
        pubdate=now - timedelta(days=400), publisher=p1
    )
    b2 = Lab9Book.objects.create(
        title="Database Systems", price=120, quantity=3, rating=5,
        pubdate=now - timedelta(days=200), publisher=p1
    )

    # p2 – Pearson (2 books)
    b3 = Lab9Book.objects.create(
        title="Computer Networks", price=80, quantity=10, rating=3,
        pubdate=now - timedelta(days=300), publisher=p2
    )
    b5 = Lab9Book.objects.create(
        title="Operating Systems", price=95, quantity=4, rating=4,
        pubdate=now - timedelta(days=100), publisher=p2
    )

    # p3 – McGraw Hill (2 books)
    b4 = Lab9Book.objects.create(
        title="Cyber Security", price=150, quantity=2, rating=5,
        pubdate=now - timedelta(days=50), publisher=p3
    )
    b6 = Lab9Book.objects.create(
        title="Data Structures", price=60, quantity=8, rating=4,
        pubdate=now - timedelta(days=350), publisher=p3
    )

    # p4 – Springer (2 books)
    b7 = Lab9Book.objects.create(
        title="Machine Learning", price=200, quantity=3, rating=5,
        pubdate=now - timedelta(days=150), publisher=p4
    )
    b8 = Lab9Book.objects.create(
        title="Compiler Design", price=70, quantity=1, rating=3,
        pubdate=now - timedelta(days=250), publisher=p4
    )

    # b9 – one book with rating 2 and price ≤ 50 for edge cases
    b9 = Lab9Book.objects.create(
        title="Intro to Programming", price=45, quantity=6, rating=2,
        pubdate=now - timedelta(days=500), publisher=p1
    )

    # p5 – Apollo Press has NO books → tests Coalesce & None branches

    # ---------- AUTHORS ↔ BOOKS ----------
    b1.authors.add(a1)
    b2.authors.add(a1, a2)
    b3.authors.add(a2)
    b4.authors.add(a3)
    b5.authors.add(a4)
    b6.authors.add(a3)
    b7.authors.add(a4)
    b8.authors.add(a1, a4)
    b9.authors.add(a2)

    return HttpResponse("Lab9 Data Added")

def lab9_task1(request):

    total_quantity = Lab9Book.objects.aggregate(
        total=Sum('quantity')
    )['total']

    books = Lab9Book.objects.all()

    for book in books:
        book.availability = round(
            (book.quantity / total_quantity) * 100,
            2
        )

    return render(
        request,
        'bookmodule/lab9_task1.html',
        {'books': books}
    )

def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_stock=Coalesce(Sum('lab9book__quantity'), Value(0))).order_by('name')

    return render(
        request,
        'bookmodule/lab9_task2.html',
        {'publishers': publishers}
    )

def lab9_task3(request):
    oldest_book = Lab9Book.objects.filter(
        publisher=OuterRef('pk')
    ).order_by('pubdate')

    publishers = Publisher.objects.annotate(
        oldest_title=Subquery(oldest_book.values('title')[:1]),
        oldest_date=Subquery(oldest_book.values('pubdate')[:1]),
        oldest_price=Subquery(oldest_book.values('price')[:1]),
        oldest_quantity=Subquery(oldest_book.values('quantity')[:1]),
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_task3.html',
        {'publishers': publishers}
    )

def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('lab9book__price'),
        min_price=Min('lab9book__price'),
        max_price=Max('lab9book__price'),
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_task4.html',
        {'publishers': publishers}
    )

def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        high_rated_count=Count(
            'lab9book',
            filter=Q(lab9book__rating__gte=4)
        ),
        high_rated_quantity=Coalesce(
            Sum(
                'lab9book__quantity',
                filter=Q(lab9book__rating__gte=4)
            ),
            Value(0)
        ),
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_task5.html',
        {'publishers': publishers}
    )

def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_count=Count(
            'lab9book',
            filter=Q(
                lab9book__price__gt=50,
                lab9book__quantity__lt=5,
                lab9book__quantity__gte=1,
            )
        ),
    ).order_by('name')

    return render(
        request,
        'bookmodule/lab9_task6.html',
        {'publishers': publishers}
    )


def list_books_lab10(request):

    books = Book.objects.all()

    return render(
        request,
        'bookmodule/listbooks_lab10.html',
        {'books': books}
    )

def add_book_lab10(request):

    if request.method == 'POST':

        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        edition = request.POST['edition']

        Book.objects.create(
            title=title,
            author=author,
            price=price,
            edition=edition
        )

        return redirect('books.lab10.list')

    return render(
        request,
        'bookmodule/addbook_lab10.html'
    )

def edit_book_lab10(request, id):

    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':

        book.title = request.POST['title']
        book.author = request.POST['author']
        book.price = request.POST['price']
        book.edition = request.POST['edition']

        book.save()

        return redirect('books.lab10.list')

    return render(
        request,
        'bookmodule/editbook_lab10.html',
        {'book': book}
    )

def delete_book_lab10(request, id):

    book = get_object_or_404(Book, id=id)

    book.delete()

    return redirect('books.lab10.list')

def add_book_form(request):

    if request.method == 'POST':

        form = BookForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('books.lab10.list')

    else:

        form = BookForm()

    return render(
        request,
        'bookmodule/addbook_form.html',
        {'form': form}
    )

def edit_book_form(request, id):

    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':

        form = BookForm(
            request.POST,
            instance=book
        )

        if form.is_valid():

            form.save()

            return redirect('books.lab10.list')

    else:

        form = BookForm(instance=book)

    return render(request,'bookmodule/editbook_form.html',{'form': form,'book': book} )

def delete_book_form(request, id):

    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':

        book.delete()

        return redirect('books.lab10.list')

    return render(
        request,
        'bookmodule/deletebook_form.html',
        {'book': book}
    )