from django.contrib import admin
from .models import Employee, Department, Position, DTR, LoansTaxes

admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(DTR)
admin.site.register(LoansTaxes)