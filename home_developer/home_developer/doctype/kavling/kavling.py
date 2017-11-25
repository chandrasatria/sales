# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Kavling(Document):

	def autoname(self):
		self.name=self.naming_series + self.nama_kavling

		
@frappe.whitelist()
def fetch_komplek_diskon(komplek):
	komdoc = frappe.get_doc("Tipe Rumah",komplek)
	return komdoc.diskon_cash
	
