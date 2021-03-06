from . import models, forms
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from random import choice
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth import authenticate  # 用户验证
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


quotes = ['真理惟一可靠的标准就是永远自相符合。 —— 欧文',
          '忠诚可以简练地定义为对不可能的情况的一种不合逻辑的信仰。 —— 门肯',
          '时间是一切财富中最宝贵的财富。 —— 德奥弗拉斯多',
          '这世界要是没有爱情，它在我们心中还会有什么意义！这就如一盏没有亮光的走马灯。 —— 歌德',
          '我读的书愈多，就愈亲近世界，愈明了生活的意义，愈觉得生活的重要。 —— 高尔基',
          '理想是人生的太阳。 —— 德莱赛',
          '把时间用在思考上是最能节省时间的事情。 —— 卡曾斯',
          '科学是到处为家的，不过，在任何不播种的地方，是决不会得到丰收的。 —— 赫尔岑',
          '成功的秘诀，在永不改变既定的目的。 —— 卢梭',
          '文明就是要造成有修养的人。 —— 罗斯金']


def sendEmail(name, email, work, message):
    server = "smtp.163.com"
    sender = "zouhanzhang666@163.com"
    pwd = "Zouhan0903"
    text = MIMEText(name + ' : ' + email + ' : ' + work + ' : ' + message)
    text["Subject"] = "网友留言"
    text["from"] = sender
    mailServer = smtplib.SMTP(server, 25)  # 25为端口号
    mailServer.login(sender, pwd)
    mailServer.sendmail(sender, ["zouhanzhang666@163.com"], text.as_string())
    mailServer.quit()


def write(request):
    quote = choice(quotes)

    try:
        anickname = request.GET['nick_name']
        acategory = request.GET['category']
        amessage = request.GET['message']
        adel_pwd = request.GET['del_pwd']
        post = models.Post.objects.create(nickname=anickname, category=acategory, message=amessage, del_pwd=adel_pwd)
        post.save()
        ans = '发帖成功'
    except:
        ans = '请输入所有信息'
    return render(request, 'writeMessage.html', {"answer": ans, "quote": quote})


def homePage(request):
    quote = choice(quotes)
    if request.user.is_authenticated:
        username = request.user.username
    messages.get_messages(request)
    return render(request, "homePage.html", locals())

def lol(request):
    return render(request,"lolView.html")

def read(request):
    quote = choice(quotes)
    allPost = models.Post.objects.all().filter(enable=True).order_by('-time')
    allPost = allPost[:30]
    if request.user.is_authenticated:
        username = request.user.username
    messages.get_messages(request)
    try:
        cate = request.GET['category']
        allPost = models.Post.objects.all().filter(enable=True).order_by('-time').filter(category=cate)[:30]
    except:
        pass
    return render(request, "readMessage.html", locals())


def dele(request, id):
    quote = choice(quotes)
    postToDele = models.Post.objects.get(pk=id)
    if request.user.is_authenticated:
        username = request.user.username
    try:
        pwd = request.GET['pwd']
        if pwd == postToDele.del_pwd:
            postToDele.delete()
            ans = "删除成功"
        else:
            ans = "密码错误"
    except:
        ans = "请输入正确的密码"
    return render(request, "deleMessage.html", locals())


def contact(request):  # 发邮件到站主邮箱
    ans = None
    if request.user.is_authenticated:
        username = request.user.username
    quote = choice(quotes)
    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():  # 检查窗口正确性
            ans = "感谢您的建议，已将建议内容发送到站主邮箱。"
            name = form.cleaned_data['user_name']
            work = form.cleaned_data['user_work']
            email = form.cleaned_data['user_email']
            message = form.cleaned_data['user_message']
            try:
                sendEmail(name, email, work, message)
            except:
                ans = "出错啦！邮件发送失败，建议您手动将建议发送给zouhanzhang666@163.com"
        else:
            ans = "请输入完整信息"
    else:
        form = forms.ContactForm()
    return render(request, 'contact.html', locals())


def login(request):
    quote = choice(quotes)
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            entername = request.POST['username']
            enterpassword = request.POST['password']
            user = authenticate(username=entername, password=enterpassword)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, '登录成功')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '账号未启用')
            else:
                messages.add_message(request, messages.WARNING, '登陆失败,请确认账户密码正确')
        else:
            messages.add_message(request, messages.INFO, '请输入完整有效的信息')

    else:
        login_form = forms.LoginForm()
    return render(request, "login.html", locals())


def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "退出登录成功")
    return redirect("/login/")


@login_required(login_url='/login/')
def userinfo(request):
    quote = choice(quotes)
    if request.user.is_authenticated:
        username = request.user.username
    user = User.objects.get(username=username)
    try:
        profile = models.Profile.objects.get(user=user)
    except:
        profile = models.Profile(user=user)  # 如果数据库里没有就重新建一个
    if request.method=="POST":
        profile_form=forms.ProfileForm(request.POST,instance=profile)
        if profile_form.is_valid():
            messages.add_message(request,messages.INFO,"个人资料已储存")
            profile_form.save()
            return HttpResponseRedirect('../userinfo/')
        else:
            messages.add_message(request,messages.INFO,'请填入完整信息')
    else:
        profile_form=forms.ProfileForm()
    return render(request, 'userinfo.html', locals())


import smtplib
import apscheduler.schedulers.background
from email.mime.text import MIMEText
import urllib.request
import gzip
import json
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET


def sendEmail(header, mess, weather, high, low):
    server = "smtp.163.com"
    sender = "zouhanzhang666@163.com"
    pwd = "Zouhan0903"
    add = "（本邮件由雯雯专属天气助手发送，当天气条件较差时会自动触发，回复 我是憨憨 & I Love ZHZ 可退订本服务）"
    text = MIMEText(mess + '\n\n' + '今日天气:' + weather + '\n' + high + '\n' + low + '\n\n\n\n' + add)
    text["Subject"] = header
    text["from"] = sender
    mailServer = smtplib.SMTP(server, 25)  # 25为端口号
    mailServer.login(sender, pwd)
    mailServer.sendmail(sender, ["zouhanzhang666@163.com", "1453196338@qq.com", ], text.as_string())
    mailServer.quit()


# "1623005735@qq.com"
# 实例化调度器


# 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记 'cron', day_of_week='mon-fri', hour='20', minute='55', second='10'
# ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
scheduler=apscheduler.schedulers.background.BackgroundScheduler()

@scheduler.scheduled_job('cron',hour=15,minute=18)
def wenwen():
    city_name = '环翠区'
    type = 0
    mess = ""
    url1 = 'http://wthrcdn.etouch.cn/WeatherApi?city=' + urllib.parse.quote(city_name)
    weather_data = urllib.request.urlopen(url1).read()
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    print(weather_data)
    tree = ET.fromstring(weather_data)
    接口消息 = parseString(weather_data)
    今天 = 接口消息.getElementsByTagName('weather')[0]
    天气 = 今天.getElementsByTagName("type")[0]
    高温 = 今天.getElementsByTagName("high")[0]
    低温 = 今天.getElementsByTagName("low")[0]
    指数 = 接口消息.getElementsByTagName('zhishu')
    for 类别 in 指数:
        detail = 类别.getElementsByTagName("detail")[0]
        name = 类别.getElementsByTagName("name")[0]
        value = 类别.getElementsByTagName('value')[0]
        if name.firstChild.data == '雨伞指数' and value.firstChild.data == '带伞':
            mess = detail.firstChild.data
            header = "带伞警告！"
            type = 1
        elif name.firstChild.data == '感冒指数' and value.firstChild.data == '极易发':
            mess = detail.firstChild.data
            header = "防感冒警告"
            type = 2
    if type == 1 or type == 2:
        sendEmail(header, str(mess), str(天气.firstChild.data), str(高温.firstChild.data), str(低温.firstChild.data))
    if type==0:
        sendEmail("hh","jj","jj","oo","pp")

scheduler.start()
