# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

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
	
	string_kondisi = str(tahun) + "-" + str(string_bulan) + "%"
	date_clause = """ AND l.`creation` LIKE "{0}" """.format(string_kondisi)
	
	
	result = frappe.db.sql(""" 
		SELECT l.`source`,l.`perumahan`,SUM(1) FROM `tabLead`l
		WHERE NOT l.`perumahan` IS NULL 
		{0}
		GROUP BY l.`source`,l.`perumahan`
		ORDER BY l.`perumahan`
		""".format(date_clause),as_list=1)
	
	source_list = []
	perum_list = []
	data_dict = {}
	columns = ["Lead Source:Link/Lead Source:150"]
	for res in result :
		if res[0] not in source_list :
			source_list.append(res[0])
		if res[1] not in perum_list :
			perum_list.append(res[1])
			columns.append(res[1]+":Int:125")
		key = (res[0],res[1])
		data_dict[key] = res[2]
	columns.append("Total:Int:60")
	
	source_list.sort()
	data = []
	for source in source_list :
		total = 0
		data_row = [source]
		for perum in perum_list :
			key = (source,perum)
			if key in data_dict :
				lead_num = data_dict[key]
				total = total + lead_num
				data_row.append(lead_num)
			else :
				data_row.append(0)
		data_row.append(total)
		data.append(data_row)
	
	return columns, data
