from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    context = {}
    records = Record.objects.all()
    context['records'] = records

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Logged In")
                return redirect('home')
            else:
                messages.error(request, "Error logging in. Please try again.")
        else:
            messages.error(request, "Username and password are required.")

        return redirect('home') 
    else:
        if request.user.is_authenticated:
            context['first_name'] = request.user.first_name
        return render(request, "home.html", context)



def logout_user(request):
    logout(request)
    messages.success(request,"You have been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect('home')  # Redirect to a 'home' page or any other page after successful registration
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
     if request.user.is_authenticated:
         #Look up record
         customer_record = Record.objects.get(id=pk)
         return render(request, 'record.html', {'customer_record': customer_record})
     else:
        messages.success(request, "You Must Be Logged In To View That Page")
        return redirect('home')


def delete_record(request, pk):
        if request.user.is_authenticated:
            delete_it = Record.objects.get(id=pk)
            delete_it.delete()
            messages.success(request, "Record Deleted Successfully")
            return redirect('home')
        else:
            messages.success(request, "You Must Be Logged In To Delete That Record")
            return redirect('home')

def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully")
                return redirect("home")    
        else:
            return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect("home") 

def search_record(request):
    if request.user.is_authenticated:
        query = request.GET.get('q')
        if query:
            try:
                # Attempt to find a record matching the query in first_name or last_name
                records = Record.objects.filter(
                    first_name__icontains=query
                ).first() or Record.objects.filter(
                    last_name__icontains=query
                ).first()
                if customer_record:
                    return redirect('record', pk=records.id)
                else:
                    messages.error(request, "No matching records found.")
            except Record.DoesNotExist:
                messages.error(request, "No matching records found.")
        else:
            messages.error(request, "Please enter a search term.")
        return redirect('home')
    else:
        messages.error(request, "You must be logged in to perform a search.")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Updated Successfully")
                return redirect("home")
        else:
            return render(request, 'update.html', {'form':form})
        
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect("home") 