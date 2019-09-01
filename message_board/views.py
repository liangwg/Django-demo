from . import models
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from random import choice

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
    return render(request, "homePage.html")
def read(request):
    quote = choice(quotes)
    allPost = models.Post.objects.all().filter(enable=True).order_by('-time')[:30]

    ans=allPost
    try:
        cate=request.GET['category']
        ans = models.Post.objects.all().filter(enable=True).order_by('-time').filter(category=cate)[:30]
    except:
        pass
    return render(request, "readMessage.html", {"allPost":ans,"quote":quote})


def dele(request, id):
    quote = choice(quotes)
    postToDele = models.Post.objects.get(pk=id)
    try:
        pwd = request.GET['pwd']
        if pwd == postToDele.del_pwd:
            postToDele.delete()
            ans = "删除成功"
        else:
            ans = "密码错误"
    except:
        ans = "请输入正确的密码"
    return render(request, "deleMessage.html", {"postToDele": postToDele, "answer": ans,"quote":quote})