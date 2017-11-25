# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Sales:Link/User:100","Lead:Int:100","Potensi 1:Int:100","Potensi 2:Int:100","Converted:Int:100","Do Not Contact:Int:100"]
	
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
	
	data = frappe.db.sql(""" SELECT u.`sales_person`, SUM(IF(STRCMP(l.`status`,'Lead'),0,1)) ,SUM(IF(STRCMP(l.`status`,'Potensi 1'),0,1)),
		SUM(IF(STRCMP(l.`status`,'Potensi 2'),0,1)),SUM(IF(STRCMP(l.`status`,'Converted'),0,1)),
		SUM(IF(STRCMP(l.`status`,'Do Not Contact'),0,1)) 
		FROM `tabLead`l JOIN `tabUser`u on l.`lead_owner` = u.`name`
		WHERE l.`perumahan`="{0}" 
		{1}
		GROUP BY l.`lead_owner`""".format(filters.get("perumahan"),date_clause))
	
	return columns, data
