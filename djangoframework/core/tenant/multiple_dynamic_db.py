# import threading
# from django.db import connections
# from django.db.utils import ConnectionHandler,ConnectionDoesNotExist
# from django.conf import settings
# from concurrent.futures import ThreadPoolExecutor
# import asyncio
# from asgiref.sync import sync_to_async,async_to_sync
# from django.db.models import Q

# therad_name = threading.current_thread().name

# # create Excutor
# db_excutor = ThreadPoolExecutor(max_workers=50)

# def add_database(db_name):

#     if db_name not in settings.DATABASES:
#         settings.DATABASES[db_name] = {
#             'ENGINE': settings.DATABASES['default']['ENGINE'],
#             'NAME': db_name,
#             'USER': settings.DATABASES['default']['USER'],
#             'PASSWORD': settings.DATABASES['default']['PASSWORD'],
#             'HOST': settings.DATABASES['default']['HOST'],
#             'PORT': settings.DATABASES['default']['PORT'],
#             # other configurations
#             'TIME_ZONE': settings.DATABASES['default'].get('TIME_ZONE', None),
#             'OPTIONS': settings.DATABASES['default'].get('OPTIONS', {}),
#             'AUTOCOMMIT': settings.DATABASES['default'].get('AUTOCOMMIT', False),
#             'CONN_MAX_AGE': settings.DATABASES['default'].get('CONN_MAX_AGE', 60),
#             'CONN_HEALTH_CHECKS': settings.DATABASES['default'].get('CONN_HEALTH_CHECKS', False),
#             'CONN_PARAMS': settings.DATABASES['default'].get('CONN_PARAMS', {}),
#             'TEST': settings.DATABASES['default'].get('TEST', {}),
#             'TEST_CHARSET': settings.DATABASES['default'].get('TEST_CHARSET', None),
#             'TEST_COLLATION': settings.DATABASES['default'].get('TEST_COLLATION', None),
#             'AUTOMIC_REQUESTS': settings.DATABASES['default'].get('AUTOMIC_REQUESTS', False),
#         }
#         connections.databases[db_name] = settings.DATABASES[db_name]

# @sync_to_async
# def get_db_all():
#     return list(orgization.objects.filter(is_active=True).exclude(Q(db_name__isnull=True) | Q(db_name='')) .values_list('db_name', flat=True))

# #checking all db in phone number
# @sync_to_async(executor=db_excutor,thread_sensitive=False)
# async def check_all_db(request):

#     mobile = request.data.get('mobile')
#     def get_user_by_mobile(db_name:str,mobile:str):
#         User.objects.using(db_name).filter(mobile=mobile).exists()
#         add_database(db)
#         db_status = User.objects.using(db).filter(mobile=mob_no).exists()
#         connections[db].close()
#         return db_status

#     db_list = await get_db_all()
#     task = [get_user_by_mobile(db,mobile) for db in db_list]
#     return await asyncio.gather(*task)

# class UserFinding(GenericAPIView):
#     def post(self,request):
#         db_status = async_to_sync(check_all_db)(request)
#         return Response({'db_status':db_status})