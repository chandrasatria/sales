# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar

def execute(filters=None):
	columns, data = [], []
	
	bulan = filters.get("month")
	string_bulan = ""
	if bulan == "January" :
		string_bulan = str("01")
	elif bulan == "February" :
		string_bulan = str("02")
	elif bulan == "March" :
		string_bulan = str("03")
	elif bulan == "April" :
		string_bulan = str("04")
	elif bulan == "May" :
		string_bulan = str("05")
	elif bulan == "June" :
		string_bulan = str("06")
	elif bulan == "July" :
		string_bulan = str("07")
	elif bulan == "August" :
		string_bulan = str("08")
	elif bulan == "September" :
		string_bulan = str("09")
	elif bulan == "October" :
		string_bulan = str("10")
	elif bulan == "November" :
		string_bulan = str("11")
	elif bulan == "December" :
		string_bulan = str("12")
	
	tahun = str(filters.get("year"))
	
	days = calendar.monthrange(int(tahun),int(string_bulan))[1]
	
	string_kondisi = str(tahun) + "-" + str(string_bulan) + "%"
	date_clause = """ WHERE l.`creation` LIKE "{0}" """.format(string_kondisi)
	sales_clause = ""
	if filters.get("sales_person") :
		sales_clause = """ 
		JOIN `tabUser`u ON u.`name`=l.`lead_owner` 
		JOIN `tabSales Person`s ON s.`name`=u.`sales_person`  AND s.`name`="{0}" """.format(filters.get("sales_person"))
	result = frappe.db.sql(""" 
		SELECT l.`source`,DATE(l.`creation`) as `posting_date`,SUM(1) FROM `tabLead`l {0} 
		{1}
		GROUP BY l.`source`,`posting_date`
		ORDER BY l.`source`
		""".format(sales_clause,date_clause))
	
	source_list = []
	date_list = []
	for i in range(1,days + 1) :
		str_i = str(i)
		if i < 10 :
			str_i = "0" + str_i
		date_list.append(str_i)
	data_dict = {}
	columns = ["Lead Source:Link/Lead Source:150"]
	for res in result :
		if res[0] not in source_list :
			source_list.append(res[0])
		date = str(res[1]).split("-")[-1]
		key = (res[0],date)
		data_dict[key] = res[2]
	for date in date_list :
		columns.append(date+":Int:50")
	columns.append("Total:Int:60")
	
	data = []
	for source in source_list :
		total = 0
		data_row = [source]
		for date in date_list :
			key = (source,date)
			if key in data_dict :
				lead_num = data_dict[key]
				total = total + lead_num
				data_row.append(lead_num)
			else :
				data_row.append(0)
		data_row.append(total)
		data.append(data_row)
	
	
	return columns, data
