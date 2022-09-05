from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from statistic.Service.statistic_service import (
    get_gender_statistics,
)


class GenderStatisticsView(APIView):
    """
    남/여 유저 성별 통계 기능
    """

    def get(self, request):
        male_count, female_count = get_gender_statistics()
        return Response({"male_count": male_count, "female_count": female_count}, status=status.HTTP_200_OK)


class AgeStatisticsView(APIView):
    """
    나이별 유저 통계 기능    
    """

    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)