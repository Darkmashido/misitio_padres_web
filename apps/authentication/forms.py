from django import forms


class AuthenticationForm(forms.Form):
    email = forms.EmailField(
        label="Usuario",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full rounded-2xl border border-white/20 bg-white/90 px-5 py-4 text-base font-semibold text-slate-900 shadow-sm outline-none transition placeholder:text-slate-500 focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/25",
                "placeholder": "admin@misitio.com",
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Contrasena",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full rounded-2xl border border-white/20 bg-white/90 px-5 py-4 text-base font-semibold text-slate-900 shadow-sm outline-none transition placeholder:text-slate-500 focus:border-cyan-400 focus:ring-4 focus:ring-cyan-400/25",
                "placeholder": "************",
                "autocomplete": "current-password",
            }
        ),
    )
