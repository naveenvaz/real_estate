from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import *
from .forms import *
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm

def user_logout(request):
    logout(request)
    return redirect('login')

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

@login_required(login_url='login')
def property_list(request):
    property = Property.objects.all()
    return render(request,"property_listings.html",{'properties':property})

@login_required(login_url='login')
def property_create(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('property_list')
            except:
                pass
    else:
        form = PropertyForm()
    return render(request,'create_property.html',{'form':form})

@login_required(login_url='login')
def property_update(request, id):
    proper = Property.objects.get(id=id)
    form = PropertyForm(initial={'name': proper.name, 'address': proper.address, 'location': proper.location, 'features': proper.features})
    if request.method == "POST":
        form = PropertyForm(request.POST, instance=proper)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('property_list')
            except Exception as e:
                pass
    return render(request,'update_property.html',{'form':form})

@login_required(login_url='login')
def property_delete(request, id):
    property_obj = Property.objects.get(id=id)
    try:
        property_obj.delete()
    except:
        pass
    return redirect('property_list')

@login_required(login_url='login')
def property_units(request, property_id):
    property_instance = get_object_or_404(Property, pk=property_id)
    units = property_instance.unit_set.all()
    context = {
        'property': property_instance,
        'units': units,
    }
    return render(request, 'property_detail.html', context)

@login_required(login_url='login')
def unit_list(request):
    search_query = request.GET.get('search', '')
    all_units = Unit.objects.all()
    if search_query:
        all_units = all_units.filter(
            Q(property__name__icontains=search_query) |
            Q(size__icontains=search_query) |
            Q(tenant__name__icontains=search_query) |
            Q(tenant__isnull=True)
        )
    available_units = all_units.filter(available=True, tenant__isnull=False)
    available_to_book_units = all_units.filter(available=True, tenant__isnull=True)
    return render(request, 'unit_list.html', {
        'available_units': available_units,
        'available_to_book_units': available_to_book_units,
        'search_query': search_query,
    })

@login_required(login_url='login')
def create_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        property_id = request.GET.get('property_id')
        size = request.GET.get('size')
        if property_id and size:
            existing_unit = get_object_or_404(Unit, property__id=property_id, size=size, available=True, tenant__isnull=True)
            form = UnitForm(instance=existing_unit)
        else:
            form = UnitForm()
    return render(request, 'create_unit.html', {'form': form})

@login_required(login_url='login')
def update_unit(request, id):
    unit = get_object_or_404(Unit, pk=id)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'update_unit.html', {'form': form, 'unit': unit})
@login_required(login_url='login')
def delete_unit(request, id):
    unit = get_object_or_404(Unit, pk=id)
    unit.delete()
    return redirect('unit_list')

@login_required(login_url='login')
def agreement_list(request):
    agreements = Agreement.objects.all()
    return render(request, 'agreement_list.html', {'agreements': agreements})

@login_required(login_url='login')
def create_agreement(request):
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agreement_list')
        else:
            pass
    else:
        form = AgreementForm()
    return render(request, 'create_agreement.html', {'form': form})

@login_required(login_url='login')
def update_agreement(request, id):
    agreement = get_object_or_404(Agreement, pk=id)
    if request.method == 'POST':
        form = AgreementForm(request.POST, instance=agreement)
        if form.is_valid():
            form.save()
            return redirect('agreement_list')
    else:
        form = AgreementForm(instance=agreement)
    return render(request, 'update_agreement.html', {'form': form})

@login_required(login_url='login')
def delete_agreement(request, id):
    agreement = get_object_or_404(Agreement, pk=id)
    agreement.delete()
    return redirect('agreement_list')

@login_required(login_url='login')
def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenant_list.html', {'tenants': tenants})

@login_required(login_url='login')
def create_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'create_tenant.html', {'form': form})

@login_required(login_url='login')
def update_tenant(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    if request.method == 'POST':
        form = TenantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'update_tenant.html', {'form': form, 'tenant': tenant})

@login_required(login_url='login')
def delete_tenant(request, pk):
    tenant = get_object_or_404(Tenant, pk=pk)
    tenant.delete()
    return redirect('tenant_list')

@login_required(login_url='login')
def tenant_profile(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    documents = tenant.document_set.all()
    unit = Unit.objects.filter(tenant=tenant).first()
    context = {
        'tenant': tenant,
        'documents': documents,
        'unit': unit,
    }
    return render(request, 'tenant_profile.html', context)

@login_required(login_url='login')
def agreements_for_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    agreements = tenant.agreement_set.all()
    context = {
        'tenant': tenant,
        'agreements': agreements,
    }
    if not agreements:
        return render(request, 'no_agreements_found.html', context)
    return render(request, 'agreements_for_tenant.html', context)

@login_required(login_url='login')
def view_documents(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    context = {
        'tenant': tenant,
    }
    return render(request, 'view_documents.html', context)

@login_required(login_url='login')
def get_units_for_property(request):
    property_id = request.GET.get('property_id')
    units = Unit.objects.filter(property__id=property_id)
    unit_options = [{'id': unit.id, 'name': str(unit)} for unit in units]
    return JsonResponse({'units': unit_options})

@login_required(login_url='login')
def get_tenants_for_unit(request):
    unit_id = request.GET.get('unit_id')
    unit_obj = Unit.objects.get(id=unit_id)
    if unit_obj.tenant:
        tenant_options = [{'id': unit_obj.tenant.id, 'name': unit_obj.tenant.name}]
    else:
        tenant_options = []
    return JsonResponse({'tenants': tenant_options})

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def search_results(request):
    query = request.GET.get('q', '')
    results = Unit.objects.filter(size__icontains=query)  # Adjust based on your model fields
    context = {'query': query, 'results': results}
    return render(request, 'search_results.html', context)

@login_required(login_url='login')
def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            if 'add_another' in request.POST:
                return redirect('add_document')
            else:
                return redirect('add_document')
    else:
        form = DocumentForm()

    return render(request, 'add_documents.html', {'form': form})

@login_required(login_url='login')
def feature_list(request):
    features = Feature.objects.all()
    return render(request, 'features_list.html', {'features': features})

@login_required(login_url='login')
def create_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feature_list')
    else:
        form = FeatureForm()
    return render(request, 'create_feature.html', {'form': form})

@login_required(login_url='login')
def update_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            return redirect('feature_list')
    else:
        form = FeatureForm(instance=feature)
    return render(request, 'update_features.html', {'form': form, 'feature': feature})

@login_required(login_url='login')
def delete_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    feature.delete()
    return redirect('feature_list')