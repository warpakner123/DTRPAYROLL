from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import datetime
from .models import Employee, Department, Position, DTR
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UploadFileForm
import xlrd
from datetime import datetime
import time



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
            print("UPLOADED FILE: ",uploaded_file)
            sheet = excel_data.sheet_by_index(0)
            #cell_value=sheet.cell_value(0,0)
            #print(cell_value)
            first_id=''
            def convert(a):
                converted_string=str(a)
                converted_string = converted_string.replace('text:\'', '').replace('\'', '')
                return converted_string
            #store employee
            emp_storage = []
            temp_storage = []
            
            for rx in range(1, sheet.nrows):
                system_id=sheet.row(rx)[2]
                systemId=int(convert(system_id))
                if first_id == '':
                    first_id=systemId
                
                if first_id != systemId:
                    first_id = systemId
                    emp_storage.append(temp_storage)
                    temp_storage=[]
                    
                if first_id == systemId:
                    temp_storage.append(sheet.row(rx))
                if rx == sheet.nrows - 1:
                    emp_storage.append(temp_storage)
                    temp_storage=[]
            print("Employee Storage")
            print(emp_storage)
            for first_array in emp_storage:
                temp_date=''
                temp_time=''
                
                for index, second_array in enumerate(first_array):
                    time = convert(second_array[3])
                    strip_time = datetime.strptime(time,'%d/%m/%Y %H:%M:%S')
                    print(strip_time.date())
                    if temp_date == '':
                        temp_date = strip_time.date()
                    
                    # if same date check time.
                    if index != 0 and temp_date == strip_time.date():
                        # check previous - current time
                        previous_time = convert(first_array[index - 1][3])
                        previous_time = datetime.strptime(previous_time, '%d/%m/%Y %H:%M:%S')
                        print('previous: {}'.format(previous_time))
                        print(previous_time.timestamp())
                        # current time
                        current = strip_time
                        print('current: {}'.format(current))
                        print(current.timestamp())
                        # interval time between current and previous time
                        interval_nila = current.timestamp() - previous_time.timestamp()
                        print('interval: {}'.format(interval_nila / 3600))
                        # check if interval in less than 2 hours
                        if not (interval_nila < 7200):
                            print('counted')
                        else:
                            print('not counted')
                        # print((previous_time + current).time())
                        # chop-chop ang date para sa payroll
                    if temp_date != strip_time.date():
                        temp_date = strip_time.date()
                        return render(request,'success.html')
        else:
            form=UploadFileForm()
    return render(request, 'upload_xls.html')


def login_page(request):
    return render(request, 'login_page.html')

def empdb(request):
    return render(request, 'empdb.html')