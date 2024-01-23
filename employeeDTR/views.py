from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import datetime
from .models import Employee, Department, Position, DTR
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UploadFileForm
import xlrd



def base(request):
    
    
    return render(request,'base.html')

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
                (datetime.combine(datetime.today(), dtr.timeOut_AM) - datetime.combine(datetime.today(), dtr.timeIn_AM)).total_seconds() +
                (datetime.combine(datetime.today(), dtr.timeOut_PM) - datetime.combine(datetime.today(), dtr.timeIn_PM)).total_seconds()
            ) / 3600

            total_overtime_hours = (
                (datetime.combine(datetime.today(), dtr.overtimeOut) - datetime.combine(datetime.today(), dtr.overtimeIn)).total_seconds() / 3600
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

def upload_xls(request):
    if request.method=='POST':
        form=UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file=request.FILES['excelFile']
            excel_data = xlrd.open_workbook(file_contents=uploaded_file.read())
            print("Uploaded_file",uploaded_file)
            print("asd",excel_data)
            sheet = excel_data.sheet_by_index(0)
            cell_value=sheet.cell_value(1,0)
            print(cell_value)
            #return render(request,'success.html')
        else:
            form=UploadFileForm()
    return render(request, 'upload_xls.html')


def login_page(request):
    return render(request, 'login_page.html')

def empdb(request):
    return render(request, 'empdb.html')