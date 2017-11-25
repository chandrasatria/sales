from frappe import _

def get_data():
	return {
		'fieldname': 'skjb_utj_booking',
		#'non_standard_fieldnames': {
		#
		#},
		#'internal_links': {
		#	'Sales Invoice': ['items', 'sales_invoice'],
		#},
		'transactions': [
			{
				'label': _('Invoice'),
				'items': ['Sales Invoice']
			},
			
		]
	}