from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM buyer WHERE username = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer ORDER BY first_name")
        buyers = cursor.fetchall()
        # list of tuples

    result_dict = {'records': buyers}

    return render(request,'app/index.html',result_dict)



def buyerindex(request):
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM buyer WHERE username = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer ORDER BY first_name")
        buyers = cursor.fetchall()
        # list of tuples

    result_dict = {'records': buyers}

    return render(request,'app/buyerindex.html',result_dict)

def login(request):
	return render(request,'AppHONUSupper/login.html')

@login_required
def loginhome(request):
	return render(request,'AppHONUSupper/loginhome.html')

def login(request):
	return render(request,'AppHONUSupper/login.html')

def register(request):
	form = CreateUserForm()
	
	if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account created for {username}! Please log in.')
				return redirect('userdb')
	
	else:
			form = CreateUserForm()
	
	return render(request,'AppHONUSupper/register.html', {'form': form})
	
def userdb(request):
	form = CreateUsersForm()
	
	if request.method == 'POST':
			form = CreateUsersForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account created for {username}! Please log in.')
				return redirect('login')
	
	else:
			form = CreateUsersForm()
	
	return render(request,'AppHONUSupper/register.html', {'form': form})

@login_required
def ride(request):
	search_string = request.GET.get('origin', '')
	search_string2 = request.GET.get('destination', '')
	results = Ride.objects.filter(origin__regex=r'%s' %(search_string), destination__regex=r'%s' %(search_string2))
	results = [(r.ride_id,r.origin,r.destination,r.start_time) for r in results]
	result_dict = {'records': results}
	return render(request,'AppHONUSupper/ride.html',result_dict)

def bid(request):
	form = Bid()
	
	if request.method == 'POST':
			form = Bid(request.POST)
			if form.is_valid():
#				form = form.save(commit=False)
#				form.bid_id = random.randint(10000, 99999)
#				form.username = request.user
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Bid created for {username}!')
				return redirect('loginhome')
	
	else:
			form = Bid()
			
	return render(request,'AppHONUSupper/bid.html', {'form': form})			
			
@login_required
def driver(request):
	search_string = request.GET.get('rideid','')
	users = 'SELECT * FROM bid WHERE ride_id ~ \'%s\'' % (search_string)
	c = connection.cursor()
	c.execute(users)
	results = c.fetchall()
	result_dict = {'records': results}
	return render(request,'AppHONUSupper/driver.html',result_dict)
                      
@login_required
def profile(request):
	return render(request,'AppHONUSupper/profile.html')
	
@login_required
def advertise(request):
	form = Advertise()
	
	if request.method == 'POST':
			form = Advertise(request.POST)
			if form.is_valid():
#				form = form.save(commit=False)
#				form.ride_id = random.randint(10000000, 99999999)
#				form.driver = request.user
				form.save()
				username = form.cleaned_data.get('username')
				messages.success(request, f'Ride created for {username}!')
				return redirect('loginhome')
	
	else:
			form = Advertise()
	
	return render(request,'AppHONUSupper/advertise.html', {'form': form})

@login_required
def acceptance(request):
	search_string = request.GET.get('name','')
	users = 'SELECT * FROM bid,ride WHERE bid_id ~ \'%s\' AND bid.ride_id = ride.ride_id' % (search_string)
	c = connection.cursor()
	c.execute(users)
	results = c.fetchall()
	result_dict = {'records': results}
	return render(request,'AppHONUSupper/acceptance.html',result_dict)
	
#@login_required
#def acceptance(request):
#	return render(request,'AppHONUSupper/acceptance.html')

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
        buyer = cursor.fetchone()
    result_dict = {'buyer': buyer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM buyer WHERE username = %s", [request.POST['username']])
            buyer = cursor.fetchone()
            ## No customer with same id
            if buyer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO buyer VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['username'], request.POST['password'], request.POST['first_name'],
                           request.POST['last_name'] , request.POST['phone_number'], request.POST['hall'], request.POST['wallet_balance'] ])
                return redirect('index')    
            else:
                status = 'Buyer with Username %s already exists' % (request.POST['username'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE buyer SET password = %s, first_name = %s, last_name = %s, phone_number = %s, hall = %s, wallet_balance = %s WHERE username = %s"
                    , [request.POST['password'], request.POST['first_name'], request.POST['last_name'],
                        request.POST['phone_number'] , request.POST['hall'], request.POST['wallet_balance'], id ])
            status = 'Buyer edited successfully!'
            cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)
