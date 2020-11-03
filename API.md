
## Routers - автоматическая маршрутизация URL ( способ привязки логики представления к набору URL-адресов)
Добавление бибилтотеки: from rest_framework import routers
### * SimpleRouter - класс
``` javascript 
router = routers.SimpleRouter()
Inst: router.register(prefix, viewset , basename)
router.register(r'users', UserViewSet, basename='user-list')
router.register(r'accounts', AccountViewSet, basename='account-list')
```
#### > First style of including urls
``` javascript
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('', include(router.urls))
]
urlpatterns += router.urls
```
#### > Second style of including urls
``` javascript
urlpatterns = [
    path('forgot-password', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```
#### > Third style of including urls
``` javascript
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'))),
]
```
#### > Fourth style of including urls
``` javascript
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
```
### DefaultRouter - класс
