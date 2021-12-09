from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.global_variable import BASE_DIR
from collections import Counter
import pytz

class TimezoneView(APIView):
    def get(self, request):
        dir = BASE_DIR + "/timezone_calc/timezone.txt"
        Names = []
        for line in open(dir, 'r').readlines():
            Names.append(line.strip())
        print(Names, "mm")
        my_dict = dict(Counter(Names))
        print(my_dict, "1")
        sorted_values = sorted(my_dict.values())  # Sort the values
        sorted_dict = {}

        for i in sorted_values:
            for k in my_dict.keys():
                if my_dict[k] == i:
                    sorted_dict[k] = my_dict[k]

        print(sorted_dict, "sd")
        res = dict(reversed(list(sorted_dict.items())))
        print(res)
        l = []
        for i in res.keys():
            l.append(i)
            if len(l) == 5:
                break
        print(l)
        return Response({
            "status": True,
            "timezones": l
        })


class AllTimezones(APIView):
    def get(self, request):
        a = [i for i in pytz.all_timezones]
        all_tz_list = []
        i = 1
        for item in a:
            value = {i: item}
            all_tz_list.append(value)
            i = i + 1

        return Response({
            "status": True,
            "all_timezones": all_tz_list
        })
