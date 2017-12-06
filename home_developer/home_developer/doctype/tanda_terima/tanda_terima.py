# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class TandaTerima(Document):
	def validate(self):
		self.generate_in_words()			
		if self.workflow_state != self.old_workflow :
			self.generate_document_ledger()
	def generate_in_words(self):
		if self.utj :
			self.terbilang_utj = frappe.utils.data.money_in_words(self.utj,"Rupiah","Sen")
		else :
			self.terbilang_utj = "-"
	
	def on_update_after_submit(self):
		if self.workflow_state != self.old_workflow :
			self.generate_document_ledger()
	def generate_document_ledger(self):
		dt = frappe.new_doc("Document Ledger")
		dt.document_type = "Tanda Terima"
		dt.document_name = self.name
		dt.sales_person = self.sales_person
		dt.document_status = self.workflow_state
		dt.posting_date = self.posting_date
		dt.value = self.utj
		dt.company = self.company
		dt.transition_date = frappe.utils.today()
		dt.save()
		self.old_workflow = self.workflow_state