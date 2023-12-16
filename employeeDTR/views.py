from django.shortcuts import render
from django.db.models import Sum, F
from datetime import datetime
from .models import Employee, Department, Position, DTR


def home(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    positions = Position.objects.all()
    dtr_list = DTR.objects.all()

    # Calculate total worked hours for each employee and date
    total_hours_data = {}
    for employee in employees:
        dtr_instances = DTR.objects.filter(employee=employee)
        
        for dtr in dtr_instances:
            date_str = str(dtr.date)
            if date_str not in total_hours_data:
                total_hours_data[date_str] = {
                    'date': dtr.date,
                    'employee_data': [],
                }

            total_regular_hours = (
                (datetime.combine(datetime.today(), dtr.timeOut_AM) - datetime.combine(datetime.today(), dtr.timeIn_AM)).seconds +
                (datetime.combine(datetime.today(), dtr.timeOut_PM) - datetime.combine(datetime.today(), dtr.timeIn_PM)).seconds
            ) / 3600
            total_overtime_hours = (
                (datetime.combine(datetime.today(), dtr.overtimeOut) - datetime.combine(datetime.today(), dtr.overtimeIn)).seconds / 3600
            )

            total_hours_data[date_str]['employee_data'].append({
                'employee': employee,
                'total_regular_hours': total_regular_hours,
                'total_overtime_hours': total_overtime_hours,
            })
            

    context = {
        'total_hours_data': total_hours_data.values(),
        'departments': departments,
        'positions': positions,
        'dtr_list': dtr_list,
    }

    return render(request, 'home.html', context)
