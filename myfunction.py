from django.http import *
from django.shortcuts import *
from datetime import datetime
from pymysql import *
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import *
import http.client
from connectionfile import *

conn=Connect("127.0.0.1","root",'',"project")

def indexpage(request):
    return render(request,'index.html')

def home(request):
    return render(request,"home.html")

def inputadmin(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")
    return render(request,"addadmin.html")

def addadmin(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")
    global conn
    s = "insert into admin values('" + request.GET["textbox1"] + "','" + request.GET["textbox2"] + "','" +request.GET["type"] + "','')"

    cr = conn.cursor()
    s1 = "select * from admin"

    cr.execute(s1)
    flag = False
    result = cr.fetchall()

    for row in result:
        if row[0] == request.GET["textbox1"]:
            flag = True
            break

    d = {}
    if flag == True:
        d["message"] = "duplicate email"

    else:
        cr.execute(s)
        conn.commit()
        d["message"] = "admin added successfully"

    return render(request, "confirmadmin.html", d)

def viewadmin(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query="select * from admin"

    cr=conn.cursor()
    cr.execute(query)

    result=cr.fetchall()
    x=[]
    for row in result:
        d={}
        d["Email"]=row[0]
        d["Password"] = row[1]
        d["Type"] = row[2]
        x.append(d)

    return render(request,"viewadmin.html",{"data":x})


def removeadmin(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")
    global conn
    query="delete from admin where email='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(query)
    conn.commit()
    d={"message":"admin removed"}
    return render(request, "confirmadmin.html", d)

def editadmin(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")
    global conn
    s="select * from admin where Email='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(s)
    result=cr.fetchone()

    d={}
    d["Email"]=result[0]
    d["Type"] = result[2]

    return render(request, "getdata.html", d)


def save(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")
    global conn
    s="update admin set Type='"+request.GET["type"]+"' where Email='"+request.GET["textbox1"]+"'"
    cr=conn.cursor()
    cr.execute(s)
    conn.commit()

    d={"message":"Data updated"}
    return render(request,"confirmadmin.html",d)

def login(request):
    return render(request,"adminlogin.html")

def userlogin(request):
    return render(request,"userlogin.html")

def landing(request):
    return render(request,"landing.html")

@csrf_exempt
def checklogin(request):
    global conn
    s = "select * from admin "

    cr = conn.cursor()
    cr.execute(s)

    result = cr.fetchall()
    flag = False
    for row in result:
        if request.POST["textbox1"] == row[0] and request.POST["textbox2"] == row[1]:
            request.session['email'] = request.POST["textbox1"]
            flag = True
            break
    d = {}
    if flag == True:
        d = {"message": "Login Successful"}
        return render(request, "landing.html",d)

    else:

        d['msg'] = "wrong email and password"
        return render(request, "adminlogin.html", d)

@csrf_exempt
def checklogin2(request):
    global conn
    s = "select * from signup "

    cr = conn.cursor()
    cr.execute(s)

    result = cr.fetchall()
    flag = False
    for row in result:
        if request.POST["textbox1"] == row[0] and request.POST["textbox2"] == row[4]:
            request.session['useremail'] = request.POST["textbox1"]
            request.session['usertype'] = row[8]
            flag = True
            break
    d = {}
    if flag == True:
        d = {"message": "Login Successful"}
        return render(request, "userlanding.html",d)

    else:

        d['msg'] = "wrong email and password"
        return render(request, "userlogin.html", d)


def logout(request):
    del request.session["email"]
    return HttpResponseRedirect("login")

def logoutuser(request):
    del request.session["useremail"]
    return HttpResponseRedirect("userlogin")


def addnews(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    return render(request, "addnews.html")

def insertnews(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    dt=datetime.now().date()
    global conn
    s = "insert into newstable values('' ,'" + request.GET["textbox1"] + "','"+str(dt)+"','" +request.GET["textbox2"] + "')"

    cr = conn.cursor()
    s1 = "select * from newstable"

    cr.execute(s1)
    flag = False
    result = cr.fetchall()

    for row in result:
        if row[1] == request.GET["textbox1"]:
            flag = True
            break

    d = {}
    if flag == True:
        d["message"] = "duplicate news"

    else:
        cr.execute(s)
        conn.commit()
        d["message"] = "news added successfully"

    return render(request, "confirmadmin.html", d)


def viewnews(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query="select * from newstable"

    cr=conn.cursor()
    cr.execute(query)

    result=cr.fetchall()

    x=[]
    for row in result:
        d={}
        d['id']=row[0]
        d["title"] = row[1]
        d["description"] = row[3]
        x.append(d)

    return render(request,"viewnews.html",{"data":x})

def removenews(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query="delete from newstable where id='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(query)
    conn.commit()
    d={"message":"news removed"}
    return render(request,"confirmadmin.html",d)

def editnews(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    s="select * from newstable where id='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(s)
    result=cr.fetchone()

    d={}
    d['id'] = result[0]
    d["title"]=result[1]
    d["dateofnews"]=result[2]
    d["description"] = result[3]

    return render(request, "getnewsdata.html", d)

def savenews(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    global conn

    s="update newstable set description='"+request.GET["textbox2"]+"' where id='"+request.GET["id"]+"'"
    s1="update newstable set title='"+request.GET["textbox1"]+"' where id='"+request.GET["id"]+"'"
    cr=conn.cursor()
    cr.execute(s)
    cr.execute(s1)

    conn.commit()

    d={"message":"Data updated"}
    return render(request,"confirmadmin.html",d)

def viewpublicnews(request):


    global conn
    query="select * from newstable"

    cr=conn.cursor()
    cr.execute(query)

    result=cr.fetchall()

    x=[]
    for row in result:
        d={}
        d['id']=row[0]
        d["title"] = row[1]
        d["description"] = row[3]
        x.append(d)

    return render(request,"viewpublicnews.html",{"data":x})

def openchangepass(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    return render(request,'adminchangepassword.html')

@csrf_exempt
def changepassword(request):
    if not("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    s = "select * from admin where Email='" + request.POST["email"] + "' and Password='"+request.POST['oldpassword']+"'"
    cr = conn.cursor()
    result=cr.execute(s)
    print(result)

    d={}
    if result==1:
        s1 = "update admin set Password='" + request.POST['newpassword'] + "' where Email='" + request.POST['email'] + "'"
        cr.execute(s1)
        conn.commit()
        d['message'] = 'password changed successfully'

    else:
        d['message'] = 'email and oldpassword not match/invalid credentials'

    return render(request, "confirmadmin.html", d)

def signup(request):
    return render(request,"signup.html")

def insertuser(request):
    dt2=datetime.now().date()
    photo =request.FILES['photo']
    global conn
    cr = conn.cursor()
    s1 = "select * from signup"

    cr.execute(s1)
    flag = False
    result = cr.fetchall()

    for row in result:
        if row[0] == request.POST["email"]:
            flag = True
            break

    d = {}
    if flag == True:
        d["message"] = "duplicate user"

    else:
        fs = FileSystemStorage()
        fileName = fs.save(photo.name, photo)
        s = "insert into signup values('" + request.POST["email"] + "','" + request.POST["fullname"] + "','" + request.POST["mobileno"] + "','" + request.POST["dob"] + "','" + request.POST["newpassword"] + "','','" +  request.POST["aadhaar"] + "','" + fileName + "','"+request.POST['usertype']+"')"

        cr.execute(s)
        conn.commit()
        d["message"] = "user added successfully"

    return render(request, "confirm.html", d)

def openchangeuserpass(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    return render(request,'userchangepassword.html')

@csrf_exempt
def changeuserpassword(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    s = "select * from signup where email='" + request.POST["email"] + "' and password='"+request.POST['oldpassword']+"'"
    cr = conn.cursor()
    result=cr.execute(s)

    d={}
    if result==1:
        s1 = "update signup set password='" + request.POST['newpassword'] + "' where email='" + request.POST['email'] + "'"
        cr.execute(s1)
        conn.commit()
        d['message'] = 'password changed successfully'

    else:
        d['message'] = 'email and oldpassword not match/invalid credentials'

    return render(request, "confirm.html", d)



def viewuser (request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query = "select * from signup"

    cr = conn.cursor()
    cr.execute(query)

    res = cr.fetchall()
    x=[]
    for row in res:
        d={}
        d['email']=row[0]
        d['fullname']=row[1]
        d['mobileno']=row[2]
        d['dob']=row[3]
        d['password']=row[4]
        d['otp']=row[5]
        d['aadhaarno']=row[6]
        d['photo']=row[7]
        x.append(d)
    return render(request,'viewuser.html',{'x':x})

def removeuser(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query="delete from signup where email='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(query)
    conn.commit()
    d={"message":"user removed"}
    return render(request,"confirmadmin.html",d)

def viewuserprofile(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    query = "select * from signup where email='"+request.session['useremail']+"'"

    cr = conn.cursor()
    cr.execute(query)

    res = cr.fetchall()
    x = []
    for row in res:
        d = {}
        d['email'] = row[0]
        d['fullname'] = row[1]
        d['mobileno'] = row[2]
        d['dob'] = row[3]
        d['password'] = row[4]
        d['otp'] = row[5]
        d['aadhaarno'] = row[6]
        d['photo'] = row[7]
        x.append(d)
    return render(request, 'viewuserprofile.html', {'x': x})

def addcategory(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    return render(request,"addcategory.html")

def insertcategory(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    s = "insert into categorytable values('" + request.GET["catname"] + "','" + request.GET["description"] + "')"

    cr = conn.cursor()
    s1 = "select * from categorytable"

    cr.execute(s1)
    flag = False
    result = cr.fetchall()

    for row in result:
        if row[0] == request.GET["catname"]:
            flag = True
            break

    d = {}
    if flag == True:
        d["message"] = "duplicate category"

    else:
        cr.execute(s)
        conn.commit()
        d["message"] = "category added successfully"

    return render(request, "confirmadmin.html", d)

def viewcategory(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query="select * from categorytable"

    cr=conn.cursor()
    cr.execute(query)

    result=cr.fetchall()
    x=[]
    for row in result:
        d={}
        d["catname"]=row[0]
        d["description"] = row[1]
        x.append(d)

    return render(request,"viewcategory.html",{"data":x})

def removecategory(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    query="delete from categorytable where catname='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(query)
    conn.commit()
    d={"message":"category removed"}
    return render(request,"confirmadmin.html",d)

def editcategory(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    s="select * from categorytable where catname='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(s)
    result=cr.fetchone()

    d={}
    d["catname"]=result[0]
    d["description"] = result[1]

    return render(request, "getcategorydata.html", d)

def savecategory(request):
    if not ("email") in request.session:
        return HttpResponseRedirect("login")

    global conn
    s="update categorytable set description='"+request.GET["description"]+"' where catname='"+request.GET["catname"]+"'"
    cr=conn.cursor()
    cr.execute(s)
    conn.commit()

    d={"message":"category updated"}
    return render(request,"confirmadmin.html",d)

def addroom(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    query = "select * from categorytable"

    cr = conn.cursor()
    cr.execute(query)

    result = cr.fetchall()
    x = []
    for row in result:
        d = {}
        d["catname"] = row[0]
        x.append(d)
    return render(request,"addroom.html",{'x':x})

def insertroom(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    coverphoto =request.FILES['coverphoto']
    photo1 =request.FILES['photo1']
    photo2 =request.FILES['photo2']
    photo3 =request.FILES['photo3']
    photo4 =request.FILES['photo4']

    global conn


    cr = conn.cursor()
    s1 = "select * from roomtable"

    cr.execute(s1)
    flag = False
    result = cr.fetchall()

    for row in result:
        if row[1] == request.POST["title"]:
            flag = True
            break

    d = {}
    if flag == True:
        d["message"] = "duplicate room"

    else:
        fs = FileSystemStorage()
        fileName = fs.save(coverphoto.name, coverphoto)
        fileName1 = fs.save(photo1.name, photo1)
        fileName2 = fs.save(photo2.name, photo2)
        fileName3 = fs.save(photo3.name, photo3)
        fileName4 = fs.save(photo4.name, photo4)
        s = "insert into roomtable values(null,'" + request.POST["title"] + "','" + request.POST["ppd"] + "','" + request.POST["description"] + "','" + fileName + "','" + request.POST["city"] + "','" + request.POST["address"] + "','" + fileName1 + "','" + fileName2 + "','" +  fileName3 + "','" + fileName4 + "','"+request.POST['catname']+"','"+ request.session['useremail'] +"')"

        cr.execute(s)
        conn.commit()
        d["message"] = "room added successfully"

    return render(request, "confirm.html", d)

def viewroom (request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    query = "select * from roomtable"

    cr = conn.cursor()
    cr.execute(query)

    res = cr.fetchall()
    x=[]
    for row in res:
        d={}
        d['roomid']=row[0]
        d['title']=row[1]
        d['priceperday']=row[2]
        d['description']=row[3]
        d['coverphoto']=row[4]
        d['city']=row[5]
        d['address']=row[6]
        d['photo1']=row[7]
        d['photo2']=row[8]
        d['photo3']=row[9]
        d['photo4']=row[10]
        d['catname']=row[11]
        d['email']=row[12]
        x.append(d)
    return render(request,'viewroom.html',{'x':x})


def removeroom(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    query="delete from roomtable where roomid='"+request.GET["q"]+"'"
    cr=conn.cursor()
    cr.execute(query)
    conn.commit()
    d={"message":"room removed"}
    return render(request,"confirm.html",d)

def editroom(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    s="select * from roomtable where roomid='"+request.GET["q"]+"'"

    cr=conn.cursor()
    cr.execute(s)
    result = cr.fetchone()

    d={}

    d['roomid'] = result[0]
    d['title'] = result[1]
    d['priceperday'] = result[2]
    d['description'] = result[3]
    d['coverphoto'] = result[4]
    d['city'] = result[5]
    d['address'] = result[6]
    d['photo1'] = result[7]
    d['photo2'] = result[8]
    d['photo3'] = result[9]
    d['photo4'] = result[10]
    d['catname'] = result[11]
    d['email'] = result[12]


    return render(request, "getroomdata.html", d)

def saveroom(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn

    s="update roomtable set title='"+request.GET["title"]+"' where roomid='"+request.GET["roomid"]+"'"
    s1="update roomtable set priceperday='"+request.GET["ppd"]+"' where roomid='"+request.GET["roomid"]+"'"
    s2="update roomtable set description='"+request.GET["description"]+"' where roomid='"+request.GET["roomid"]+"'"
    s4="update roomtable set city='"+request.GET["city"]+"' where roomid='"+request.GET["roomid"]+"'"
    s5="update roomtable set address='"+request.GET["address"]+"' where roomid='"+request.GET["roomid"]+"'"


    cr=conn.cursor()
    cr.execute(s)
    cr.execute(s1)
    cr.execute(s2)
    cr.execute(s4)
    cr.execute(s5)


    conn.commit()

    d={"message":"Data updated"}
    return render(request,"confirm.html",d)

def editphoto(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    cphoto = request.FILES['coverphotofile']
    id=request.POST['photoid']
    columnname= request.POST['columnname']

    fs = FileSystemStorage()
    filename = fs.save(cphoto.name, cphoto)
    print("kkk " + id+"  "+filename,"  "+columnname)
    if str(columnname) == 'coverphoto':
        s = "update roomtable set coverphoto='" + filename + "' where roomid='" + id + "'"
    if str(columnname) == 'photo1':
        s = "update roomtable set photo1='" + filename + "' where roomid='" + id + "'"
    if str(columnname) == 'photo2':
        s = "update roomtable set photo2='" + filename + "' where roomid='" + id + "'"
    if str(columnname) == 'photo3':
        s = "update roomtable set photo3='" + filename + "' where roomid='" + id + "'"
    if str(columnname) == 'photo4':
        s = "update roomtable set photo4='" + filename + "' where roomid='" + id + "'"
    cr  = conn.cursor()
    cr.execute(s)
    conn.commit()
    return HttpResponse("success")

def searchroom(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    return render(request, "searchroom.html")

def getallcityname(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    query = "select DISTINCT(city) from roomtable order by city"
    r = conn.cursor()
    r.execute(query)
    conn.commit()
    print(query)
    result = r.fetchall()

    x = []
    for p in result:
        print(p[0], ' ----')
        x.append(p[0])
    print(x)
    return JsonResponse(x, safe=False)

@csrf_exempt
def roomsearchaction(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    city = request.POST["city"]
    query = "select * from roomtable where city='" + city + "'"
    r = conn.cursor()
    r.execute(query)
    result = r.fetchall()
    x = []
    for p in result:
        d = {}
        d["roomid"] = p[0]
        d["title"] = p[1]
        d["priceperday"] = p[2]
        d["description"] = p[3]
        d["coverphoto"] = p[4]
        d["email"] = p[12]
        d["city"] = p[5]
        x.append(d)
    return JsonResponse(x, safe=False)

def roomdetail(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")

    global conn
    roomid = request.GET["roomid"]
    query = "select * from roomtable where roomid='" + roomid + "'"
    r = conn.cursor()
    r.execute(query)
    result = r.fetchone()

    x = []
    d = {}
    d["roomid"] = result[0]
    d["title"] = result[1]
    d["priceperday"] = result[2]
    d["description"] = result[3]
    d["coverphoto"] = result[4]
    d["city"] = result[5]
    d["address"] = result[6]
    d["photo1"] = result[7]
    d["photo2"] = result[8]
    d["photo3"] = result[9]
    d["photo4"] = result[10]
    d["catname"] = result[11]
    d["email"] = result[12]

    # x.append(d)

    # for p in result1:
    #     a={}
    #     a["pic"]=p[0]
    #     x.append(a)
    #
    print(d)

    return render(request, "roomdetail.html", d)

def ajax_avg_rating(request):
    roomid = request.GET['roomid']
    conn = connectionfile.ConnectMe('')
    s = "select avg(rate) from rating where roomid='"+str(roomid)+"'"
    cr =conn.cursor()
    cr.execute(s)
    res = cr.fetchall()
    x = []
    rating = res[0][0]
    print(rating)
    return HttpResponse(rating)

def ajax_addrating(request):
    rate = request.GET['rate']
    roomid = request.GET['roomid']
    conn =connectionfile.ConnectMe('')
    cr = conn.cursor()
    s1 = "select * from rating where roomid='"+str(roomid)+"' and useremail='"+request.session['useremail']+"'"
    cr.execute(s1)
    res = cr.fetchall()
    if len(res)<=0:
        s = "insert into rating values (null,'"+str(rate)+"','"+str(roomid)+"','"+request.session['useremail']+"')"
        cr.execute(s)
        conn.commit()
    return HttpResponse(1)


def ratingdemo(request):
    return render(request,'ratingdemo.html')

def bookingpage(request):
    global conn
    roomid = request.GET["roomid"]
    query = "select * from roomtable where roomid='" + roomid + "'"
    r = conn.cursor()
    r.execute(query)
    result = r.fetchone()

    x = []
    d = {}
    d["roomid"] = result[0]
    d["title"] = result[1]
    d["priceperday"] = result[2]
    d["description"] = result[3]
    d["coverphoto"] = result[4]
    d["city"] = result[5]
    d["address"] = result[6]
    d["photo1"] = result[7]
    d["photo2"] = result[8]
    d["photo3"] = result[9]
    d["photo4"] = result[10]
    d["catname"] = result[11]
    d["email"] = result[12]

    print(d)
    return render(request,"bookingpage.html",d)

@csrf_exempt
def bookingaction(request):
    if not ("useremail") in request.session:
        return HttpResponseRedirect("userlogin")
    bookingdate = datetime.now().date()
    global conn
    email = request.session['useremail']
    priceperday = request.POST['priceperday']
    roomid = request.POST["roomid"]
    bookername = request.POST["bookername"]
    mobileno = request.POST["mobileno"]
    noofperson = request.POST["noofperson"]
    totalcost = request.POST["totalcost"]
    fromdate = request.POST["fromdate"]
    todate = request.POST["todate"]
    bookingdate = datetime.now().strftime("%y-%m-%d")
    alldays = request.POST['alldays']
    paymentmode = request.POST['paymentmode'];

    noofdays = alldays.split(',')
    print(noofdays, ' ---------')

    d = {}
    query = "insert into bookingtable  values (null,'" + bookername + "','" + mobileno + "','"+str(roomid)+"','" + str(totalcost) + "','" + str(bookingdate) + "','" + str(email) + "','" + str(noofperson) + "','"+paymentmode+"')"

    print(query)
    r = conn.cursor()
    r.execute(query)
    conn.commit()

    bookingid = r.lastrowid

    for i in range(0, len(noofdays)):
        qr = "insert into bookingdetail values (null," + str(bookingid) + "," + str(roomid) + ",'" + str(
            noofdays[i]) + "','" + str(priceperday) + "')"
        r1 = conn.cursor()
        r1.execute(qr)
        conn.commit()

    d['bookingid'] = bookingid

    msg = "Your room has been booked for the date ("+str(alldays)+"). Your Booking ID is " + str(bookingid)
    msg = msg.replace(" ","%20")
    conn1 = http.client.HTTPConnection("server1.vmm.education")
    conn1.request('GET',
                 "/VMMCloudMessaging/AWS_SMS_Sender?username=monika&password=L78E7CIB&message=" + msg + "&phone_numbers=" + mobileno)
    response = conn1.getresponse()
    print(response.read())

    return JsonResponse(d, safe=False)

def checkavailability(request):
    global conn
    roomid = request.GET["roomid"]
    fromdate = request.GET["fromdate"]
    todate = request.GET["todate"]

    fromdate = datetime.strptime(fromdate, '%m/%d/%Y').strftime('%Y-%m-%d')
    todate = datetime.strptime(todate, '%m/%d/%Y').strftime('%Y-%m-%d')

    qr = "Select * from bookingdetail where date1>='" + str(fromdate) + "' and date1<='" + str(
        todate) + "' and roomid='" + str(roomid) + "'"
    r = conn.cursor()
    r.execute(qr)
    res = r.fetchall()
    d = {}
    if len(res) > 0:
        d['error_date'] = '1'
    else:
        d['error_date'] = '2'
    return JsonResponse(d, safe=False)

def confirmbooking(request):
    global conn
    bookingid = request.GET["bookingid"]
    query = "select bookingtable.id,bookingtable.email,bookingtable.bookername,bookingtable.mobileno,bookingtable.noofpersons,bookingtable.totalcost,roomtable.roomid,roomtable.title from bookingtable INNER JOIN roomtable on bookingtable.roomid=roomtable.roomid where bookingtable.id='" + str(bookingid) + "'"
    print(query)
    r = conn.cursor()
    r.execute(query)
    result = r.fetchone()
    print(result)

    d = {}
    d["bid"] = result[0]
    d["email"] = result[1]
    d["name"] = result[2]
    d["mobileno"] = result[3]
    d["noofperson"] = result[4]
    d["totalcost"] = result[5]
    d["roomid"] = result[6]
    d["title"] = result[7]

    return render(request, "confirmbooking.html", d)

def mybooking(request):
    global conn
    email = request.session['useremail']
    cr = conn.cursor()
    s = "select bookingid,bookername,mobileno, GROUP_CONCAT(date1) dates,totalcost,title,bookingdate FROM bookingtable bt JOIN bookingdetail bd ON (bt.id = bd.bookingid) JOIN roomtable ON (bd.roomid=roomtable.roomid) where bt.email='"+email+"' GROUP BY bookingid"
    cr.execute(s)
    res = cr.fetchall()
    x = []
    for row in res:
        d = {}
        d['bookingid'] = row[0]
        d['bookername'] = row[1]
        d['mobileno'] = row[2]
        d['date'] = row[3]
        d['amount'] = row[4]
        d['title'] = row[5]
        d['bookingdate'] = row[6]
        x.append(d)
    return render(request,'mybooking.html',{'x':x})

@csrf_exempt
def addReview(request):
    roomid = request.POST['roomid']
    review = request.POST['review']
    dt  =datetime.today().date()
    useremail = request.session['useremail']
    conn = connectionfile.ConnectMe('')
    cr = conn.cursor()
    s1 = "select * from reviews where roomid='"+str(roomid)+"' and useremail='"+useremail+"'"
    cr.execute(s1)
    res = cr.fetchall()
    if len(res)>0:
        d = {'error':1}
        return JsonResponse(d,safe=False)
    else:
        s = "insert into reviews values (null,'"+review+"','"+str(roomid)+"','"+useremail+"','"+str(dt)+"')"
        cr.execute(s)
        conn.commit()
        conn.close()
        d = {'error': 2}
        return JsonResponse(d, safe=False)

def showReviews(request):
    roomid = request.GET['roomid']
    conn = connectionfile.ConnectMe('')
    s = "select * from reviews where roomid='"+str(roomid)+"' order by id DESC"
    cr = conn.cursor()
    cr.execute(s)
    res = cr.fetchall()
    conn.close()
    x = []
    for row in res:
        d = {}
        d['id'] = row[0]
        d['review'] = row[1]
        d['useremail'] = row[3]
        d['dateofreview'] = row[4]
        x.append(d)
    return JsonResponse(x,safe=False)

@csrf_exempt
def feedback(request):
    global conn
    s = "insert into feedback values('" + request.POST["name"] + "','" + request.POST["email"] + "','" + request.POST[
        "Message"] + "')"

    cr = conn.cursor()
    cr.execute(s)
    conn.commit()
    d={}
    d["message"] = "THANKS FOR YOUR FEEDBACK"

    return render(request, "confirm.html", d)