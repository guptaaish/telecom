import pandas as pd

cols = ['Plan name','Monthly Rental','Free internet','Free calls','Free SMS','Call charges(per minute)','SMS charges(per sms)','Data Charges(per MB)','Roaming charges(per Minute)']

df = pd.DataFrame()

def add_row():
	
	print('Example\nPlan name:\tSpecial\nMonthly Rental:\t200\nFree Internet:\tYes\nFree calls:\tYes\nFree Internet:\tYes\nCall charges:\t0.2\nSMS charges:\t0.1\nData charges:\t0\nRoaming charges:\t0')
	
	print('Enter the details')

	plan_name = input("Plan name:\t")
	monthly_rental = int(input('Monthly Rental:\t'))
	free_internet = input('Free Internet:\t')
	free_calls = input('Free calls:\t')
	free_sms = input('Free SMS:\t')
	call_charges = float(input('Call charges:\t'))
	sms_charges = float(input('SMS charges:\t'))
	data_charges = float(input('Data charges:\t'))
	roaming_charges = float(input('Roaming Charges:\t'))
	
	data = [[plan_name, monthly_rental,free_internet,free_calls,free_sms,call_charges,sms_charges,data_charges,roaming_charges]]
	
	df1 = pd.DataFrame(data,columns = cols)
	
	df.append(df1)
	df = df.reset_index().drop(['index'],axis = 1)

def display():
	print(df)

def filter():
	print('The data can be filtered on Free Calls, Free SMSs, Free Internet, Monthly Rental')
	response = input('enter the filter criteria').lower()
	if response == 'free sms' | response == 'free smss':
		print(df[df['Free SMS'] == 'Yes'])
	elif response == 'free calls':
		print(df[df['Free calls'] == 'Yes'])
	elif response == 'free internet':
		print(df[df['Free internet'] == 'Yes'])
	elif response == 'monthly rental':
		minimum = int(input('enter the minimum amount:\t'))
		maximum = int(input('enter the maximum amount:\t'))
		print(df[(df['Monthly Rental'] >= minimum) & (df[df['Monthly Rental'] <= maximum)])

a = True

print('__________________________________Welcome to the Telecom Operator Application________________________________________________')

while a == True:

	print('For adding a row type ADD\nFor displaying allthe plans from the database type DISPLAY\nFor applying filters type FILTER')
	response = input()
	if response == 'ADD':
		add_row()

	elif response == 'DISPLAY':
		display()

	elif response == 'FILTER':
		filter()

	else:
		print('Invalid command')

	exit_res = input('type Yes if you want to continue').lower()

	if exit_res == 'yes':
		a = False



