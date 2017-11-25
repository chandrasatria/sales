// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Business Intelligence"] = {
	"filters": [
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: [
				{ "value": "Qty", "label": __("Qty") },
				{ "value": "Omzet", "label": __("Omzet") },
			],
			reqd: 1
		},
		{
			fieldname: "report_type",
			label: __("Document"),
			fieldtype: "Select",
			options: [
				{ "value": "Lead", "label": __("Lead") },
				{ "value": "UTJ Pending", "label": __("UTJ") },
				{ "value": "UTJ Batal", "label": __("Batal UTJ") },
				{ "value": "Else", "label": __("SKJB") },
				{ "value": "Batal", "label": __("SKJB Batal") },
				{ "value": "Pindah Kavling", "label": __("SKJB Pindah") },
			],
			reqd: 1
		},
		{
			fieldname: "filter_by",
			label: __("Filter By"),
			fieldtype: "Select",
			options: [
				{ "value": "Lead Source", "label": __("Lead Source") },
				{ "value": "Sales Person", "label": __("Sales Person") },
				{ "value": "Perumahan", "label": __("Perumahan") },
			],
			reqd: 1
		},
		/*
		{
			fieldname: "fiscal_year",
			label: __("Fiscal Year"),
			fieldtype: "Link",
			options: "Fiscal Year",
			default: frappe.sys_defaults.fiscal_year,
			reqd: 1
		},
		*/
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1
		},
		{
			fieldname: "period",
			label: __("Period"),
			fieldtype: "Select",
			options: [
				{ "value": "Daily", "label": __("Daily") },
				{ "value": "Weekly", "label": __("Weekly") },
				{ "value": "Monthly", "label": __("Monthly") },
				{ "value": "Quarterly", "label": __("Quarterly") },
				{ "value": "Yearly", "label": __("Yearly") },
			],
			reqd: 1
		},
	]
}
