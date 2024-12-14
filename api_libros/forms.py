from django import forms
from api_libros.modelos.models import Usuario  # Importa tu modelo personalizado


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario  # Usa tu modelo personalizado
        fields = ['email', 'username', 'nombre', 'password']  # Incluye todos los campos necesarios

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])  # Establece la contraseña
        if commit:
            usuario.save()
        return usuario
