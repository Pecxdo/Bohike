from django.urls import path
from .views import eliminar_categoria, home, register, agregar_movimiento, eliminar_movimiento, categorias, agregar_categoria

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("agregar/", agregar_movimiento, name="agregar"),
    path("eliminar/<int:id>/", eliminar_movimiento, name="eliminar"),
    path("categorias/", categorias, name="categorias"),
    path("categorias/agregar/", agregar_categoria, name="agregar_categoria"),
    path("categorias/eliminar/<int:id>/", eliminar_categoria, name="eliminar_categoria"),
]