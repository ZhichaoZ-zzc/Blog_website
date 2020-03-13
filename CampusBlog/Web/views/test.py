"""
权限管理测试
第一步：获取用户的所有角色
第二步：获取角色所对应的所有权限
第三步：将增删改查放到权限表中
第四步：在叶子节点显示菜单列表
第五步：获取所有的菜单列表
"""
from django.shortcuts import render,redirect,HttpResponse
from repository import models
import re

class MenuHelper(object):

    def __init__(self,request,username):

        self.request =request
        self.username =username
        self.current_url = request.path_info

        self.permission2action_dict = None
        self.menu_leaf_list = None
        self.menu_list = None


        self.session_data()


    def session_data(self):
        permission_dict = self.request.session.get('permission_info')

        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']


        else:
            role_list = models.Role.objects.filter(user2role__u__username=self.username)
            #print(role_list)#<QuerySet [<Role: CEO>, <Role: CTO>]>

            permission2action_list = models.Permission2Action.objects.\
                filter(permission2action2role__r__in=role_list).\
                values('p__url','a__code').distinct()
            #print(permission2action_list)  #<QuerySet [{'p__url': 'yonghu.html', 'a__code': 'get'}, {'p__url': 'yonghu.html', 'a__code': 'delete'}, {'p__url': 'guliang.html', 'a__code': 'delete'}, {'p__url': 'dingdan.html', 'a__code': 'put'}]>


            permission2action_dict ={}
            for item in permission2action_list:
                if item['p__url'] in permission2action_dict:
                    permission2action_dict[item['p__url']].append(item['a__code'])
                else:
                    permission2action_dict[item['p__url']] =[item['a__code']]

            #print(permission2action_dict)  #{'yonghu.html': ['get', 'delete'], 'guliang.html': ['delete'], 'dingdan.html': ['put']}

            menu_leaf_list = list(models.Permission2Action.objects.\
                                  filter(permission2action2role__r__in=role_list).exclude(p__menu__isnull=True).\
                                  values('p_id','p__url','p__caption','p__menu').distinct())

            #print(menu_leaf_list)  #[{'p_id': 1, 'p__url': 'yonghu.html', 'p__caption': '用户管理', 'p__menu': 5}, {'p_id': 3, 'p__url': 'guliang.html', 'p__caption': '菇凉管理', 'p__menu': 4}, {'p_id': 2, 'p__url': 'dingdan.html', 'p__caption': '订单管理', 'p__menu': 6}]

            menu_list = list(models.Menu.objects.values('id','caption','parent_id'))
            #print(menu_list) #[{'id': 2, 'caption': '学校管理', 'parent_id': None}, {'id': 3, 'caption': '学校2管理', 'parent_id': None}, {'id': 4, 'caption': '学校三管理', 'parent_id': None}, {'id': 5, 'caption': '学院管理', 'parent_id': 2}, {'id': 6, 'caption': '学院2管理', 'parent_id': 3}, {'id': 7, 'caption': '学院三管理', 'parent_id': 4}]


            self.request.session['permission_info'] ={
                'permission2action_dict':permission2action_dict,
                'menu_leaf_list':menu_leaf_list,
                'menu_list':menu_list
            }

    def actions(self):
        action_list = []

        for k,v in self.permission2action_dict.items():
            # print(k,v)
            # print(self.current_url)
           # if re.match(k,self.current_url):
            action_list =v
                #break
            return action_list

    def menu_content(self,child_list):
        response = ""
        tpl = """
            <div class="item %s">
                <div class="title">%s</div>
                <div class="content">%s</div>
            </div>
        """
        for row in child_list:
            if not row['status']:
                continue
            active = ""
            if row['open']:
                active = "active"
            if 'url' in row:
                response += "<a class='%s' href='%s'>%s</a>" % (active, row['url'], row['caption'])
            else:
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl % (active, title, content)
        return response

    def menu_data_list(self):
        menu_leaf_dict = {}
        open_leaf_parent_id = None

        for item in self.menu_leaf_list:
            item = {
                'id':item['p_id'],
                'url':item['p__url'],
                'caption':item['p__caption'],
                'parent_id':item['p__menu'],
                'child':[],
                'status':True,
                'open':False
            }
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append(item)
            else:
                menu_leaf_dict[item['parent_id']] = [item, ]

            if re.match(item['url'], self.current_url):
                item['open'] = True
                open_leaf_parent_id = item['parent_id']

            menu_dict = {}
            for item in self.menu_list:
                item['child'] = []
                item['status'] = False
                item['open'] = False
                menu_dict[item['id']] = item

           # print(self.menu_list)

            for k, v in menu_leaf_dict.items():
                menu_dict[k]['child'] = v
                parent_id = k
                # 将后代中有叶子节点的菜单标记为【显示】
                while parent_id:
                    menu_dict[parent_id]['status'] = True
                    parent_id = menu_dict[parent_id]['parent_id']

            while open_leaf_parent_id:
                menu_dict[open_leaf_parent_id]['open'] = True
                open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parent_id']

            # 生成树形结构数据
            result = []
            for row in menu_dict.values():
                if not row['parent_id']:
                    result.append(row)
                else:
                    menu_dict[row['parent_id']]['child'].append(row)

            return result


    def menu_tree(self):
        response = ""
        tpl = """
        <div class="item %s">
            <div class="title">%s</div>
            <div class="content">%s</div>
        </div>
        """
        for row in self.menu_data_list():  # 构造成树形结构
            if not row['status']:
                continue
            active = ""
            if row['open']:
                active = "active"
            # 第一层第一个
            title = row['caption']
            # 第一层第一个的后代
            content = self.menu_content(row['child'])
            response += tpl % (active, title, content)
        return response





def login(request):
    if request.method =='GET':
        return render(request,'test/login.html')

    else:
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        obj = models.User.objects.filter(username=username,password=pwd).first()

        if obj:
            request.session['user_info'] = {'nid':obj.id,'username':obj.username}

            MenuHelper(request,obj.username)
            return redirect('yonghu.html')
        else:
            return redirect('test.html')


def permission(func):
    def inner(request,*args,**kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('test.html')

        obj = MenuHelper(request,user_info['username'])

        action_list = obj.actions()
        if not action_list:
            return HttpResponse('无权限访问')
        kwargs['menu_string'] = obj.menu_tree()
        kwargs['action_list'] =action_list
        return func(request, *args, **kwargs)

    return inner



@permission
def index(request,*args,**kwargs):
    action_list = kwargs.get('action_list')
    menu_string = kwargs.get('menu_string')
    if "GET" in action_list:
        result = models.User.objects.all()
    else:
        result = []
    return render(request, 'test/index.html', {'menu_string': menu_string, 'action_list': action_list})








