from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from board.models import Board, Command, Tag
from users.models import User
from users.views import ID_REPOSITORY, check_blank, read_image, get_base


def get_user(request):
    return ID_REPOSITORY.get(request.COOKIES.get('id'))


def get_tag(request: WSGIRequest, tag: str):
    tags = set()
    if tag:
        if not tag.strip().startswith("#"):
            messages.error(request, "태그가 형태가 일치하지 않습니다.")
            return None
        for i in set([s.strip().lower().replace(" ", "_") for s in tag.split("#")]):
            if not i:
                pass
            elif len(Tag.objects.filter(tag_name=i).all()) == 0:
                tags.add(Tag.objects.create(tag_name=i))
            else:
                tags.add(Tag.objects.get(tag_name=i))
        return tags
    else:
        return tags


class Main(View):  #
    def get(self, request):
        return render(request, 'index.html')


# Create your views here.
class ListBoard(View):  # boards/   boards
    def get(self, request):
        page = request.GET.get('page', 1)
        sort = request.GET.get('sort', 'create_date_new')
        search = request.GET.get('search', '')
        username_search = request.GET.get('username_search', '')
        sort_list = [
            {'create_date_new': {"name": '최신 생성일 순', 'check': sort == 'create_date_new'}},
            {'create_date_old': {"name": '오래된 생성일 순', 'check': sort == 'create_date_old'}},
            {'good': {"name": '좋아요 내림차 순', 'check': sort == 'good'}},
            {'good_reverse': {"name": '좋아요 오름차 순', 'check': sort == 'good_reverse'}},
            {'look': {"name": '조회수 내림차 순', 'check': sort == 'look'}},
            {'look_reverse': {"name": '조회수 오름차 순', 'check': sort == 'look_reverse'}}
        ]

        user = get_user(request)
        content = {'now_page': page,
                   'now_sort': sort,
                   'now_search': search,
                   'sort_list': sort_list,
                   'now_username_search': username_search,
                   }
        if user is not None:
            content["username"] = user.username

        boards = Board.objects.filter(title__icontains=search).filter(username__icontains=username_search)

        if sort == 'create_date_new':
            board_list = boards.order_by('-create_date')
        elif sort == 'create_date_old':
            board_list = boards.order_by('create_date')
        elif sort == 'good':
            board_list = boards.order_by('-good_count')
        elif sort == 'look':
            board_list = boards.order_by('-visit')
        elif sort == 'look-revers':
            board_list = boards.order_by('visit')
        else:
            board_list = boards.order_by('good_count')

        paginator = Paginator(board_list.all(), 5)
        page = paginator.get_page(page)

        content['boards'] = page.object_list
        content['page_list'] = paginator.page_range
        return render(request, 'boards.html', content)


class CreateBoard(View):  # boards/add/  board-add
    def get(self, request):
        user = get_user(request)
        if user is None:
            return redirect(f'/users/login/?next=/boards/add/')
        else:
            return render(request, 'item/board_create.html')

    def post(self, request):
        data = request.POST
        title = data.get("title")
        content = data.get("content")
        user = get_user(request)
        if user is None:
            return redirect(f'/users/login/?next=/boards/add/')

        tags = get_tag(request, request.POST.get("tag"))
        b = False
        b = check_blank(title, "제목", request) or b
        b = check_blank(content, "내용", request) or b
        b = tags is None or b

        if b:
            return redirect(request.META['HTTP_REFERER'])
        board = Board.objects.create(
            title=title,
            content=content,
            user=user,
            username=user.username
        )
        for tag in tags:
            board.tag.add(tag)
        board.save()
        return redirect('boards')


class OneBoard(View):  # boards/<int:board_id>/    board-item
    def get(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        board.visit += 1
        board.save()
        user = get_user(request)

        commands = list()
        for i in board.command.all():
            login_check = (user is not None) and (user == i.user)
            commands.append({"value": i, "login_check": login_check})

        check_user = board.user == user
        context = {
                    "board": board,
                    "good": len(board.good.all()),
                    "commands": commands,
                    "check_user": check_user,
                    "tags": board.tag.all()
                }
        if (user is not None) and (user in board.good.all()):
            context["good_check"] = True
        context['user'] = user

        exi, image_data = read_image(board.user.profile_image.name)
        context['image'] = {"exi": exi, "data": get_base(image_data)}
        return render(request, 'item/board_item.html', context)

    def post(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        user = get_user(request)
        if user is None:
            return redirect(f'/users/login/?next=/boards/{board_id}/')
        else:
            if request.POST.get('good') is not None:
                if board in user.good.all():
                    user.good.remove(board)
                    board.good.remove(user)
                    board.good_count = len(board.good.all())
                else:
                    user.good.add(board)
                    board.good.add(user)
                    board.good_count = len(board.good.all())
                board.save()
            elif request.POST.get('command_send') is not None:
                command_value = request.POST.get('command')
                if not check_blank(command_value, '댓글 내용', request):
                    command = Command.objects.create(
                        content=command_value,
                        user=user
                    )
                    board.command.add(command)
            elif request.POST.get('command_remove') is not None:
                command_id = request.POST.get('command_id')
                Command.delete(Command.objects.get(pk=command_id))
            return redirect(request.META['HTTP_REFERER'])


class EditBoard(View):  # boards/<int:board_id>/edit/    board-edit
    def get(self, request, board_id):
        board = Board.objects.get(pk=board_id)
        user: User = get_user(request)
        if user is None or board.user != user:
            return redirect(f'/users/login/?next=/boards/{board_id}/edit/')
        else:
            content = {
                "title": board.title,
                "content": board.content,
                "board_id": board_id,
                "tags": "#" + " #".join(list(tags.tag_name for tags in board.tag.all()))
            }
            return render(request, 'item/board_edit.html', content)

    def post(self, request, board_id):
        title = request.POST.get("title")
        content = request.POST.get("content")
        tags = get_tag(request, request.POST.get("tag"))

        b = False
        b = check_blank(title, "제목", request) or b
        b = check_blank(content, "내용", request) or b
        if b:
            return redirect(request.META['HTTP_REFERER'])
        else:
            board = Board.objects.get(pk=board_id)
            board.title = title
            board.content = content
            for tag in tags:
                board.tag.add(tag)
            board.save()
            return redirect(f"/boards/{board.pk}/")


class RemoveBoard(View):  # boards/<int:board_id>/remove/    board-remove
    def get(self, request, board_id):
        user = get_user(request)
        board = Board.objects.get(pk=board_id)
        if user is not None and board.user == user:
            Board.delete(board)
            return redirect('boards')
        else:
            return redirect(f'/users/login/?next=/boards/{board_id}/')
