from django.db import models
from datetime import datetime


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.department_name

class Position(models.Model):
    position = models.CharField(max_length=255)
    
    def __str__(self):
        return self.position
    
class LoansTaxes(models.Model):
    name=models.CharField(max_length=255)
    amount=models.FloatField()
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    STATUS_CHOICES = [
        (1, "Active"),
        (0, "Inactive"),
    ]

    EMP_TYPE_CHOICES = [
        ("Part-Time", "Part-Time"),
        ("Full-Time", "Full-Time"),
        ("Flex-Time", "Flex-Time"),
        ("Project-Based", "Project-Based"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    dob = models.DateField()
    date_hired = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    hourly_rate = models.FloatField(default=0.0)
    employee_type = models.CharField(max_length=100, choices=EMP_TYPE_CHOICES, default="Part-Time")
    email = models.EmailField(max_length=255)
    sample_loans=models.ManyToManyField(LoansTaxes,related_name="employee", through="Deductions")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class DTR(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    timeIn_AM = models.TimeField()
    timeOut_AM = models.TimeField()
    timeIn_PM = models.TimeField()
    timeOut_PM = models.TimeField()
    overtimeIn = models.TimeField()
    overtimeOut = models.TimeField()
    paid=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date}"
    
    def total_worked_hours(self):
        # Convert time fields to datetime objects with a fixed date
        date_today = datetime.today().date()
        time_in_am = datetime.combine(date_today, self.timeIn_AM)
        time_out_am = datetime.combine(date_today, self.timeOut_AM)
        time_in_pm = datetime.combine(date_today, self.timeIn_PM)
        time_out_pm = datetime.combine(date_today, self.timeOut_PM)
        overtime_in = datetime.combine(date_today, self.overtimeIn)
        overtime_out = datetime.combine(date_today, self.overtimeOut)

        # Calculate total worked hours for the day
        total_worked_hours = (
            (time_out_am - time_in_am).seconds / 3600 +
            (time_out_pm - time_in_pm).seconds / 3600 +
            (overtime_out - overtime_in).seconds / 3600
        )

        return total_worked_hours
    

class Deductions(models.Model):
    employee=models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    loanTaxes=models.ForeignKey(LoansTaxes, on_delete=models.CASCADE, null=True)
    
