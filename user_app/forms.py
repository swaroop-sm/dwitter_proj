from django import forms


class SignUpForm(forms.Form):
    
    username = forms.CharField(label = "Username*")

    email = forms.EmailField(label = "Email*")

    password = forms.CharField(label = "Password*",
                    widget = forms.PasswordInput(),
                    error_messages = {'required': "Please enter a Password"})

    first_name = forms.CharField(label = "First Name*",
                    error_messages = {'required': "Please enter Full Name"})
    
    last_name = forms.CharField(label = "Last Name*", 
                    error_messages = {'required': "Please enter Last Name"})

    mobile = forms.CharField(label = "Mobile Number*",
                    max_length = 15, min_length = 10, 
                    error_messages = {'required': "Please enter Mobile Number"})
    
    dob = forms.DateField(label = "Date of Birth*", input_formats = ['%m/%d/%Y'],
                    widget = forms.TextInput(attrs = {'placeholder': 'MM/DD/YYYY'}))




class LoginForm(forms.Form):
    
    username = forms.CharField(label = "Username",
                    error_messages = {'required': "Please enter Username"})
    
    password = forms.CharField(label = "Password",
                    error_messages = {'required': "Please enter a Password"})