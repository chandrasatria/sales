from __future__ import unicode_literals
import frappe

	
def check_stock(doc,method):
	if doc.lead_status == "Potensi 1" or doc.lead_status == "Potensi 2" :
		if not doc.stock_lead :
			frappe.throw("Mandatory Field : Stock Lead")
	if doc.lead_status != doc.old_status :
		dt = frappe.new_doc("Document Ledger")
		dt.document_type = "Lead"
		dt.document_name = doc.name
		if doc.lead_owner :
			user = frappe.get_doc("User",doc.lead_owner)
			if user.sales_person :	
				dt.sales_person = user.sales_person
		dt.document_status = doc.lead_status
		dt.posting_date = doc.creation
		dt.transition_date = frappe.utils.today()
		dt.save()
		doc.old_status = doc.lead_status
def get_lead_source(doc,method):
	if doc.lead_name :
		doc.lead_source = frappe.get_value("Lead",doc.lead_name,"source")
	else :
		doc.lead_source = ""
