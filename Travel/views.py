from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

# Create your views here.
from django.urls import reverse

from Travel.forms import UserForm
from Travel.models import City, CartInfo, Custom, Guestbook

'''首页'''


def index(request):
    return render(request, 'Travel/index.html')


# 注册
def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            pwd = uf.cleaned_data['pwd']
            user_name = uf.cleaned_data['user_name']
            ulist = User.objects.filter(username=user_name)
            if ulist:
                return render(request, 'Travel/resgister.html',
                              {'message': 'username already exist', 'user_name': user_name})
            else:
                User.objects.create_user(username=user_name, password=pwd)
                return render(request, 'Travel/login.html')

    else:
        uf = UserForm()
        return render(request, 'Travel/register.html', {'uf': uf})


# 登录
def login(request):
    # 实现登陆功能，返回user
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        # 用户验证
        user_result = auth.authenticate(username=user_name, password=pwd)

        # url_from = request.session.get('from')
        # if url_from:
        #     if user_result is not None:
        #         # 用户登陆
        #         auth.login(request, user_result)
        #         del request.session['from']
        #         return redirect(url_from)
        #     else:
        #         return render(request, 'Travel/register.html', {'login_error': 'username or password wrong'})
        # else:
        #     return render(request, 'Travel/index.html', {'user': user_result})

        url_from = request.session.get('from')
        if user_result is not None:
            # 用户登陆
            auth.login(request, user_result)
            if url_from:
                del request.session['from']
                return redirect(url_from)
            else:
                return render(request, 'Travel/index.html', {'user': user_result})
        else:
            return render(request, 'Travel/login.html', {'login_error': 'username or password wrong'})
    else:
        # 访问登陆页面
        return render(request, 'Travel/login.html', {'login_error': 'username or password wrong'})


# 退出
def logout(request):
    auth.logout(request)
    # return render(request, 'Travel/index.html')
    return redirect('Travel:index')


'''测试'''
# def test(request):
#     return render(request, 'Travel/test.html')
#
#
# def test2(request):
#     return render(request, 'Travel/分页.html')
'''国外'''


def foreign(request):
    return render(request, 'Travel/foreign.html')


'''国内'''


def inland(request):
    return render(request, 'Travel/inland.html')


'''高级定制'''


def custom(request):
    uid = request.user.id
    print(uid)
    uname = request.user.username
    print(uname)
    if uid:
        return render(request, 'Travel/custom.html', {'uname': uname})
    else:
        return redirect('Travel:login')


def custom_add(request):
    uid = request.user.id
    if uid:
        cf_city = request.POST.get('cf_city')
        dd_city = request.POST.get('dd_city')
        cf_date = request.POST.get('cf_date')
        travel_days = request.POST.get('travel_days')
        travel_adult = request.POST.get('travel_adult')
        travel_children = request.POST.get('travel_children')
        name = request.POST.get('name')
        number = request.POST.get('number')
        content = request.POST.get('content')
        res = Custom(cf_city=cf_city, dd_city=dd_city, cf_date=cf_date, travel_days=travel_days,
                     travel_adult=travel_adult,
                     travel_children=travel_children, name=name, number=number, content=content, user_id=uid)
        res.save()

        # return HttpResponse('恭喜定制成功！稍后会有客服跟您联系。')
        # return redirect('Travel:custom')
        return render(request, 'Travel/custom.html')
    else:
        return redirect('Travel:login')


'''介绍'''


def introduce(request):
    return render(request, 'Travel/introduce.html')


'''详情页'''


def detail(request, id):
    detail = City.objects.get(id=id)
    return render(request, 'Travel/detail.html', {'detail': detail})


'''我的订单'''


def myorder(request):
    uid = request.user.id
    if uid:
        carts = CartInfo.objects.filter(user_id=uid)
        id = User.objects.get(id=uid)
        prices = 0
        num = 0
        for i in carts:
            prices = int(i.travel_count) * int(i.goods.price + prices)
            num = num + 1
        return render(request, 'Travel/myorder.html', locals())
    else:
        return redirect('Travel:login')


'''增加预约'''


def add(request, cid):
    # 获取来源页面地址
    url_from = request.META.get('HTTP_REFERER')
    request.session['from'] = url_from

    uid = request.user.id
    if uid:
        travel_count = request.GET.get('travel_count')
        travel_city = request.GET.get('travel_city')
        travel_data = request.GET.get('travel_data')
        travel_number = request.GET.get('travel_number')
        res = CartInfo(travel_count=travel_count, travel_city=travel_city, travel_data=travel_data,
                       travel_number=travel_number, user_id=uid, goods_id=cid)
        res.save()
        return redirect('Travel:myorder')
    else:
        return redirect('Travel:login')


'''修改预约'''


def compile(request, id):
    gid = CartInfo.objects.get(id=id)
    if request.method == 'POST':
        travel_count = request.POST.get('travel_count')
        travel_city = request.POST.get('travel_city')
        travel_data = request.POST.get('travel_data')
        travel_number = request.POST.get('travel_number')
        gid.travel_count = travel_count
        gid.travel_city = travel_city
        gid.travel_data = travel_data
        gid.travel_number = travel_number
        gid.save()
        return redirect('Travel:myorder')
    else:
        return render(request, 'Travel/compile.html', {'gid': gid})


'''删除预约订单'''


def delete(request, gid):
    cart = CartInfo.objects.get(id=int(gid))
    cart.delete()
    return redirect('Travel:myorder')


'''留言'''


def show_guestbook(request):
    guestbooks = Guestbook.objects.all()
    return render(request, 'Travel/guestbook.html', {'guestbooks': guestbooks})


def ask_guestbook(request):
    uid = request.user.id
    if uid:
        if request.method == 'POST':
            title = request.POST.get('title')
            titles = Guestbook(title=title, content='', user_id=uid)
            titles.save()
            return redirect('Travel:show_guestbook')
    else:
        return redirect('Travel:login')


def answer_guestbook(request, id):
    id = Guestbook.objects.get(id=id)
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer == '':
            return redirect('Travel:show_guestbook')
        else:
            id.content = answer
            id.save()
            return redirect('Travel:show_guestbook')
    else:
        return render(request, 'Travel/answer_guestbook.html', {'id': id})


'''个人中心'''


def personal(request):
    uid = request.user.id
    if uid:
        carts = CartInfo.objects.filter(user_id=uid)
        return render(request, 'Travel/personal.html', {'carts': carts})


'''----------------国内城市-----------------'''


def city_yn2(request):
    city = City.objects.filter(title__contains='云南').order_by('price')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city2.html', {'citys': citys})
def city_yn3(request):
    city = City.objects.filter(title__contains='云南').order_by('-price')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city3.html', {'citys': citys})

def city_yn(request):
    city = City.objects.filter(title__contains='云南')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_xzcy(request):
    city = City.objects.filter(title__contains='西藏川渝')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_gz(request):
    city = City.objects.filter(title__contains='贵州')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_db(request):
    # citys = City.objects.filter(title__contains='洛阳')
    city = City.objects.filter(title__contains='长白山')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_nmhn(request):
    city = City.objects.filter(title__contains='河南')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)

    return render(request, 'Travel/city.html', {'citys': citys})


def city_xb(request):
    city = City.objects.filter(title__contains='西北')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_xa(request):
    city = City.objects.filter(title__contains='西安')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_jzhy(request):
    city = City.objects.filter(title__contains='江浙沪皖')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_bj(request):
    city = City.objects.filter(title__contains='北京')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_sdsx(request):
    city = City.objects.filter(title__contains='山东山西')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_jxfj(request):
    city = City.objects.filter(title__contains='江西福建')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_sy(request):
    city = City.objects.filter(title__contains='三亚')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_hbhn(request):
    city = City.objects.filter(title__contains='湖北湖南')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_gd(request):
    city = City.objects.filter(title__contains='广东')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_gx(request):
    city = City.objects.filter(title__contains='广西')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def city_xgam(request):
    city = City.objects.filter(title__contains='香港澳门')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


'''--------------------国外城市-----------------'''


def country_uk(request):
    city = City.objects.filter(title__contains='英国')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_france(request):
    city = City.objects.filter(title__contains='法国意大利')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_southafrican(request):
    city = City.objects.filter(title__contains='南非')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_thai(request):
    city = City.objects.filter(title__contains='泰国')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_singapore(request):
    city = City.objects.filter(title__contains='新加坡')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_roundtheworld(request):
    city = City.objects.filter(title__contains='环球')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_usa(request):
    city = City.objects.filter(title__contains='美国')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_hawaiyi(request):
    city = City.objects.filter(title__contains='夏威夷')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_dubai(request):
    city = City.objects.filter(title__contains='迪拜')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_egypt(request):
    city = City.objects.filter(title__contains='埃及')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_tokyo(request):
    city = City.objects.filter(title__contains='东京')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_japan(request):
    city = City.objects.filter(title__contains='日本')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_south(request):
    city = City.objects.filter(title__contains='南极')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_north(request):
    city = City.objects.filter(title__contains='北极')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_australia(request):
    city = City.objects.filter(title__contains='澳大利亚')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_newzealand(request):
    city = City.objects.filter(title__contains='新西兰')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_maldivees(request):
    city = City.objects.filter(title__contains='马尔代夫')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


def country_fiji(request):
    city = City.objects.filter(title__contains='斐济')
    book_list = []
    '''
    数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    '''
    for x in city:
        book_list.append(x)

    # 将数据按照规定每页显示 5 条, 进行分割
    paginator = Paginator(book_list, 5)

    if request.method == "GET":
        # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
        page = request.GET.get('page')
        try:
            citys = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            citys = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            citys = paginator.page(paginator.num_pages)
    return render(request, 'Travel/city.html', {'citys': citys})


# ----------------------------------------------------后台管理---------------------------------------------

def manage_base(request):
    username = request.user.username
    if username:
        return render(request, 'Travel/manage/manage_base.html', {'username': username})


def manage_index(request):
    username = request.user.username
    if username:
        return render(request, 'Travel/manage/manage_index.html',{'username': username})


def add_user(request):
    username = request.user.username
    if username:
        if request.method == 'POST':
            uf = UserForm(request.POST)
            if uf.is_valid():
                pwd = uf.cleaned_data['pwd']
                user_name = uf.cleaned_data['user_name']
                ulist = User.objects.filter(username=user_name)
                if ulist:
                    return render(request, 'Travel/manage/add_user.html', {'message': 'username already exist','username': username})
                else:
                    User.objects.create_user(username=user_name, password=pwd)
                    return render(request, 'Travel/manage/add_user.html', {'message': 'Regist successfully !!','username': username})
        else:
            uf = UserForm()
            return render(request, 'Travel/manage/add_user.html', {'uf': uf,'username': username})


def show_user(request):
    username = request.user.username
    if username:
        user = User.objects.all()
        return render(request, 'Travel/manage/del_user.html', {'user': user,'username': username})


def del_user(request, user_id):
    username = request.user.username
    if username:
        users = User.objects.get(id=int(user_id))
        users.delete()
        return redirect('Travel:show_user')


def show_citys(request):
    username = request.user.username
    if username:
        city = City.objects.all()
        book_list = []
        '''
        数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
        '''
        for x in city:
            book_list.append(x)

        # 将数据按照规定每页显示 5 条, 进行分割
        paginator = Paginator(book_list, 8)

        if request.method == "GET":
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page')
            try:
                citys = paginator.page(page)
            # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                citys = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                citys = paginator.page(paginator.num_pages)
        return render(request, 'Travel/manage/update_citys.html', {'citys': citys,'username': username})


def update(request, id):
    username = request.user.username
    if username:
        cid = City.objects.get(id=id)
        if request.method == 'POST':
            title = request.POST.get('title')
            price = request.POST.get('price')
            name1 = request.POST.get('name1')
            name2 = request.POST.get('name2')
            name3 = request.POST.get('name3')
            cid.title = title
            cid.price = price
            cid.name1 = name1
            cid.name2 = name2
            cid.name3 = name3
            cid.save()
            return redirect('Travel:show_citys')
        else:
            return render(request, 'Travel/manage/update.html', {'cid': cid,'username':username})


def del_citys(request, id):
    cid = City.objects.get(id=int(id))
    cid.delete()
    return redirect('Travel:show_citys')


def look_user(request):
    username = request.user.username
    if username:
        look = CartInfo.objects.all()
        return render(request, 'Travel/manage/look_user.html', {'look': look,'username':username})


def del_look(request, id):
    lid = CartInfo.objects.get(id=int(id))
    lid.delete()
    return redirect('Travel:look_user')


def look_message(request):
    username = request.user.username
    if username:
        message = Guestbook.objects.all()
        return render(request, 'Travel/manage/look_message.html', {'message': message,'username':username})


def del_message(request, id):
    cid = Guestbook.objects.get(id=int(id))
    cid.delete()
    return redirect('Travel:look_message')
