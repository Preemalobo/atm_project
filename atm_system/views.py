
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import logout
from .models import User
from .models import Transaction

def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(f"Trying to login with: {username} / {password}")  # Debug
            user = authenticate(request, username=username, password=password)
            print(f"Authenticated user: {user}")  # Debug

            if user is not None:  # ✅ this should only be True if auth succeeded
                login(request, user)
                # return redirect('dashboard')
                return redirect(request.GET.get('next') or 'dashboard')
            else:
                error = 'Invalid username or password.'

    return render(request, 'login.html', {"form": form, "error": error})


@login_required
def dashboard_view(request):
    user=request.user
    transactions=Transaction.objects.filter(user=user).order_by('-timestamp')[:5]
    return render(request,'dashboard.html',{'transactions': transactions,'user':request.user})

# @login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')

@login_required
def deposit_view(request):
    user=request.user
    if request.method=='POST':
        amount=float(request.POST['amount'])
        user.balance+=amount
        user.save()
        Transaction.objects.create(
            user=user,
            transaction_type='Deposit',
            amount=amount
        )
        return redirect('dashboard')
    return render(request,'deposit.html')

@login_required
def withdraw_view(request):
    """ Removing this since I have used authenticate and login which directly sets up the django session automatically"""
    # if 'user_id' not in request.session:
    #     return redirect('login')
    # user = User.objects.get(id=request.session['user_id'])
    user=request.user
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        if amount > user.balance:
            return render(request, 'withdraw.html', {'error': 'Insufficient funds'})
        user.balance -= amount
        user.save()
        Transaction.objects.create(
            user=user,
            transaction_type='Withdraw',
            amount=amount
        )
        return redirect('dashboard')
    return render(request, 'withdraw.html')

@login_required
def transfer_view(request):
    # if 'user_id' not in request.session:
    #     return redirect('login')
    # user = User.objects.get(id=request.session['user_id'])
    user=request.user
    if request.method == 'POST':
        recipient_username = request.POST['recipient']
        amount = float(request.POST['amount'])
        try:
            recipient = User.objects.get(username=recipient_username)
            if amount > user.balance:
                return render(request, 'transfer.html', {'error': 'Insufficient funds'})
            user.balance -= amount
            recipient.balance += amount
            user.save()
            recipient.save()
            Transaction.objects.create(
                user=user,
                transaction_type='Transfer',
                amount=amount
            )
            return redirect('dashboard')
        except User.DoesNotExist:
            return render(request, 'transfer.html', {'error': 'Recipient not found'})
    return render(request, 'transfer.html')


def transactions_view(request):
    transactions = Transaction.objects.all().order_by('-timestamp')  # Fetch all transactions, newest first
    return render(request, 'dashboard.html', {'transactions': transactions})

from django.utils import timezone
from django.shortcuts import HttpResponse
def test_transaction(request):
    user = User.objects.first()
    Transaction.objects.create(
        transaction_type="Credit",
        amount=1000,
        timestamp=timezone.now(),
        user=user
    )
    return HttpResponse("Transaction created!")