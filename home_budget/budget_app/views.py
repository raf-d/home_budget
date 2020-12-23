from django.shortcuts import render
from budget_app.models import FamilyMember, Category, MoneyTransfer
from django.views import View


def main_page(request):
    member_id = request.session.get('family_member_id')
    if not member_id:
        return render(request, 'login.html')
    return render(request, 'index.html')


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
            request.session['family_member_id'] = FamilyMember.objects.get(name=family_member).id
            return render(request, 'index.html')


class Transfer(View):
    def post(self, request):
        member_id = request.session.get('family_member_id')
        if not member_id:
            return render(request, 'login.html')
        description = request.POST['description']
        amount = request.POST['amount']
        date = request.POST['date']
        category_id = request.POST['category']
        member = FamilyMember.objects.get(id=member_id)
        category = Category.objects.get(id=category_id)
        mt = MoneyTransfer.objects.create(date=date,
                                          owner=member,
                                          amount=-amount,  # wartość ujemna bo wydatki
                                          description=description,
                                          category=category
                                          )
        return main_page(request)

