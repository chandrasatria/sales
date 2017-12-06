# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Kavling(Document):
	def validate(self):
		if self.is_used==1:
			result = frappe.db.sql("""select name from `tabSKPJB` where kavling="{}" and workflow_state NOT IN ("Pending","Batal") """.format(self.name),asList=1)
			for row in result:
				frappe.throw("Kavling tidak bisa di Open karena sudah memiliki {}".format(row[0]))
	def autoname(self):
		self.name=self.naming_series + self.nama_kavling

		
@frappe.whitelist()
def fetch_komplek_diskon(komplek):
	komdoc = frappe.get_doc("Tipe Rumah",komplek)
	return komdoc.diskon_cash
	
