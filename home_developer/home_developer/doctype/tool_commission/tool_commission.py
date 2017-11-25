# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ToolCommission(Document):
	

	def get_data(self):

		if not self.month_commission :
			frappe.throw("Field Month diisi terlebih dahulu !")
		if not self.fiscal_year :
			frappe.throw("Field Year  diisi terlebih dahulu !")
		if not self.sales_person :
			frappe.throw("Field Sales diisi terlebih dahulu !")

		bulan = self.month_commission
		tahun = self.fiscal_year
		sales_person = self.sales_person

		user_sales = sales_person

		self.penamaan_document = sales_person + " " + bulan + " " + tahun

		self.posting_date = frappe.utils.today()

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

		string_kondisi = str(tahun) + "-" + str(string_bulan) + "%"


		temp_data = frappe.db.sql(""" 
			SELECT
			skjb.`name`,
			skjb.`nama_pembeli`,
			skjb.`posting_date`,
			skjb.`harga_jual`,
			skjb.`workflow_state`
			FROM `tabSKPJB` skjb
			WHERE (skjb.`workflow_state` = "HardCash" 
				OR skjb.`workflow_state` = "Booking Confirmed" 
				OR skjb.`workflow_state` = "Tunai Bertahap" 
				OR skjb.`workflow_state` = "KPR" 
				OR skjb.`workflow_state` = "Batal"
				OR skjb.`workflow_state` = "Pindah Kavling"  
			)
			AND skjb.`posting_date` LIKE "{0}"
			AND skjb.`sales_person` = "{1}"
		
		""".format(string_kondisi, user_sales), as_list=1)

		temp_data_batal = frappe.db.sql(""" 
			

			SELECT
			skjb.`name`,
			skjb.`nama_pembeli`,
			skjb.`posting_date`,
			skjb.`harga_jual`,
			skjb.`workflow_state`
			FROM `tabSKPJB` skjb
			WHERE skjb.`workflow_state` = "Batal"
			AND skjb.`tanggal_cancel` LIKE "{0}"
			AND skjb.`sales_person` = "{1}"

		
		""".format(string_kondisi, user_sales), as_list=1)

		temp_data_pindah = frappe.db.sql(""" 
			

			SELECT
			skjb.`name`,
			skjb.`nama_pembeli`,
			skjb.`posting_date`,
			skjb.`harga_jual`,
			skjb.`workflow_state`
			FROM `tabSKPJB` skjb
			WHERE skjb.`workflow_state` = "Pindah Kavling"
			AND skjb.`tanggal_pindah` LIKE "{0}"
			AND skjb.`sales_person` = "{1}"
		
		""".format(string_kondisi, user_sales), as_list=1)

		self.tool_commission_item = []
		total_fee = 0
		total_price = 0
		
		#aku tambahin persen_fee disini ya, soalnya error
		persen_fee = 0
		
		if temp_data :
			
			for i in temp_data :
				total_price = total_price + i[3]

			if temp_data_batal :
				for i in temp_data_batal :
					total_price = total_price - (i[3])

			if temp_data_pindah :
				for i in temp_data_pindah :
					total_price = total_price - (i[3])

			persen_fee = 0
			if total_price < 999999999 :
				persen_fee = 1
			elif total_price >= 1000000000 and total_price < 1999999999 :
				persen_fee = 1.2
			elif total_price >= 2000000000 :
				persen_fee = 1.5

			
			for i in temp_data :
				pp_so = self.append('tool_commission_item', {})
				pp_so.skjb = i[0]
				pp_so.skjb_date = i[2]
				pp_so.skjb_customer = i[1]
				pp_so.skjb_net_price = i[3]
				pp_so.skjb_fee = i[3] * persen_fee / 100
				total_fee = total_fee + pp_so.skjb_fee

				kavling = frappe.get_doc("SKPJB", i[0]).kavling
				company_kavling = frappe.get_doc("Kavling", kavling).company
				pp_so.company = company_kavling

		if temp_data_batal :
			
			
			for i in temp_data_batal :
				pp_so = self.append('tool_commission_item', {})
				pp_so.skjb = i[0]
				pp_so.skjb_date = i[2]
				pp_so.skjb_customer = i[1]
				pp_so.skjb_net_price = i[3] * -1
				pp_so.skjb_fee = i[3] * persen_fee / 100 * -1
				total_fee = total_fee + pp_so.skjb_fee

				kavling = frappe.get_doc("SKPJB", i[0]).kavling
				company_kavling = frappe.get_doc("Kavling", kavling).company
				pp_so.company = company_kavling

		if temp_data_pindah :

			for i in temp_data_pindah :
				pp_so = self.append('tool_commission_item', {})
				pp_so.skjb = i[0]
				pp_so.skjb_date = i[2]
				pp_so.skjb_customer = i[1]
				pp_so.skjb_net_price = i[3] * -1
				pp_so.skjb_fee = i[3] * persen_fee / 100 * -1
				total_fee = total_fee + pp_so.skjb_fee

				kavling = frappe.get_doc("SKPJB", i[0]).kavling
				company_kavling = frappe.get_doc("Kavling", kavling).company
				pp_so.company = company_kavling
		
		#kena error persen_fee nya di sini
		self.fee = persen_fee
		self.total_net_price = total_price
		self.total_fee = total_fee



@frappe.whitelist()
def make_payment_entry(tool_commission):

	frappe.msgprint("Untuk sementara buat jurnalnya manual dahulu")
	
	# # cara baru
	# temp_data = frappe.db.sql(""" 
	# 	SELECT
	# 	sum(tci.`skjb_fee`),
	# 	tci.`company`
	# 	FROM `tabTool Commission Item` tci
	# 	WHERE tci.`parent` = "{}"
	# 	group by tci.`company`
	# 	ORDER BY tci.`company`
			
	# """.format(tool_commission), as_list=1)


	# if temp_data :
	# 	company = ""
	# 	account_kas = "2.1.404 LAIN-LAIN TERHUTANG - "
	# 	account_commission = "4.1.101 PENJUALAN BLOK A - "
	# 	cost_center = "Main - "
	# 	company_abbr = ""

	# 	data_je = ""
	# 	counter = 0
	# 	for i in temp_data :
	# 		if i[0] == 0 :
	# 			counter = 0
	# 		elif i[0] > 0 :
	# 			company = i[1]
	# 			je = frappe.new_doc("Journal Entry")
	# 			je.update({
	# 				"voucher_type": "Journal Entry",
	# 				"tool_commission" : tool_commission,
	# 				"company" : company,
	# 				"posting_date" : frappe.utils.today()
	# 			})
	# 			company_abbr = frappe.get_doc("Company", company).abbr

	# 			je.append("accounts", {
	# 				"debit_in_account_currency": abs(i[0]),
	# 				"debit": abs(i[0]),
	# 				"account" : account_commission + company_abbr,
	# 				"cost_center" : cost_center + company_abbr
	# 			})

	# 			je.append("accounts", {
	# 				"credit_in_account_currency": abs(i[0]),
	# 				"credit": abs(i[0]),
	# 				"account" : account_kas + company_abbr,
	# 				"cost_center" : cost_center + company_abbr
	# 			})

	# 			je.flags.ignore_permissions = 1
	# 			je.save()

	# 			data_je = data_je + str(je.name)

	# 		elif i[0] < 0 :
	# 			company = i[1]
	# 			je = frappe.new_doc("Journal Entry")
	# 			je.update({
	# 				"voucher_type": "Journal Entry",
	# 				"tool_commission" : tool_commission,
	# 				"company" : company,
	# 				"posting_date" : frappe.utils.today()
	# 			})
	# 			company_abbr = frappe.get_doc("Company", company).abbr

	# 			je.append("accounts", {
	# 				"credit_in_account_currency": abs(i[0]),
	# 				"credit": abs(i[0]),
	# 				"account" : account_commission + company_abbr,
	# 				"cost_center" : cost_center + company_abbr
	# 			})

	# 			je.append("accounts", {
	# 				"debit_in_account_currency": abs(i[0]),
	# 				"debit": abs(i[0]),
	# 				"account" : account_kas + company_abbr,
	# 				"cost_center" : cost_center + company_abbr
	# 			})

	# 			je.flags.ignore_permissions = 1
	# 			je.save()

	# 			data_je = data_je + str(je.name)



	# # cara lama
	# # ambil data komisi

	# temp_data = frappe.db.sql(""" 
	# 	SELECT
	# 	tci.`skjb`,
	# 	tci.`skjb_fee`,
	# 	tci.`company`
	# 	FROM `tabTool Commission Item` tci
	# 	WHERE tci.`parent` = "{}"
	# 	AND tci.`is_used` = 0
	# 	ORDER BY tci.`company`
			
	# """.format(tool_commission), as_list=1)

	# if temp_data :
	# 	company = ""
	# 	counter = 0
	# 	total_kas = 0
	# 	panjang_data = len(temp_data)
	# 	account_kas = "Cash - "
	# 	account_commission = "Commission on Sales - "
	# 	cost_center = "Main - "
	# 	company_abbr = ""

	# 	data_je = ""
	# 	for i in temp_data :
	# 		if counter == 0 :
	# 			company = i[2]
	# 			je = frappe.new_doc("Journal Entry")
	# 			je.update({
	# 				"voucher_type": "Journal Entry",
	# 				"tool_commission" : tool_commission,
	# 				"company" : company,
	# 				"posting_date" : frappe.utils.today()
	# 			})

	# 			# isi je account
	# 			company_abbr = frappe.get_doc("Company", company).abbr

	# 			if i[1] < 0 :
	# 				je.append("accounts", {
	# 					"credit_in_account_currency": i[1],
	# 					"account" : account_commission + company_abbr,
	# 					"skjb" : i[0],
	# 					"cost_center" : cost_center + company_abbr
	# 				})
	# 			else :
	# 				je.append("accounts", {
	# 					"debit_in_account_currency": i[1],
	# 					"account" : account_commission + company_abbr,
	# 					"skjb" : i[0],
	# 					"cost_center" : cost_center + company_abbr
	# 				})

	# 			total_kas = total_kas + i[1]
	# 			counter = counter + 1

	# 			if counter == panjang_data :
	# 				je.append("accounts", {
	# 					"credit_in_account_currency": total_kas,
	# 					"account" : account_kas + company_abbr,
	# 					"cost_center" : cost_center + company_abbr
	# 				})

	# 				je.flags.ignore_permissions = 1
	# 				je.save()

	# 				data_je = data_je + str(je.name)

	# 		elif company == i[2] :

	# 			# isi je account
	# 			company_abbr = frappe.get_doc("Company", company).abbr

	# 			if i[1] < 0 :
	# 				je.append("accounts", {
	# 					"credit_in_account_currency": i[1],
	# 					"account" : account_commission + company_abbr,
	# 					"skjb" : i[0],
	# 					"cost_center" : cost_center + company_abbr
	# 				})
	# 			else :
	# 				je.append("accounts", {
	# 					"debit_in_account_currency": i[1],
	# 					"account" : account_commission + company_abbr,
	# 					"skjb" : i[0],
	# 					"cost_center" : cost_center + company_abbr
	# 				})

	# 			total_kas = total_kas + i[1]
	# 			counter = counter + 1

	# 			if counter == panjang_data :
	# 				je.append("accounts", {
	# 					"credit_in_account_currency": total_kas,
	# 					"account" : account_kas + company_abbr,
	# 					"cost_center" : cost_center + company_abbr
	# 				})

	# 				je.flags.ignore_permissions = 1
	# 				je.save()

	# 				data_je = data_je + str(je.name)

	# 		else :
	# 			# je sebelumnya
	# 			je.append("accounts", {
	# 				"credit_in_account_currency": total_kas,
	# 				"account" : account_kas + company_abbr,
	# 					"cost_center" : cost_center + company_abbr
	# 			})

	# 			je.flags.ignore_permissions = 1
	# 			je.save()

	# 			data_je = data_je + str(je.name)

	# 			# new je
	# 			company = ""
	# 			total_kas = 0
	# 			account_kas = "Cash - "
	# 			account_commission = "Commission on Sales - "
	# 			company_abbr = ""

	# 			# 
	# 			company = i[2]
	# 			je = frappe.new_doc("Journal Entry")
	# 			je.update({
	# 				"voucher_type": "Journal Entry",
	# 				"tool_commission" : tool_commission,
	# 				"company" : company,
	# 				"posting_date" : frappe.utils.today()
	# 			})

	# 			# isi je account
	# 			company_abbr = frappe.get_doc("Company", company).abbr

	# 			if i[1] < 0 :
	# 				je.append("accounts", {
	# 					"credit_in_account_currency": i[1],
	# 					"account" : account_commission + company_abbr,
	# 					"skjb" : i[0],
	# 					"cost_center" : cost_center + company_abbr
	# 				})
	# 			else :
	# 				je.append("accounts", {
	# 					"debit_in_account_currency": i[1],
	# 					"account" : account_commission + company_abbr,
	# 					"skjb" : i[0],
	# 					"cost_center" : cost_center + company_abbr
	# 				})

	# 			total_kas = total_kas + i[1]
	# 			counter = counter + 1

	# 			if counter == panjang_data :
	# 				je.append("accounts", {
	# 					"credit_in_account_currency": total_kas,
	# 					"account" : account_kas + company_abbr,
	# 					"cost_center" : cost_center + company_abbr
	# 				})

	# 				je.flags.ignore_permissions = 1
	# 				je.save()

	# 				data_je = data_je + str(je.name)


	# return data_je