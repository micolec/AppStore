from modulefinder import STORE_NAME
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

# Create your views here.

def basebuyer(request, username):

    context = {'username' : username}

    return render(request, 'app/basebuyer.html', context)

def baseseller(request, username):

    context = {'username' : username}

    return render(request, 'app/baseseller.html', context)

def buyer_menu_choice(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT shopname FROM shop")
        results = cursor.fetchall()

    result_dict = {'shopname': results}

    return render(request, "app/buyer_menu_choice.html", result_dict)

def buyer_menu(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM item WHERE shopname = %s", [request.GET['shopname']])
        results = cursor.fetchall()
        
    result_dict = {'menu': results, 'shopname': request.GET['shopname']}

    return render(request,"app/buyer_menu.html", result_dict)

def buyer_menu(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM item WHERE shopname = %s", [id])
        results = cursor.fetchall()
        
    result_dict = {'menu': results, 'shopname': id}

    return render(request,"app/buyer_menu.html", result_dict)

def buyerstats(request, username):
    with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(user_saved)\
                            FROM (SELECT DISTINCT group_order_id, username, CAST(user_saved AS MONEY)\
                                    FROM orders \
                                    INNER JOIN (SELECT group_order_id, delivery_fee, COUNT(DISTINCT username) AS users,\
                                                ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, \
                                                (delivery_fee - ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) ) AS user_saved\
                                                FROM (SELECT o.group_order_id, delivery_fee, o.username\
                                                        FROM orders o, item i, shop s\
                                                        WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                                                GROUP BY group_order_id, delivery_fee\
                                                ORDER BY group_order_id ) AS t1\
                                    USING(group_order_id)\
                                    WHERE username = %s) AS t2", [username])
            tot = cursor.fetchone()
            tot = tot[0]
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT group_order_id, username, CAST(user_saved AS MONEY)\
                        FROM orders \
                        INNER JOIN (SELECT group_order_id, delivery_fee, COUNT(DISTINCT username) AS users,\
                                    ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, \
                                    (delivery_fee - ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) ) AS user_saved\
                                    FROM (SELECT o.group_order_id, delivery_fee, o.username\
                                            FROM orders o, item i, shop s\
                                            WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                                    GROUP BY group_order_id, delivery_fee\
                                    ORDER BY group_order_id ) AS t1\
                        USING(group_order_id)\
                        where username = %s", [username])
        ranking = cursor.fetchall()

    result_dict = {'records': ranking, 'username':username, 'total':tot}

    return render(request,'app/buyerstats.html', result_dict)

def index(request):
    with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(DISTINCT username) FROM orders")
            users = cursor.fetchone()
            users = users[0]
    with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(users*user_saved)\
                            FROM (	SELECT group_order_id, delivery_fee, COUNT(DISTINCT username) AS users,\
                            ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, \
                            (delivery_fee - ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) ) AS user_saved\
                            FROM (SELECT o.group_order_id, delivery_fee, o.username\
                                FROM orders o, item i, shop s\
                                WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                            GROUP BY group_order_id, delivery_fee ) AS t1")
            tot = cursor.fetchone()
            tot = tot[0]
    with connection.cursor() as cursor:
            cursor.execute("SELECT ROUND(AVG(users),0)\
                            FROM (  SELECT group_order_id, COUNT(DISTINCT username) AS users\
                                    FROM (SELECT o.group_order_id, delivery_fee, o.username\
                                            FROM orders o, item i, shop s\
                                            WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item\
                                            GROUP BY group_order_id, delivery_fee, o.username) AS orders_with_price\
                                    GROUP BY group_order_id, delivery_fee) AS t1")
            avg = cursor.fetchone()
            avg = avg[0]

    with connection.cursor() as cursor:
            cursor.execute("SELECT CAST(ROUND(SUM(users*user_saved)/SUM(users),2) AS MONEY)\
                            FROM (	SELECT group_order_id, delivery_fee, COUNT(DISTINCT username) AS users,\
                                    ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, \
                                    (delivery_fee - ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) ) AS user_saved\
                                    FROM (SELECT o.group_order_id, delivery_fee, o.username\
                                        FROM orders o, item i, shop s\
                                        WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                                    GROUP BY group_order_id, delivery_fee ) AS t1")

            order = cursor.fetchone()
            order = order[0]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, SUM(user_saved)\
                        FROM ( SELECT DISTINCT group_order_id, username, CAST(user_saved AS MONEY)\
                                FROM orders \
                                INNER JOIN (SELECT group_order_id, delivery_fee, COUNT(DISTINCT username) AS users,\
                                            ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, \
                                            (delivery_fee - ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) ) AS user_saved\
                                            FROM (SELECT o.group_order_id, delivery_fee, o.username\
                                                    FROM orders o, item i, shop s\
                                                    WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                                            GROUP BY group_order_id, delivery_fee ) AS t1\
                                USING(group_order_id) ) AS t2\
                        GROUP BY username\
                        ORDER BY sum DESC\
                        LIMIT 3")
        top3 = cursor.fetchall()
    
    result_dict = {'tot_users': users, 'tot_amt': tot, 'avg_users':avg, 'avg_order': order, 'top': top3}


    return render(request,'app/index.html', result_dict)

def login(request):
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
            username = request.POST['username']
            password = request.POST['password']
            if username == 'superadmin' and password == 'superadmin':
                messages.success(request, f'Welcome superadmin back to HONUSupper!')
                return redirect('buyerindex')
            with connection.cursor() as cursor:
                try:
                    cursor.execute("SELECT password FROM buyer WHERE username = %s", [request.POST['username']])
                    password = cursor.fetchone()[0]
                    if password == request.POST['password']:
                        messages.success(request, f'Welcome buyer %s back to HONUSupper!' % (request.POST['username']))
                        return redirect(f'/openorders/%s' % username) 
                    else:
                        status = 'Unable to login. Password is incorrect.'
                except:
                    status = 'Unable to login. Username is incorrect.'
    context['status'] = status

    return render(request, "app/login.html", context)

def logout(request):
    return render(request, 'app/logout.html')

def stats(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT buyer_hall, shopname, popularity, \
                        RANK() OVER(PARTITION BY buyer_hall ORDER BY popularity DESC) Rank\
                        FROM(\
                            SELECT buyer_hall, shopname, COUNT(shopname) AS popularity\
                            FROM orders \
                            GROUP BY buyer_hall, shopname) AS t1\
                        ORDER BY buyer_hall, rank	")
        ranking = cursor.fetchall()
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT shopname, SUM(total_price) AS shop_total, COUNT(*) AS group_size\
                        FROM (SELECT \
                            o.shopname,o.item, qty, price AS price_per_item, \
                            (price * qty) AS total_price\
                            FROM orders o, item i\
                            WHERE o.shopname = i.shopname AND o.item = i.item) AS orders_with_price\
                        GROUP BY shopname; ")
        revenue = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("SELECT shopname, CAST(ROUND(AVG(CAST(shop_total AS DECIMAL(6,2))),2) AS MONEY) AS avg_perday\
                        FROM (\
                                SELECT shopname, SUM(total_price) AS shop_total, COUNT(*) AS group_size, order_date\
                                FROM (SELECT o.username,order_date,\
                                    o.shopname,o.item, qty, price AS price_per_item, \
                                    (price * qty) AS total_price\
                                    FROM orders o, item i, orderid oi\
                                    WHERE o.shopname = i.shopname AND o.item = i.item \
                                    AND oi.group_order_id = o.group_order_id) AS orders_with_price\
                                GROUP BY shopname, order_date\
                                ORDER BY shopname, order_date ) AS t1\
                        GROUP BY shopname")
        avg_day = cursor.fetchall()
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT shopname, COUNT(*) AS group_size, SUM(total_price) AS shop_total, order_date, CAST(ROUND(AVG(CAST(total_price AS DECIMAL(10,2))),2) AS MONEY)\
                        FROM (SELECT o.username,order_date,\
                            o.shopname,o.item, qty, price AS price_per_item, \
                            (price * qty) AS total_price\
                            FROM orders o, item i, orderid oi\
                            WHERE o.shopname = i.shopname AND o.item = i.item \
                            AND oi.group_order_id = o.group_order_id) AS orders_with_price\
                        GROUP BY shopname, order_date\
                        ORDER BY shopname, order_date;")
        daily_stats = cursor.fetchall()
    
    

    result_dict = {'records': ranking, 'records2': revenue, 'records3': avg_day, 'records4': daily_stats}

    return render(request,'app/stats.html', result_dict)


def promo(request):

    with connection.cursor() as cursor:
        cursor.execute("SELECT buyer_hall, shopname, COUNT(shopname)  \
                        FROM orders  \
                        GROUP BY buyer_hall, shopname\
                        HAVING (buyer_hall, COUNT(shopname)) IN (\
                            SELECT buyer_hall, MAX(popularity) \
                            FROM ( \
                                SELECT buyer_hall, shopname, COUNT(shopname) AS popularity\
                                FROM orders \
                                GROUP BY buyer_hall, shopname) AS t1\
                            GROUP BY buyer_hall) ")
        popular = cursor.fetchall()
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT b.first_name, b.last_name,  b.username, b.hall,b.phone_number\
                        FROM buyer b\
                        WHERE b.username NOT IN  (\
                            SELECT username\
                            FROM orders) \
                ORDER BY b.hall, b.last_name, b.first_name")
        buyers = cursor.fetchall()

    result_dict = {'records': popular, 'records2': buyers}

    return render(request,'app/promo.html', result_dict)

def openorders(request, username):

    status = ''

    with connection.cursor() as cursor:
        cursor.execute(";with t1 AS (\
                        SELECT *\
                        FROM orderid \
                        WHERE delivery_status = 'Order Open'\
                        ORDER BY group_order_id DESC ),\
                    t2 AS (\
                        SELECT group_order_id, CAST(delivery_fee AS MONEY), COUNT(DISTINCT username) AS users,\
                        CAST(ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS MONEY) AS delivery_fee_per_pax\
                        FROM (SELECT o.group_order_id, delivery_fee, o.username\
                            FROM orders o, item i, shop s\
                            WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                        GROUP BY group_order_id, delivery_fee\
                        ORDER BY group_order_id)\
                    SELECT t1.group_order_id, t1.creator, t1.hall, t1.shopname, t1.order_date,\
                        t1.order_by, t1.delivery_status, t2.delivery_fee, t2.users, t2.delivery_fee_per_pax\
                    FROM t1\
                    INNER JOIN t2\
                    USING (group_order_id)\
                    WHERE hall = (SELECT hall FROM buyer WHERE username = %s)\
                    ORDER BY t1.group_order_id DESC ", [username])
        grporders = cursor.fetchall()
        # list of tuples

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orderid WHERE delivery_status = 'Order Open' AND creator = %s ORDER BY group_order_id DESC", [username])
        creator = cursor.fetchall()

    ## Use raw query to get all objects
    if request.POST:
        with connection.cursor() as cursor:
            shopname = request.POST['shopname']
            cursor.execute("SELECT shopname FROM shop")
            shops = cursor.fetchall()
            for index, tuple in enumerate(shops):
                if shopname == tuple[0]:
                    messages.success(request, f'Below are the open orders from %s!' % (request.POST['shopname']))
                    return redirect(f'/filtered_openorders/%s/%s' %(username,shopname))
            status = 'Unable to query. Shop name is incorrect.'

    result_dict = {'records': grporders, 'status': status, 'username' : username, 'records2':creator}

    return render(request,'app/openorders.html', result_dict)

def filtered_openorders(request, username, shopname):

    status = ''

    # Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute(";with t1 AS (\
                        SELECT *\
                        FROM orderid \
                        WHERE delivery_status = 'Order Open'\
                        ORDER BY group_order_id DESC ),\
                    t2 AS (\
                        SELECT group_order_id, CAST(delivery_fee AS MONEY), COUNT(DISTINCT username) AS users,\
                        CAST(ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS MONEY) AS delivery_fee_per_pax\
                        FROM (SELECT o.group_order_id, delivery_fee, o.username\
                            FROM orders o, item i, shop s\
                            WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item) AS orders_with_price\
                        GROUP BY group_order_id, delivery_fee\
                        ORDER BY group_order_id)\
                    SELECT t1.group_order_id, t1.creator, t1.hall, t1.shopname, t1.order_date,\
                        t1.order_by, t1.delivery_status, t2.delivery_fee, t2.users, t2.delivery_fee_per_pax\
                    FROM t1\
                    INNER JOIN t2\
                    USING (group_order_id)\
                    WHERE hall = (SELECT hall FROM buyer WHERE username = %s)\
                    AND shopname = %s\
                    ORDER BY t1.group_order_id DESC ", [username, shopname])
        grporders = cursor.fetchall()
 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orderid WHERE delivery_status = 'Order Open' AND creator = %s ORDER BY group_order_id DESC", [username])
        creator = cursor.fetchall()

    ## Use raw query to get all objects
    if request.POST:
        with connection.cursor() as cursor:
            shopname = request.POST['shopname']
            cursor.execute("SELECT shopname FROM shop")
            shops = cursor.fetchall()
            for index, tuple in enumerate(shops):
                if shopname == tuple[0]:
                    messages.success(request, f'Below are the open orders from %s!' % (request.POST['shopname']))
                    return redirect(f'/filtered_openorders/%s/%s' %(username,shopname))
            status = 'Unable to query. Shop name is incorrect.'

    result_dict = {'records': grporders, 'status': status, 'username' : username, 'records2':creator}   

    return render(request,'app/filtered_openorders.html', result_dict)

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

def deliverystatus(request, username):
    context = {}
    status = ''
    fee = ''
    indivorders = ''
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT(oi.group_order_id) \
                        FROM orders o, orderid oi \
                        WHERE oi.delivery_status != 'Order Open' AND o.group_order_id = oi.group_order_id AND username = %s" , [username])
        indivorders = cursor.fetchall()
        if indivorders:
            grpid = indivorders[0]
        #rn the second table is using orderid = grpid which is the first entry of first table
        # list of tuples

    with connection.cursor() as cursor:
        if indivorders:
            cursor.execute(";with t1 as ( \
                SELECT group_order_id, SUM(total_price) AS group_total, order_date, order_by, \
                ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, COUNT(DISTINCT username) AS users, delivery_fee, delivery_status \
                FROM ( \
                    SELECT o.username, o.group_order_id, (price * qty) AS total_price, delivery_fee, delivery_status, order_date, order_by \
                    FROaM orders o, item i, shop s, orderid oi \
                    WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item AND oi.group_order_id = o.group_order_id \
                    ORDER BY group_order_id, username) AS orders_with_price \
                    GROUP BY group_order_id, delivery_fee, delivery_status, order_date, order_by \
                    ORDER BY group_order_id \
                    ), \
                t2 as ( SELECT username, buyer_hall, shopname, group_order_id, SUM(total_price) AS indiv_total \
                    FROM ( SELECT username, buyer_hall, o.shopname, group_order_id,(price * qty) AS total_price \
                        FROM orders o, item i \
                        WHERE o.shopname = i.shopname AND o.item = i.item) AS orders_with_price \
                        GROUP BY username, group_order_id, buyer_hall, shopname \
                        ORDER BY group_order_id) \
                SELECT t2.group_order_id, t2.username, t2.buyer_hall, t2.shopname, t1.order_date, t1.order_by, \
                (t2.indiv_total + CAST(t1.delivery_fee_per_pax AS MONEY)) AS Total, t1.users,  \
                (CAST(t1.delivery_fee - t1.delivery_fee_per_pax AS MONEY)) AS delivery_saved, t1.delivery_status \
                FROM t1,t2 \
                WHERE t1.group_order_id = t2.group_order_id AND t2.username = %s AND t1.group_order_id = %s \
                ORDER BY group_order_id DESC", [username, grpid])
            fee = cursor.fetchall()
   
    result_dict = {'records2': fee, 'status':status, 'username' : username}

    return render(request,'app/deliverystatus.html',result_dict)

def viewindivorder(request, id):
    ## Delete customer NEED TO FIX!!!! must add condition on item also
    status = ''
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, buyer_hall, group_order_id, o.shopname, o.item, qty, price, (price*qty) AS total_price, paid FROM orders o, item i WHERE o.shopname = i.shopname AND o.item=i.item AND username = %s ORDER BY group_order_id DESC" , [id])
        indivorders = cursor.fetchall()
        if indivorders:
            grpid = indivorders[0][2]
        #rn the second table is using orderid = grpid which is the first entry of first table
        # list of tuples
    with connection.cursor() as cursor:
        fee = 0
        if indivorders:
            cursor.execute(";with t1 as ( \
                SELECT group_order_id, SUM(total_price) AS group_total, \
                ROUND((delivery_fee *1.0)/ COUNT(DISTINCT username), 2) AS delivery_fee_per_pax, COUNT(DISTINCT username) AS users, delivery_fee, delivery_status \
                FROM (\
                    SELECT o.username, o.group_order_id, (price * qty) AS total_price, delivery_fee, delivery_status\
                    FROM orders o, item i, shop s, orderid oi\
                    WHERE o.shopname = i.shopname AND o.shopname = s.shopname AND o.item = i.item AND oi.group_order_id = o.group_order_id\
                    ORDER BY group_order_id, username) AS orders_with_price\
                    GROUP BY group_order_id, delivery_fee, delivery_status \
                    ORDER BY group_order_id \
                    ),\
                t2 as ( SELECT username, group_order_id, SUM(total_price) AS indiv_total \
                    FROM ( SELECT username, group_order_id,(price * qty) AS total_price\
                        FROM orders o, item i\
                        WHERE o.shopname = i.shopname AND o.item = i.item) AS orders_with_price\
                        GROUP BY username, group_order_id\
                        ORDER BY group_order_id) \
                SELECT t2.username, t2.group_order_id, t2.indiv_total, t1.delivery_fee, t1.users,  \
                    t1.delivery_fee_per_pax, (t2.indiv_total + CAST(t1.delivery_fee_per_pax AS MONEY)) AS Total, t1.delivery_status\
                FROM t1,t2\
                WHERE t1.group_order_id = t2.group_order_id AND t2.username = %s\
                ORDER BY group_order_id DESC", [id])
            fee = cursor.fetchall()
            total = fee[0][6]
            total = float(total[1:7])
           
    with connection.cursor() as cursor:
            cursor.execute("SELECT wallet_balance FROM buyer WHERE username = %s", [id])
            money = cursor.fetchone()
            existing = money[0]
            existing = float(existing[1:])
    
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
            prev = cursor.fetchone()
            username = prev[0]
            result_dict = {'prev': prev}
   
    
    status = ''
    if request.POST:
        #PROBLEM: delete deletes every order buyer has bought!!! vito pls help fix thanku :>
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orders WHERE username = %s", [id])
        if request.POST['action'] == 'deduct':
            with connection.cursor() as cursor:
                curgrp = request.POST['curgrp']
                totals = request.POST['totals']
                totals = float(totals[1:])
                if (existing - totals) >= 5:
                    cursor.execute("UPDATE buyer SET wallet_balance = (%s - %s) WHERE username = %s", [existing, totals, id])
                    cursor.execute("UPDATE orders SET paid = 'Paid' WHERE username = %s AND group_order_id = %s", [id, curgrp])
                    messages.success(request, f'Paid! Wallet Balance has been updated.')
                    return redirect(f'/viewindivorder/%s' % id)    
                else:
                    status = 'Wallet has insufficient balance. Please Top Up! Ensure wallet has minimum $5 after payment.'       
   
    result_dict = {'records': indivorders, 'records2': fee, 'status':status, 'groupid':grpid, 'username':id, 'prev': prev}

    return render(request,'app/viewindivorder.html',result_dict)



def topup(request, id):
    
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
            prev = cursor.fetchone()
            username = prev[0]
            balance = float((prev[6])[1:])

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE buyer SET wallet_balance = (%s + %s)  WHERE username = %s", (balance, request.POST['wallet_balance'], prev[0]))
            messages.success(request, f'Wallet Balance has been updated!')
            return redirect(f'/viewindivorder/%s' % id)   
    
    result_dict = {'username' : id, 'prev':prev}
    return render(request, "app/topup.html", result_dict)



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
            cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    , [request.POST['username'], hall, group_ord_id, hall, shopname, request.POST['item'], request.POST['qty'], 'Unpaid' ])
            messages.success(request, f'%s added to Group Order! Feel free to order more items.' % (request.POST['item']))
            return redirect(f'/viewindivorder/%s' % (request.POST['username']))
            """should link to viewindivorder"""
    
    result_dict = {'username' : id, 'prev' : prev}

    return render(request, "app/addindivorder.html", result_dict)

def addgrouporder(request, username):
    context = {}
    status = ''

    with connection.cursor() as cursor:
        cursor.execute("SELECT hall FROM buyer WHERE username = %s", [username])
        hall = cursor.fetchone()[0]

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orderid WHERE creator = %s AND hall = %s AND shopname = %s AND order_date = %s AND order_by = %s", [username, hall, request.POST['shopname'],request.POST['order_date'], request.POST['order_by']])
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
                        , [curr_id, username, hall, request.POST['shopname'], opening, closing,
                           request.POST['order_date'] , request.POST['order_by'],status])
                messages.success(request, f'New Group Order created for %s! Please add your order and remember to submit your group order.' % (username))
                return redirect(f'/addindivorder/%s' % (curr_id))
            else:
                status = '%s Group Order created by Username %s already exists' % (request.POST['shopname'], username)


    context = {'status' : status, 'username' : username, 'hall' : hall}

    return render(request, "app/addgrouporder.html", context)

def submit_group_order(request, id, username):
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
            return redirect(f'/openorders/%s' % username)
    result_dict['username'] = id

    return render(request, "app/submit_group_order.html", result_dict)

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
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [id])
        buyer = cursor.fetchone()
    result_dict = {'buyer': buyer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def edit(request, username):

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buyer WHERE username = %s", [username])
        obj = cursor.fetchone()
        balance = float((obj[6])[1:])

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE buyer SET password = %s, first_name = %s, last_name = %s, phone_number = %s, hall = %s WHERE username = %s"
                        , [request.POST['password'], request.POST['first_name'], request.POST['last_name'],
                            request.POST['phone_number'] , request.POST['hall'], username ])
                messages.success(request, f'%s profile has been updated successfully!' % username)
                cursor.execute("SELECT password, first_name, last_name, phone_number, hall FROM buyer WHERE username = %s", [username])
                obj = cursor.fetchone()
                return redirect(f'/edit/%s' % username)

        except:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE buyer SET wallet_balance = (%s + %s)  WHERE username = %s", (balance, request.POST['wallet_balance'], obj[0]))
                messages.success(request, f'Wallet Balance has been updated!')
                return redirect(f'/edit/%s' % username)


    context["obj"] = obj
    context["status"] = status
    context["username"] = username
 
    return render(request, "app/edit.html", context)

## SELLER

# Seller's homepage
def loginseller(request):
    context = {}
    status = ''

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if username == 'superadmin' and password == 'superadmin':
            messages.success(request, f'Welcome superadmin back to HONUSupper!')
            context['username'] = username
            return redirect('sellerindex')
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT password FROM shop WHERE username = %s", [request.POST['username']])
                password = cursor.fetchone()[0]
                if password == request.POST['password']:
                    messages.success(request, f'Welcome seller %s back to HONUSupper!' % (request.POST['username']))
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT shopname FROM shop WHERE username = %s", [username])
                        shopname = cursor.fetchone()
                    return redirect(f'/sellerindex/%s' % shopname)    
                else:
                    status = 'Unable to login. Password is incorrect.'
            except:
                status = 'Unable to login. Username is incorrect.'

    context['status'] = status
 
    return render(request, "app/loginseller.html")

def sellerindex(request, shopname):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orderid WHERE NOT delivery_status = 'Food Delivered' AND NOT delivery_status = 'Order Open' AND shopname = %s", [shopname])
        results = cursor.fetchall()
        result_dict = {'records': results}

    if request.POST:
        if request.POST['action'] == 'edit':
            return redirect(f'/seller_orderid/%s' % id)
    result_dict['shopname'] = shopname

    return render(request, "app/sellerindex.html", result_dict)

def seller_orderid(request, id):
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
            return redirect(f'/sellerindex/%s' % shopname)
    result_dict['username'] = id

    return render(request, "app/seller_orderid.html", result_dict)

def seller_menu(request, shopname):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM item WHERE shopname = %s", [shopname])
        results = cursor.fetchall()
        result_dict = {'records': results}

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM item WHERE item = %s", [request.POST['id']])
                messages.success(request, f'Item has been deleted!')
                return redirect(f'/seller_menu/%s' % shopname)
        

        if request.POST['action'] == 'add_menu':
            with connection.cursor() as cursor:
                return redirect(f'/add_menu/%s' % shopname)

        if request.POST['action'] == 'edit_menu':
            with connection.cursor() as cursor:
                item = cursor.fetchone()
            return redirect(f'/edit_menu/%s' % item)

    result_dict['shopname'] = shopname

    return render(request,"app/seller_menu.html",result_dict)

def add_menu(request, id):
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orderid WHERE group_order_id = %s", [id])
            prev = cursor.fetchone()
            group_ord_id = prev[0]
            hall = prev[2]
            shopname = prev[3]
            result_dict = {'prev': prev}

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO item VALUES (%s, %s, %s)"
                    , id, request.POST['item'], request.POST['price'])
            messages.success(request, f'%s has been added into the menu!' % (request.POST['item']))
            return redirect(f'/seller_menu/%s' % (id))
 
    return render(request, "app/add_menu.html", result_dict)

def edit_menu(request, item):
    with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM item WHERE item = %s", [item])
            prev = cursor.fetchone()
            shopname = prev[0]
            item = prev[1]
            price = prev[2]
            result_dict = {'prev': prev}

    if request.POST:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE item SET price = %s WHERE item = %s", (request.POST['price'], item))
            messages.success(request, f'Item has been updated!')
            return redirect(f'/seller_menu/%s' % (shopname))
    result_dict['item'] = item

    return render(request, "app/edit_menu.html", result_dict)

def ordersindex(request):             
    
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orderid WHERE group_order_id = %s", [request.POST['id']])

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orderid ORDER BY group_order_id")
        sellers = cursor.fetchall()
    
    result_dict = {'records': sellers}

    return render(request,"app/ordersindex.html",result_dict)

def orderadd(request):
    context = {}
    curr_id = ''
    hall = ''
    opening = ''
    closing = ''

    with connection.cursor() as cursor:
        cursor.execute("SELECT MAX(group_order_id) FROM orderid")
        curr_id = cursor.fetchone()[0] + 1



    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT hall FROM buyer WHERE username = %s", [request.POST['creator']])
            hall = cursor.fetchone()[0]
            cursor.execute("SELECT creator, shopname, order_date, order_by, delivery_status FROM orderid WHERE creator = %s AND hall = %s AND shopname = %s AND order_date = %s AND order_by = %s", [request.POST['creator'], hall, request.POST['shopname'],request.POST['order_date'], request.POST['order_by']])
            orderid = cursor.fetchone()
        ## No orderid with same details
            if orderid == None:
                cursor.execute("SELECT * FROM shop WHERE shopname = %s", [request.POST['shopname']])
                shopdet = cursor.fetchone()
                opening = shopdet[3]
                closing = shopdet[4]
                cursor.execute("INSERT INTO orderid VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    , [curr_id, request.POST['creator'], hall,
                    request.POST['shopname'] , opening, closing, request.POST['order_date'],
                    request.POST['order_by'], request.POST['delivery_status']])
                messages.success(request, f'Group Order Id %s added!' % (curr_id))
                return redirect('ordersindex')    


    context['curr_id'] = curr_id
    context['hall'] = hall
    context['opening'] = opening
    context['closing'] = closing
 
    return render(request, "app/orderadd.html", context)

def orderedit(request, group_order_id):

    context ={}
    hall = ''
    opening = ''
    closing = ''

    with connection.cursor() as cursor:
        cursor.execute("SELECT creator, hall, shopname, opening, closing, order_date, order_by, delivery_status FROM orderid WHERE group_order_id = %s", [group_order_id])
        obj = cursor.fetchone()

    status = ''

    if request.POST:
            with connection.cursor() as cursor:
                cursor.execute("SELECT hall FROM buyer WHERE username = %s" ,[request.POST['creator']])
                hall = cursor.fetchone()
                cursor.execute("SELECT * FROM shop WHERE shopname = %s", [request.POST['shopname']])
                shopdet = cursor.fetchone()
                opening = shopdet[3]
                closing = shopdet[4]
                cursor.execute("UPDATE orderid SET creator = %s, hall = %s, shopname = %s, opening = %s, closing = %s, order_date = %s, order_by = %s, delivery_status = %s WHERE group_order_id = %s"
                        , [request.POST['creator'], hall, request.POST['shopname'], opening, closing,
                           request.POST['order_date'], request.POST['order_by'], request.POST['delivery_status'], group_order_id ])
                messages.success(request, f'Group Order Id %s has been updated successfully!' % group_order_id)
                cursor.execute("SELECT creator, hall, shopname, opening, closing, order_date, order_by, delivery_status FROM orderid WHERE group_order_id = %s", [group_order_id])
                obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
    context["group_order_id"] = group_order_id
    context['hall'] = hall
    context['opening'] = opening
    context['closing'] = closing
 
    return render(request, "app/orderedit.html", context)

def indivorderindex(request, group_order_id):
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM orders WHERE username = %s AND group_order_id = %s", [request.POST['id'], group_order_id])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE group_order_id = %s ORDER BY username", [group_order_id])
        indivorder = cursor.fetchall()
        # list of tuples

    result_dict = {'records': indivorder, 'group_order_id' : group_order_id}

    return render(request,'app/indivorderindex.html',result_dict)

def indivorderadd(request, group_order_id):
    context = {}
    creator_hall = ''
    buyer_hall = ''
    shopname = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE group_order_id = %s AND username = %s AND item = %s", [group_order_id, request.POST['username'], request.POST['item']])
            indivorder = cursor.fetchone()
            if indivorder == None:
                cursor.execute("SELECT * FROM orderid WHERE group_order_id = %s", [group_order_id])
                order = cursor.fetchone()
                creator_hall = order[2]
                shopname = order[3]
                cursor.execute("SELECT hall FROM buyer WHERE username = %s" ,[request.POST['username']])
                buyer_hall = cursor.fetchone()

                cursor.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['username'], buyer_hall, group_order_id,
                        creator_hall , shopname, request.POST['item'], request.POST['qty'],
                        request.POST['paid']])
                messages.success(request, f'Individual Order %s %s %s added to Group Order Id %s!' % (request.POST['username'], request.POST['qty'], request.POST['item'], group_order_id))
                return redirect(f'/indivorderindex/%s' % group_order_id)    


    context['group_order_id'] = group_order_id
    context['creator_hall'] = creator_hall
    context['buyer_hall'] = buyer_hall
    context['shopname'] = shopname
 
    return render(request, "app/indivorderadd.html", context)

def indivorderedit(request, group_order_id, username, item):

    context ={}
    status = ''

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE group_order_id = %s AND username = %s AND item = %s", [group_order_id, username, item])
        obj = cursor.fetchone()

    status = ''

    if request.POST:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE orders SET qty = %s, paid = %s WHERE group_order_id = %s AND username = %s AND item = %s "
                        , [request.POST['qty'], request.POST['paid'], group_order_id, username, item])
                messages.success(request, f'Buyer %s order in Group Order Id %s has been updated successfully!' % (username, group_order_id))
                cursor.execute("SELECT qty, paid FROM orders WHERE group_order_id = %s AND username = %s AND item = %s", [group_order_id, username, item])
                obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
    context['username'] = username
    context['group_order_id'] = group_order_id
    context['item'] = item
 
    return render(request, "app/indivorderedit.html", context)
