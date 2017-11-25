# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ToolKavling(Document):
	
	def update_kavling(doc):
		value_str = ""
		for item in doc.items :
			if item.kavling and item.harga_kavling and item.booking_fee and item.catatan and item.diskon :
				kav_doc = frappe.get_doc("Kavling",item.kavling)
				kav_doc.harga_cicilan = item.harga_kavling
				kav_doc.diskon_cash = item.diskon
				kav_doc.cash_keras = kav_doc.harga_cicilan - kav_doc.diskon_cash
				kav_doc.booking_1 = item.booking_fee
				kav_doc.catatan = item.catatan
				kav_doc.save()
		return "success"
	
	def get_kavling(doc):
		if not doc.perumahan  :
			return "fail"
		result = frappe.db.sql(""" 
			SELECT k.`name`,k.`harga_cicilan`,k.`booking_1`,k.`catatan`,k.`diskon_cash` 
			FROM `tabKavling`k 
			WHERE k.`lokasi_perumahan` = "{0}" 
			AND (ISNULL(k.`skjb`) OR k.`skjb`="") 
			""".format(doc.perumahan))
		for res in result :
			#checker = 0
			#if doc.kavling_from and doc.kavling_to :
			#	check_num = res[4]
			#	check_num = check_num.split(doc.kavling_blok,1)[1]
			#	try : 
			#		check_num = int(check_num)
			#		if check_num >= doc.kavling_from and check_num <= doc.kavling_to :
			#			checker = 1
			#		else :
			#			checker = 0
			#	except :
			#		checker = 0
			#else :
			#	checker = 1
			checker = 1
			if checker == 1 :
				cd = doc.append('items')
				cd.kavling = res[0]
				cd.harga_kavling = res[1]
				cd.booking_fee = res[2]
				cd.catatan = res[3]
				cd.diskon = res[4]
		return "success"
	
	def update_all(doc):
		for item in doc.items :
			kdoc = frappe.get_doc("Kavling",item.kavling)
			if doc.all_harga :
				item.harga_kavling = doc.all_harga
				kdoc.harga_cicilan = doc.all_harga
				kdoc.cash_keras = kdoc.harga_cicilan - (kdoc.diskon_cash or 0)
			if doc.all_booking :
				item.booking_fee = doc.all_booking
				kdoc.booking_1 = doc.all_booking
			if doc.all_catatan :
				item.catatan = doc.all_catatan
				kdoc.catatan = doc.all_catatan
			kdoc.save()
		return "success"
	pass

	