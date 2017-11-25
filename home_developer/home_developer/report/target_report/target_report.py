# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Sales:Data:80","Target (A):Currency:140","Stock Lead P1 (B1):Currency:140","Stock Lead P2 (B2):Currency:140","B1 + B2 (B3):Currency:140",
		"Target VS Stock (A-B3):Currency:140","Realisasi (D):Currency:140","Selisih (A-D):Currency:140"]
	
	string_bulan = ""
	bulan = filters.get("month")
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
	
	date_clause = """ WHERE l.`creation` LIKE "{0}" """.format(string_kondisi)
	date_clause_2 = """ AND s.`creation` LIKE "{0}" """.format(string_kondisi)
	
	data = frappe.db.sql(""" 
		SELECT sp.`name`,sp.`target_currency`,SUM(IF(STRCMP(l.`status`,'Potensi 1'),0,IFNULL(l.`stock_lead`,0))),
			SUM(IF(STRCMP(l.`status`,'Potensi 2'),0,IFNULL(l.`stock_lead`,0))),
			SUM(IF(STRCMP(l.`status`,'Potensi 1'),0,IFNULL(l.`stock_lead`,0))) +
			SUM(IF(STRCMP(l.`status`,'Potensi 2'),0,IFNULL(l.`stock_lead`,0))),
			sp.`target_currency` - SUM(IF(STRCMP(l.`status`,'Potensi 1'),0,IFNULL(l.`stock_lead`,0))) - 
			SUM(IF(STRCMP(l.`status`,'Potensi 2'),0,IFNULL(l.`stock_lead`,0))),
			IFNULL(s.`harga_jual`,0),
			sp.`target_currency` - IFNULL(s.`harga_jual`,0)
		FROM `tabSales Person`sp 
		JOIN `tabUser`u ON u.`sales_person`=sp.`name` 
		JOIN `tabLead`l ON l.`lead_owner`=u.`name`
		LEFT JOIN 
		(
			SELECT s.`sales_person`,SUM(s.`harga_jual`) AS `harga_jual` FROM `tabSKPJB`s 
			WHERE s.`docstatus`=1
			{1}
			GROUP BY s.`sales_person`
		)
		s ON s.`sales_person`=sp.`name` 
		{0}
		GROUP BY sp.`name`
		""".format(date_clause,date_clause_2))
	
	return columns, data
