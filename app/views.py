from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'app/index.html')

def login(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT password FROM buyer WHERE username = %s", [request.POST['username']])
            password = cursor.fetchone()
            if password == [request.POST['password']]:
                messages.success(request, f'Welcome user %s back to HONUSupper!' % (request.POST['username']))
                return redirect('loginhome')    
            else:
                status = 'Unable to login. Either username or password is incorrect.'


    context['status'] = status
 
    return render(request, "app/login.html", context)

def loginhome(request):
	return render(request,'app/loginhome.html')

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
                messages.success(request, f'Account created for %s! Please log in.' % (request.POST['username']))
                return redirect('login')    
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

def sellerindex(request):             
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orderid ORDER BY shopname")
        sellers = cursor.fetchall()

    result_dict = {'records': sellers}

    return render(request,"app/sellerindex.html",result_dict)

def addgrouporder(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orderid WHERE creator = %s AND hall = %s AND shopname = %s AND order_date = %s AND order_by = %s", [request.POST['creator'], request.POST['hall'], request.POST['shopname'],request.POST['order_date'], request.POST['order_by']])
            orderid = cursor.fetchone()
## No orderid with same details
            if orderid == None:
                cursor.execute("SELECT * FROM shop WHERE shopname = %s", [request.POST['shopname']])
                shopdet = cursor.fetchone()
                opening = shopdet[3]
                closing = shopdet[4]
                cursor.execute("SELECT * FROM shop WHERE shopname = %s", [request.POST['shopname']])
                messages.success(request, f'New Group Order created for %s! Please remember to close and send your group order.' % (request.POST['creator']))
                return redirect('index')
            else:
                status = '%s Group Order created by Username %s already exists' % (request.POST['shopname'], request.POST['creator'])


    context['status'] = status
    return render(request, "app/addgrouporder.html", context)
