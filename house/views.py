from django.shortcuts import render
from rest_framework import viewsets
from .models import HouseModel
from user.models import ProfileModel
from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrNone
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHouseManagerOrNone]
    queryset = HouseModel.objects.all()
    serializer_class = HouseSerializer

    @action(detail=True, methods=['post'], name='Join', permission_classes=[])
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profilemodel

            if user_profile.house is None:
                user_profile.house = house
                user_profile.save()
                return Response({'message': 'You have successfully joined the house.'}, status=status.HTTP_200_OK)
            elif user_profile in house.members.all():
                return Response({'message': 'You are already a member of this house.'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'You are already in a house.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], name='leave', permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profilemodel

            if user_profile in house.members.all():
                user_profile.house = None
                user_profile.save()
                return Response({'message': 'You have successfully left the house.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You are not in this house.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], name='remove_member', permission_classes=[IsHouseManagerOrNone])
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            member_to_remove = request.data.get('member_to_remove', None)

            if member_to_remove is None:
                return Response({'message': 'No member selected.'}, status=status.HTTP_400_BAD_REQUEST)

            profile_to_remove = ProfileModel.objects.get(user_id=member_to_remove)
            # b = get_object_or_404(ProfileModel, user_id=member_to_remove) its to get object or 404
            # another was is to remove the member from the house using house.members.remove(profile_to_remove)
            if profile_to_remove in house.members.all():
                profile_to_remove.house = None
                profile_to_remove.save()
                return Response({'message': 'Member removed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Member not part of this house.'}, status=status.HTTP_404_NOT_FOUND)

        except ProfileModel.DoesNotExist:
            return Response({'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
