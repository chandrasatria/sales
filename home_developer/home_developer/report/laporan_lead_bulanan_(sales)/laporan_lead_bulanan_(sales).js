// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Laporan Lead Bulanan (Sales)"] = {
	"filters": [
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": "January" + "\n"
				+ "February" + "\n"
				+ "March" + "\n"
				+ "April" + "\n"
				+ "May" + "\n"
				+ "June" + "\n"
				+ "July" + "\n"
				+ "August" + "\n"
				+ "September" + "\n"
				+ "October" + "\n"
				+ "November" + "\n"
				+ "December"
				,
			"reqd" : 1,
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Link",
			"options":"Fiscal Year",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("fiscal_year")
		},
	]
}
