from django.shortcuts import render
from budget_app.models import FamilyMember, Category, MoneyTransfer
from django.views import View
from datetime import date, timedelta


def main_page(request):
    member_id = request.session.get('family_member_id')
    if not member_id:
        return render(request, 'login.html')
    today = str(date.today())  # raczej do usunięcia wraz z poniższym
    categories = Category.objects.all()
    return render(request, 'index.html', {'today': today, 'categories': categories})


# sprawdzenie czy id użytkownika jest w sesji, jeżeli brak zwróci True
def check_log(request):
    member_id = request.session.get('family_member_id')
    if not member_id:
        return True
    else:
        return False


def login_view(request):
    members = FamilyMember.objects.all()
    if request.method == 'GET':
        return render(request, 'login.html', {'members': members})
    else:
        family_member = request.POST['family_member']
        new_family_member = request.POST['new_family_member']
        names = FamilyMember.objects.filter(name=family_member)
        if family_member == 'new':
            if len(new_family_member) < 3:
                return render(request, 'login.html', {'members': members, 'error': 'imię musi mieć więcej niż 2 znaki'})
            elif len(names) > 0:  # tego warunku nie jestem pewny
                return render(request, 'login.html', {'members': members, 'error': 'takie imię istnieje już w bazie'})
            else:
                new_member = FamilyMember.objects.create(name=new_family_member)
                request.session['family_member_id'] = new_member.id
                return render(request, 'index.html')
        else:
            today = str(date.today())
            categories = Category.objects.all()
            request.session['family_member_id'] = FamilyMember.objects.get(name=family_member).id
            return render(request, 'index.html', {'today': today, 'categories': categories})


class Transfer(View):
    def post(self, request):
        member_id = request.session.get('family_member_id')
        if not member_id:
            return render(request, 'login.html')
        # today = str(date.today())
        # categories = Category.objects.all()
        description = request.POST['description']
        amount = int(request.POST['amount'])
        dates = request.POST['date']
        if dates == '':
            dates = date.today()
        if request.POST['category'] != "None":
            category_name = request.POST['category']
            category_id = Category.objects.get(name=category_name).id
            category = Category.objects.get(id=category_id)
        else:
            category = None
        member = FamilyMember.objects.get(id=member_id)
        mt = MoneyTransfer.objects.create(date=dates,
                                          owner=member,
                                          amount=-amount,  # wartość ujemna bo wydatki
                                          description=description,
                                          category=category
                                          )
        return main_page(request)  # chyba trzeba zmienić na render '/'


class Incoming(View):
    def post(self, request):
        member_id = request.session.get('family_member_id')
        if not member_id:
            return render(request, 'login.html')
        member = FamilyMember.objects.get(id=member_id)
        dates = request.POST['date']
        if dates == '':
            dates = date.today()
        amount = int(request.POST['amount'])
        description = 'Wpływ do budżetu'
        category = None
        mt = MoneyTransfer.objects.create(date=dates,
                                          owner=member,
                                          amount=amount,
                                          description=description,
                                          category=category
                                          )
        return main_page(request)


class Raport(View):
    def get(self, request):
        member_id = request.session.get('family_member_id')
        if not member_id:
            return render(request, 'login.html')
        members = FamilyMember.objects.all()
        categories = Category.objects.all()
        first_day = date.today().replace(day=1)  # first day of current month
        last_day = date.today().replace(month=+1, day=1) - timedelta(1)  # last day of current month
        return render(request, 'raport.html', {'members': members, 'categories': categories,
                                              'first_day': str(first_day), 'last_day': str(last_day)
                                              })
    def post(self, request):
        transactions = MoneyTransfer.objects.all()
        q = request.POST['q']
        start = request.POST['start']
        end = request.POST['end']
        category = request.POST.getlist('category')
        member = request.POST.getlist('family_member')
        minValue = request.POST['min']
        maxValue = request.POST['max']
        print(category)
        if q:
            transactions = transactions.filter(description__icontains=q)
        if start:
            transactions = transactions.filter(date__gte=start)
        if end:
            transactions = transactions.filter(date__lte=end)
        if category:
            transactions = transactions.filter(category__in=category)
        if member:
            transactions = transactions.filter(owner__in=member)
        if minValue and minValue != '0':
            transactions = transactions.filter(amount__gte=minValue)
        if maxValue and maxValue != '0':
            transactions = transactions.filter(amount__lte=maxValue)
        total = 0
        for i in transactions:
            total += i.amount
        return render(request, 'raport-post.html', {'transactions': transactions, 'total': total})
