import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from friend.models import FriendList, FriendRequest


def friends_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id:
            try:
                this_user = User.objects.get(pk=user_id)
                context['this_user'] = this_user
            except User.DoesNotExist:
                return HttpResponse("Este usuario no existe")
            try:
                friend_list = FriendList.objects.get(user=this_user)
            except FriendList.DoesNotExist:
                return HttpResponse(f"No se pudo encontrar la lista de amigos de {this_user.username}")
            if user != this_user:
                if not user in friend_list.friends.all():
                    return HttpResponse("Debéis ser amigos para ver su lista de amigos")
            friends = []
            auth_user_friend_list = FriendList.objects.get(user=user)
            for friend in friend_list.friends.all():
                friends.append(
                    (friend, auth_user_friend_list.is_mutual_friend(friend)))
            context['friends'] = friends
    else:
        return HttpResponse("Debéis ser amigos para ver su lista de amigos")
    return render(request, "friend/friend_list.html", context)


def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        account = User.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(
                receiver=account, is_active=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("No puedes ver la lista de amigos de otros usuarios")
    else:
        redirect("login")
    return render(request, "friend/friend_requests.html", context)


def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(
                    sender=user, receiver=receiver)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("Ya le enviaste una solicitud")
                    friend_request = FriendRequest(
                        sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Solicitud de amistad enviada"
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Solicitud de amistad enviada"

            if payload['response'] == None:
                payload['response'] = "Algo fue mal"
        else:
            payload['response'] = "Error al enviar solicitud"
    else:
        payload['response'] = "Debes autenticarte para enviar la solicitud"
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept()
                    payload['response'] = "Solicitud de amistad aceptada"

                else:
                    payload['response'] = "Algo fue mal"
            else:
                payload['response'] = "No puedes aceptar una solicitud que no es tuya"
        else:
            payload['response'] = "Error al aceptar la solicitud"
    else:
        payload['response'] = "Debes autenticarte para aceptar la solicitud"
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Amigo eliminado"
            except Exception as e:
                payload['response'] = f"Algo fue mal: {str(e)}"
        else:
            payload['response'] = "Error al intentar eliminar amigo"
    else:
        payload['response'] = "Debes autenticarte para eliminar un amigo"
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.decline()
                    payload['response'] = "Solicitud de amistad declinada"
                else:
                    payload['response'] = "Algo fue mal"
            else:
                payload['response'] = "No puedes declinar una solicitud que no es tuya"
        else:
            payload['response'] = "Error al declinar la solicitud"
    else:
        payload['response'] = "Debes autenticarte para declinar una solicitud"
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(
                    sender=user, receiver=receiver, is_active=True)
            except FriendRequest.DoesNotExist:
                payload['response'] = "Solicitud de amistad no existente"
            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel()
                payload['response'] = "Solicitud de amistad cancelada"
            else:
                friend_requests.first().cancel()
                payload['response'] = "Solicitud de amistad cancelada"
        else:
            payload['response'] = "Error al cancelar la solicitud"
    else:
        payload['response'] = "Debes autenticarte para cancelar una solicitud"
    return HttpResponse(json.dumps(payload), content_type="application/json")
