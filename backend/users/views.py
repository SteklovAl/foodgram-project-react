from api.pagination import LimitPagePagination
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer


class SubscriptionsView(generics.ListAPIView):
    """Получить на кого пользователь подписан."""
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitPagePagination

    def list(self, request):
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page, many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    """
    Подписка.
    Удаление подписки.
    """

    @action(detail=True,
            methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.get_or_create(user=user, author=author)[0]
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_del(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if not Follow.objects.filter(user=user, author=author).exists():
            return Response({'errors': 'Подписки не существует.'},
                            status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.get(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
