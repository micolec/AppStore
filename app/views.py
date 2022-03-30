from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages, auth
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'app/index.html')

def login(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor: 
            username = [request.POST['username']]
            cursor.execute("SELECT password FROM buyer WHERE username = %s", [request.POST['username']])
            password = cursor.fetchone()[0]
            if password == request.POST['password']:
                messages.success(request, f'Welcome buyer %s back to HONUSupper!' % (request.POST['username']))
                buyer = authenticate(username=username, password=password)
                auth.login(request, buyer)
                return redirect('openorders')    
            else:
                status = 'Unable to login. Either username or password is incorrect.'


    context['status'] = status
 
    return render(request, "app/login.html", context)

def loginseller(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM shop WHERE username = %s", [request.POST['username']])
            password = cursor.fetchone()[0]
            if password == request.POST['password']:
                messages.success(request, f'Welcome seller %s back to HONUSupper!' % (request.POST['username']))
                return redirect('loginhome')    
            else:
                status = 'Unable to login. Either username or password is incorrect.'


    context['status'] = status
 
    return render(request, "app/loginseller.html", context)

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

def openorders(request):

    context = {}
    status = ''

    # if request.POST:
    #     ## Check if hall is present
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT shopname FROM orders WHERE buyer_hall = %s", [request.POST['buyer_hall']])
    #         shopname = cursor.fetchone()[0]
    #         if shopname == request.POST['shopname']:
    #             messages.success(request, f'Below are the open orders from %s!' % (request.POST['shopname']))
    #             return redirect('filtered_open_orders')    
    #         else:
    #             status = 'Unable to query. Either hall name or shop name is incorrect.'


    # context['status'] = status

    ## Delete customer
#    if request.POST:
#        if request.POST['action'] == 'delete':
#            with connection.cursor() as cursor:
#                cursor.execute("DELETE FROM orderid WHERE group_order_id = %s", [request.POST['id']])
#
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orderid WHERE delivery_status = 'Order Open' ORDER BY group_order_id DESC")
        grporders = cursor.fetchall()
        # list of tuples

    result_dict = {'records': grporders}

    return render(request,'app/openorders.html', result_dict)

def edit_indiv_order(request, id):
    """links from viewindivorder: edit button"""
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE group_order_id = %s", [id])
            prev = cursor.fetchone()
            group_order_id = prev[0]
            hall = prev[2]
            shopname = prev[3]
            result_dict = {'prev': prev}

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE orders SET qty = %s WHERE group_order_id = %s", (request.POST['qty'], prev[0]))
            messages.success(request, f'Delivery Status has been updated!')
            return redirect(f'/viewindivorder')
 
    return render(request, "app/edit_indiv_order.html", result_dict)

def viewindivorder(request, id):
    ## Delete customer NEED TO FIX!!!! must add condition on item also
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orders WHERE username = %s", [id])

    ## Use raw query to get all objects
    #3
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, buyer_hall, group_order_id, o.shopname, o.item, qty, price, (price*qty) AS total_price FROM orders o, item i WHERE o.shopname = i.shopname AND o.item=i.item AND username = %s", [id])
        indivorders = cursor.fetchall()
        grpid = indivorders[0][2]
        # list of tuples

    result_dict = {'records': indivorders}

    return render(request,'app/viewindivorder.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
        buyer = cursor.fetchone()
    result_dict = {'buyer': buyer}

    return render(request,'app/view.html',result_dict)

def addindivorder(request, id):
    """links from open orders: join button"""
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orderid WHERE group_order_id = %s", [id])
            prev = cursor.fetchone()
            group_ord_id = prev[0]
            hall = prev[2]
            shopname = prev[3]
            result_dict = {'prev': prev}

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    , [request.POST['username'], hall, group_ord_id, hall, shopname, request.POST['item'], request.POST['qty'] ])
            messages.success(request, f'%s added to Group Order! Feel free to order more items.' % (request.POST['item']))
            return redirect(f'/viewindivorder/%s' % (request.POST['username']))
            """should link to viewindivorder"""
 
    return render(request, "app/addindivorder.html", result_dict)

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

# vito
def sellerindex(request):             
    search_string = request.GET.get('shopname','')
    users = "SELECT * FROM orderid WHERE NOT delivery_status = 'Food Delivered' AND shopname ~ \'%s\'"% (search_string)
    c = connection.cursor()
    c.execute(users)
    results = c.fetchall()
    result_dict = {'records': results}

    if request.POST:
        if request.POST['action'] == 'edit':
            return render(request,"app/seller_orderid.html",result_dict)

    return render(request,"app/sellerindex.html",result_dict)

def seller_orderid(request, id):
    """links from sellerindex: edit button"""
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orderid WHERE group_order_id = %s", [id])
            prev = cursor.fetchone()
            group_order_id = prev[0]
            hall = prev[2]
            shopname = prev[3]
            result_dict = {'prev': prev}

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE orderid SET delivery_status = %s WHERE group_order_id = %s", (request.POST['delivery_status'], prev[0]))
            messages.success(request, f'Delivery Status has been updated!')
            return redirect(f'/sellerindex')
 
    return render(request, "app/seller_orderid.html", result_dict)

def seller_menu(request):
    search_string = request.GET.get('shopname','')
    users = "SELECT * FROM item WHERE shopname ~ \'%s\'"% (search_string)
    c = connection.cursor()
    c.execute(users)
    results = c.fetchall()
    result_dict = {'records': results}

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM item WHERE item = %s", [request.POST['id']])

        if request.POST['action'] == 'add_menu':
            return redirect(f'/add_menu')


    return render(request,"app/seller_menu.html",result_dict)

def edit_menu(request, id):

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM item WHERE item = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE item SET shopname = %s, item = %s, price = %s"
                    , [request.POST['shopename'], request.POST['item'], request.POST['price'], id ])
            status = 'Item edited successfully!'
            cursor.execute("SELECT * FROM item WHERE item = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit_menu.html", context)

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
                cursor.execute("SELECT MAX(group_order_id) FROM orderid")
                curr_id = cursor.fetchone()[0] + 1
                cursor.execute("SELECT * FROM shop WHERE shopname = %s", [request.POST['shopname']])
                shopdet = cursor.fetchone()
                opening = shopdet[3]
                closing = shopdet[4]
                status = 'Order Open'
                cursor.execute("INSERT INTO orderid VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        , [curr_id, request.POST['creator'], request.POST['hall'], request.POST['shopname'], opening, closing,
                           request.POST['order_date'] , request.POST['order_by'],status])
                messages.success(request, f'New Group Order created for %s! Please remember to close and send your group order.' % (request.POST['creator']))
                return redirect('openorders')
            else:
                status = '%s Group Order created by Username %s already exists' % (request.POST['shopname'], request.POST['creator'])


    context['status'] = status
    return render(request, "app/addgrouporder.html", context)
