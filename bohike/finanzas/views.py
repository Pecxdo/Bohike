from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Categoria
from django.shortcuts import get_object_or_404, redirect
from .models import Movimiento, Categoria

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Usuario creado correctamente")
        return redirect("login")

    return render(request, "finanzas/register.html")


#Home  
@login_required
def home(request):
    movimientos = Movimiento.objects.filter(usuario=request.user)

    ingresos = sum(m.monto for m in movimientos if m.tipo == "ingreso")
    gastos = sum(m.monto for m in movimientos if m.tipo == "gasto")

    balance = ingresos - gastos

    context = {
    "ingresos": ingresos,
    "gastos": gastos,
    "balance": balance,
    "movimientos": movimientos.order_by("-fecha"),
    }

    return render(request, "finanzas/home.html", context)






@login_required
def agregar_movimiento(request):

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descripcion = request.POST.get("descripcion")
        monto = request.POST.get("monto")
        categoria_id = request.POST.get("categoria")

        Movimiento.objects.create(
            usuario=request.user,
            tipo=tipo,
            descripcion=descripcion,
            monto=monto,
            categoria_id=categoria_id if categoria_id else None
        )

        return redirect("home")

    categorias = Categoria.objects.filter(usuario=request.user)

    return render(request, "finanzas/agregar.html", {
        "categorias": categorias
    })
   
@login_required
def eliminar_movimiento(request, id):
    movimiento = Movimiento.objects.get(id=id, usuario=request.user)
    movimiento.delete()
    return redirect("home")

def categorias(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, "finanzas/categorias.html", {
        "categorias": categorias
    })


def agregar_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            Categoria.objects.create(
                usuario=request.user,
                nombre=nombre
            )
        return redirect("categorias")

    return render(request, "finanzas/agregar_categoria.html")


def eliminar_categoria(request, id):
    categoria = get_object_or_404(
        Categoria,
        id=id,
        usuario=request.user
    )
    categoria.delete()
    return redirect("categorias")