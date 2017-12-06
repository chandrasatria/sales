# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SKPJB(Document):
	def validate(self):
		self.generate_in_words()
	
		self.check_kavling()
		if self.workflow_state != "UTJ Batal" :
			self.change_kavling()
		if self.workflow_state == "Pindah Kavling" or self.workflow_state == "Batal" or self.workflow_state == "UTJ Batal" :
			self.delete_kavling()
			
		if self.workflow_state != self.old_workflow :
			self.generate_document_ledger()

		self.get_lead_source()
	
	def on_update_after_submit(self):
		if self.workflow_state == "HardCash" and self.cara_pembayaran != "Cash Keras" :
			frappe.throw("Cara Pembayaran Tidak Sesuai")
		elif self.workflow_state == "KPR" and self.cara_pembayaran != "KPR" :
			frappe.throw("Cara Pembayaran Tidak Sesuai")
		elif self.workflow_state == "Tunai Bertahap" and self.cara_pembayaran != "Tunai Bertahap" :
			frappe.throw("Cara Pembayaran Tidak Sesuai")
			
		if self.workflow_state != self.old_workflow :
			self.generate_document_ledger()
			
	def generate_document_ledger(self):
		dt = frappe.new_doc("Document Ledger")
		dt.document_type = "SKPJB"
		dt.document_name = self.name
		dt.sales_person = self.sales_person
		dt.document_status = self.workflow_state
		dt.posting_date = self.posting_date
		dt.value = self.sisa_pembayaran
		dt.company = self.company
		dt.transition_date = frappe.utils.today()
		dt.save()
		self.old_workflow = self.workflow_state
	
	def get_lead_source(self):
		if self.nama_pembeli :
			self.lead_source = frappe.get_value("Customer",self.nama_pembeli,"lead_source")
		else :
			self.lead_source = ""
		
	
	
	def on_trash(self):
		self.delete_kavling()
	
	def before_cancel(self):
		self.set_tanggal_cancel()
	
	def on_cancel(self):
		self.delete_kavling()
		if self.workflow_state != self.old_workflow :
			self.generate_document_ledger()
		
		
	def set_tanggal_cancel(self):
		if self.workflow_state == "Batal" :
			self.tanggal_cancel = frappe.utils.today()
		elif self.workflow_state == "Pindah Kavling" :
			self.tanggal_pindah = frappe.utils.today()
		else :
			frappe.throw(self.workflow_state)
			
	def autoname(self):
		#self.name = self.nama_pembeli + "-" + self.perumahan + "-" + self.kavling
		count = frappe.get_doc("Number Count","SKJB")
		digit = str(count.next_digit)
		while len(digit) < 4 :
			digit = "0" + digit
		
		singkatan = self.kavling
		date = frappe.utils.today()
		month = date[5:7]
		year = date[0:4]
		self.name = digit + '/SKPJB/' + singkatan + '/' + month + '/' + year
		
		#update number count
		temp = count.next_digit + 1
		if temp > 9999 :
			temp = 1
		count.next_digit = temp
		count.save()
	
	def generate_in_words(self):
		if self.harga_jual :
			self.terbilang = frappe.utils.data.money_in_words(self.harga_jual,"Rupiah","Sen")
		else :
			self.terbilang = "-"
		if self.rabat_1 :
			self.terbilang_rabat_1 = frappe.utils.data.money_in_words(self.rabat_1,"Rupiah","Sen")
		else :
			self.terbilang_rabat_1 = "-"
	
	def check_kavling(self):
		kavling = self.kavling
		kdoc = ""
		try :
			kdoc = frappe.get_doc("Kavling",kavling)
		except :
			frappe.throw("Kavling tidak ditemukan.")
		if kdoc.is_used and kdoc.skjb != self.name :
			frappe.throw("Kavling sudah digunakan di SKJB lain")
		
	def change_kavling(self):
		kdoc = frappe.get_doc("Kavling",self.kavling)
		kdoc.is_used = 1
		kdoc.skjb = self.name
		kdoc.save()
		
		result = frappe.db.sql(""" SELECT k.`name` FROM `tabKavling`k WHERE k.`skjb`="{0}" AND k.`name` != "{1}" """.format(self.name,self.kavling),as_list=1)
		for res in result :
			resdoc = frappe.get_doc("Kavling",res[0])
			resdoc.is_used = 0
			resdoc.skjb = ""
			resdoc.save()
	
	def delete_kavling(self):
		result = frappe.db.sql(""" SELECT k.`name` FROM `tabKavling`k WHERE k.`skjb`="{0}" """.format(self.name),as_list=1)
		for res in result :
			resdoc = frappe.get_doc("Kavling",res[0])
			resdoc.is_used = 0
			resdoc.skjb = ""
			resdoc.save()
	
	
	#dummied
	def set_kavling(self):
		kavling = self.kavling
		kdoc = frappe.get_doc("Kavling",kavling)
		kdoc.is_used = 1
		kdoc.save()
	
	#dummied
	def cancel_kavling(self):
		kavling = self.kavling
		kdoc = frappe.get_doc("Kavling",kavling)
		kdoc.is_used = 0
		kdoc.save()
		
@frappe.whitelist()
def get_sales(customer):
	cdoc = frappe.get_doc("Customer",customer)
	lead = cdoc.lead_name
	if lead :
		ldoc = frappe.get_doc("Lead",lead)
		if ldoc.lead_owner :
			return ldoc.lead_owner
		else :
			return ""
	return ""
	

@frappe.whitelist()
def make_invoice(cdn,nama_pembeli,company):
	source_dt = frappe.get_doc("SKJB Item",cdn)
	dt = frappe.new_doc('Sales Invoice')
	dt.customer = nama_pembeli
	dt.company = company
	dt.debit_to = frappe.get_value("Company",dt.company,"default_receivable_account")
	cd = dt.append('items')
	cd.item_code = "Cicilan"
	cd.rate = source_dt.jumlah_cicilan
	cd.qty = 1
	data[res[0]] = dt.name
	return dt

@frappe.whitelist()
def get_harga_by_type(type,kavling) :
	kav_doc = frappe.get_doc("Kavling",kavling)
	pr = 0
	if type == "KPR" :
		pr = kav_doc.harga_cicilan
	elif type == "Cash Keras" :
		pr = kav_doc.cash_keras
	elif type == "Tunai Bertahap" :
		pr = kav_doc.harga_cicilan
	return pr

@frappe.whitelist()
def fetch_customer_data(customer):
	cusdoc = frappe.get_doc("Customer",customer)
	r = {}
	r["ktp_pembeli"] = cusdoc.ktp_pembeli
	r["alamat_ktp"] = cusdoc.alamat_ktp
	r["alamat_tt"] = cusdoc.alamat_tt
	r["rt_rw"] = cusdoc.rt_rw
	r["desa_kelurahan"] = cusdoc.desa_kelurahan
	r["kecamatan"] = cusdoc.kecamatan
	r["alamat_surat"] = cusdoc.alamat_surat
	r["telp_rumah"] = cusdoc.telp_rumah
	r["telp_hp"] = cusdoc.telp_hp
	r["telp_saudara"] = cusdoc.telp_saudara
	return r

@frappe.whitelist()
def get_booking_fee(kavling):
	kavdoc = frappe.get_doc("Kavling",kavling)
	return kavdoc.booking_1

@frappe.whitelist()
def get_no_rekening(kavling):
	kav_doc = frappe.get_doc("Kavling",kavling)
	data = {}
	if kav_doc.no_rekening :
		data["no_rekening"] = kav_doc.no_rekening
		rek_doc = frappe.get_doc("Nomor Rekening",kav_doc.no_rekening)
		data["atas_nama"] = rek_doc.atas_nama
		data["nama_bank"] = rek_doc.bank
	else :
		data["no_rekening"] = ""
		data["atas_nama"] = "-"
		data["nama_bank"] = "-"
	return data	
		
@frappe.whitelist()
def get_skjb_data(skjb):
	data = {}
	skjb_doc = frappe.get_doc("SKPJB",skjb)
	data["company"] = skjb_doc.company
	data["customer"] = skjb_doc.nama_pembeli
	
	com_doc = frappe.get_doc("Company",skjb_doc.company)
	data["debit_to"] = com_doc.default_receivable_account
	
	return data
	
@frappe.whitelist()
def get_current_user_sales():
	username = frappe.session.user
	user_doc = frappe.get_doc("User",username)
	if user_doc.sales_person :
		return user_doc.sales_person
	else :
		return "no_sales"
