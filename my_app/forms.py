# plate_app/forms.py
from django import forms
from .models import PlateSession

class ManualEntryForm(forms.ModelForm):
    class Meta:
        model = PlateSession
        fields = ['plate_number', 'vehicle_type']
        widgets = {
            'plate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Plate Number'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
        }


class UpdateSessionForm(forms.ModelForm):
    custom_charge = forms.DecimalField(
        required=False, 
        label='Custom Charge (Optional)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = PlateSession
        fields = ['exit_time', 'is_paid']  # Exit time now editable
        widgets = {
            'exit_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        entry = instance.entry_time
        exit = instance.exit_time

        if entry and exit:
            duration = exit - entry
            minutes = duration.total_seconds() / 60
            auto_charge = round((minutes / 60) * 20)  # ₹50/hour

            if self.cleaned_data.get('custom_charge'):
                instance.charge = self.cleaned_data['custom_charge']
            else:
                instance.charge = auto_charge

        if commit:
            instance.save()
        return instance



class ManualEntryForm(forms.ModelForm):
    class Meta:
        model = PlateSession
        fields = ['plate_number', 'vehicle_type', 'entry_time', 'exit_time', 'is_paid']
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'exit_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'plate_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
