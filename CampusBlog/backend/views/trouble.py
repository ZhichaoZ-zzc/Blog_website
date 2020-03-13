import datetime
from repository import models
from django.shortcuts import render,redirect,HttpResponse
from ..forms.troublemarker import  TroubleMaker,TroubleKill


def trouble_list(request):
    """
    显示问题
    :param request:
    :return:
    """
    current_user_id = 1
    result = models.Trouble.objects.filter(user_id=current_user_id).order_by('status'). \
        only('title', 'status', 'ctime', 'processer')
    return render(request, 'trouble/backend_trouble_list.html', {'result': result})



def trouble_create(request):
    """
     问题创建
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = TroubleMaker()
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            dic = {}
            dic['user_id'] = 1  # session中获取  当前用户id
            dic['ctime'] = datetime.datetime.now()
            dic['status'] = 1  # 未处理
            dic.update(form.cleaned_data)  # 将传过来的值添加在dic里
            models.Trouble.objects.create(**dic)  # 创建报账单
            return redirect('/backend/trouble-list.html')
    return render(request, 'trouble/backend_trouble_create.html', {'form': form})


def trouble_edit(request,nid):
    """
    编辑问题
    :param request:
    :param nid:
    :return:
    """
    if request.method == "GET":  # status=1  未处理时才能编辑
        obj = models.Trouble.objects.filter(id=nid, status=1).only('id', 'title', 'detail').first()
        if not obj:
            return HttpResponse('已处理中的保单章无法修改..')

        form = TroubleMaker(initial={'title': obj.title, 'detail': obj.detail})
        return render(request, 'trouble/backend_trouble_edit.html', {'form': form, 'nid': nid})

    else:
        form = TroubleMaker(data=request.POST)
        if form.is_valid():
            # v受影响的行数   更新了几行数据 v就是几
            v = models.Trouble.objects.filter(id=nid, status=1).update(**form.cleaned_data)
            if not v:
                return HttpResponse('已经被处理')
            else:
                return redirect('/backend/trouble-list.html')
        return render(request, 'backend_trouble_edit.html', {'form': form, 'nid': nid})


def trouble_kill_list(request):
    """
    显示问题
    :param request:
    :return:
    """
    from django.db.models import Q
    current_user_id = 1
    result = models.Trouble.objects.filter(Q(processer_id=current_user_id)|Q(status=1)).order_by('status')
    return render(request,'trouble/backend_trouble_kill_list.html',{'result':result})



def trouble_kill(request,nid):
    """
    处理问题
    :param request:
    :param nid:
    :return:
    """
    current_user_id = 1
    if request.method == 'GET':
        ret = models.Trouble.objects.filter(id=nid, processer=current_user_id).count()

        if not ret:
            v = models.Trouble.objects.filter(id=nid, status=1).update(processer=current_user_id, status=2)
            if not v:
                return HttpResponse('手速太慢...')

        obj = models.Trouble.objects.filter(id=nid).first()

        form = TroubleKill(initial={'title': obj.title, 'solution': obj.solution})
        return render(request, 'trouble/backend_trouble_kill.html', {'obj': obj, 'form': form, 'nid': nid})
    else:
        ret = models.Trouble.objects.filter(id=nid, processer=current_user_id, status=2).count()
        if not ret:
            return HttpResponse('个人信息错误')
        form = TroubleKill(request.POST)
        if form.is_valid():
            # 更新订单内容
            dic = {}
            dic['status'] = 3
            dic['solution'] = form.cleaned_data['solution']
            dic['ptime'] = datetime.datetime.now()
            models.Trouble.objects.filter(id=nid, processer=current_user_id, status=2).update(**dic)
            return redirect('/backend/trouble-kill-list.html')
        obj = models.Trouble.objects.filter(id=nid).first()
        return render(request, 'trouble/backend_trouble_kill.html', {'obj': obj, 'form': form, 'nid': nid})




