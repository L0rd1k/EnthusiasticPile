
## Routers - автоматическая маршрутизация URL ( способ привязки логики представления к набору URL-адресов)
Добавление бибилтотеки: from rest_framework import routers
### * SimpleRouter - класс
``` javascript 
router = routers.SimpleRouter()
Inst: router.register(prefix, viewset , basename)
router.register(r'users', UserViewSet, basename='user-list')
router.register(r'accounts', AccountViewSet, basename='account-list')
```
#### > 1. First style of including urls
``` javascript
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('', include(router.urls))
]
urlpatterns += router.urls
```
#### > 2. Second style of including urls
``` javascript
urlpatterns = [
    path('forgot-password', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```
#### > 3. Third style of including urls
``` javascript
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'))),
]
```
#### > 4. Fourth style of including urls
``` javascript
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
]
```

### Routing for extra actions
``` javascript
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action
class UserViewSet(ModelViewSet):
    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf], 
    url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None):
        ...
```
В приведенном выше примере теперь будет создан следующий шаблон URL:
 - URL path: ^users/{pk}/change-password/$
 - URL name: 'user-change_password'

### DefaultRouter - класс
Этот маршрутизатор похож на SimpleRouter, как указано выше, но дополнительно включает корневое представление API по умолчанию, которое возвращает ответ, содержащий гиперссылки на все представления списков. Он также генерирует маршруты для дополнительных суффиксов формата стиля .json.
``` javascript
router = DefaultRouter(trailing_slash=False) 
```
trailing_slash - По умолчанию URL-адреса, добавляются с косой чертой в конце. 
