from django import forms

from wesgarlock.tenant.models import Tenant, TenantOwner


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = "__all__"


class TenantOwnerForm(forms.ModelForm):
    class Meta:
        model = TenantOwner
        fields = "__all__"


tenant_formset = forms.inlineformset_factory(
    Tenant,
    TenantOwner,
    fields="__all__",
    fk_name="tenants"
)
