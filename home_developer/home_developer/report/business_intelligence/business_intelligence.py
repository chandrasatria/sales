# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	if filters.get("report_type") == "Lead" and filters.get("based_on") == "Omzet" :
		return [],[]
	columns,date_columns = get_columns(filters)	
	if filters.get("report_type") == "Lead" :
		first_column = ""
		group_clause = ""
		join_clause = ""
		if filters.get("filter_by") == "Lead Source" :
			first_column = """ l.`source` """
			group_clause = """ GROUP BY l.`source` """
		elif filters.get("filter_by") == "Sales Person" :
			first_column = """ u.`sales_person` """
			join_clause = """ JOIN `tabUser`u ON u.`name`=l.`lead_owner` """
			group_clause = """ GROUP BY u.`sales_person` """
		elif filters.get("filter_by") == "Perumahan" :
			first_column = """ l.`perumahan` """
			group_clause = """ GROUP BY l.`perumahan` """
		
		year_clause = ""
		#if filters.get("fiscal_year") and not filters.get("period") == "Yearly" :
		#	year_clause = """ AND YEAR(l.`creation`)={0} """.format(filters.get("fiscal_year"))
		
		date_clause = ""
		if filters.get("from_date") and filters.get("to_date") :
			date_clause = """ AND DATE(l.`creation`) BETWEEN "{0}" AND "{1}" """.format(filters.get("from_date"),filters.get("to_date"))
		
		#date_columns = ""
		#if not filters.get("period") == "Yearly" :
		#	begin_month = []
		#	end_month = []
		#	if filters.get("period") == "Monthly" :
		#		begin_month = [1,2,3,4,5,6,7,8,9,10,11,12]
		#		end_month = [1,2,3,4,5,6,7,8,9,10,11,12]
		#	elif filters.get("period") == "Quarterly" :
		#		begin_month = [1,4,7,10]
		#		end_month = [3,6,9,12]
		#	for i in range(0,len(begin_month)) :
				
		#		begin = begin_month[i]
		#		end = end_month[i]
		#		date_columns = """{0}, SUM(IF(MONTH(l.`creation`)>={1} AND MONTH(l.`creation`)<={2},1,0))  """.format(date_columns,begin,end)
		#else :
		#	result = frappe.db.sql(""" SELECT y.`name` FROM `tabFiscal Year`y  """)
		#	for res in result :
		#		date_columns = """{0}, SUM(IF(YEAR(l.`creation`)={1},1,0)) """.format(date_columns,res[0])
		#data = frappe.db.sql(""" SELECT {0} {1} FROM `tabLead`l {2} WHERE 1=1 {3} {4}  """.format(first_column,date_columns,join_clause,year_clause,group_clause))
		data = frappe.db.sql(""" SELECT {0} {1} FROM `tabLead`l {2} WHERE 1=1 {3} {4}  """.format(first_column,date_columns,join_clause,date_clause,group_clause))
	else :
		first_column = ""
		group_clause = ""
		if filters.get("filter_by") == "Lead Source" :
			first_column = """ s.`lead_source` """
			group_clause = """ GROUP BY s.`lead_source` """
		elif filters.get("filter_by") == "Sales Person" :
			first_column = """ s.`sales_person` """
			group_clause = """ GROUP BY s.`sales_person` """
		elif filters.get("filter_by") == "Perumahan" :
			first_column = """ s.`perumahan` """
			group_clause = """ GROUP BY s.`perumahan` """
		
		year_clause = ""
		#if filters.get("fiscal_year") and not filters.get("period") == "Yearly" :
		#	year_clause = """ AND YEAR(s.`posting_date`)={0} """.format(filters.get("fiscal_year"))
		date_clause = ""
		if filters.get("from_date") and filters.get("to_date") :
			date_clause = """ AND s.`posting_date` BETWEEN "{0}" AND "{1}" """.format(filters.get("from_date"),filters.get("to_date"))
		

		
		to_sum = ""
		if filters.get("based_on") == "Qty" :
			to_sum = "1"
		elif filters.get("report_type") == "UTJ Pending" or filters.get("report_type") == "UTJ Batal" :
			to_sum = "s.`rabat_1`"
		else :
			to_sum = "s.`harga_jual`"
		
		workflow_clause = ""
		if filters.get("report_type") == "Else" :
			workflow_clause = """ AND s.`workflow_state` NOT IN ("UTJ Pending","UTJ Batal","Batal","Pindah Kavling")  """
		else :
			workflow_clause = """ AND s.`workflow_state`="{0}" """.format(filters.get("report_type"))
		
		#date_columns = ""
		#if not filters.get("period") == "Yearly" :
		#	begin_month = []
		#	end_month = []
		#	if filters.get("period") == "Monthly" :
		#		begin_month = [1,2,3,4,5,6,7,8,9,10,11,12]
		#		end_month = [1,2,3,4,5,6,7,8,9,10,11,12]
		#	elif filters.get("period") == "Quarterly" :
		#		begin_month = [1,4,7,10]
		#		end_month = [3,6,9,12]
		#	for i in range(0,len(begin_month)) :
		#		begin = begin_month[i]
		#		end = end_month[i]
		#		date_columns = """{0}, SUM(IF(MONTH(s.`posting_date`)>={1} AND MONTH(s.`posting_date`)<={2},{3},0))  """.format(date_columns,begin,end,to_sum)
		#else :
		#	result = frappe.db.sql(""" SELECT y.`name` FROM `tabFiscal Year`y """)
		#	for res in result :
		#		date_columns = """{0}, SUM(IF(YEAR(l.`creation`)={1},{2},0)) """.format(date_columns,res[0],to_sum)
		data = frappe.db.sql(""" SELECT {0} {1} FROM `tabSKPJB`s WHERE 1=1 {2} {3} {4}  """.format(first_column,date_columns,workflow_clause,year_clause,group_clause))
		
	return columns, data

def get_columns(filters):
	columns = []
	if filters.get("filter_by") == "Lead Source" :
		columns = ["Lead Source:Link/Lead Source:100"]
	elif filters.get("filter_by") == "Sales Person" :
		columns = ["Sales Person:Link/Sales Person:100"]
	elif filters.get("filter_by") == "Perumahan" :
		columns = ["Perumahan:Link/Perumahan:100"]
	
	date_columns = ""
	
	data_type = ""
	if filters.get("based_on") == "Qty":
		data_type = "Int"
	elif filters.get("based_on") == "Omzet" :
		data_type = "Currency"
		
	to_sum = ""
	if filters.get("based_on") == "Qty" :
		to_sum = "1"
	elif filters.get("report_type") == "UTJ Pending" or filters.get("report_type") == "UTJ Batal" :
		to_sum = "s.`rabat_1`"
	else :
		to_sum = "s.`harga_jual`"
		
	cur_date = filters.get("from_date")
	limit_date = filters.get("to_date")
	period = filters.get("period")
	while cur_date < limit_date :
		start_date = cur_date
		end_date = start_date
		if period == "Weekly" :
			end_date = frappe.utils.data.add_days(start_date,6)
		elif period == "Monthly" :
			end_date = frappe.utils.data.get_last_day(start_date)
		elif period == "Quarterly" :
			if end_date.split("-")[1] in ["01","04","07","10"] :
				end_date = frappe.utils.data.add_months(end_date,2)
			elif end_date.split("-")[1] in ["02","05","08","11"] :
				end_date = frappe.utils.data.add_months(end_date,1)
			end_date = frappe.utils.data.get_last_day(end_date)
		elif period == "Yearly" :
			end_year = start_date.split("-")[0]
			end_date = end_year + "-12-31"
		end_date = str(end_date)
		if end_date > limit_date :
			end_date = limit_date
		if filters.get("report_type") == "Lead" :
			date_columns = """ {0}, SUM(IF( DATE(l.`creation`) BETWEEN "{1}" AND "{2}",1,0 )) """.format(date_columns,start_date,end_date)
		else :
			date_columns = """ {0}, SUM(IF( s.`posting_date` BETWEEN "{1}" AND "{2}",{3},0 )) """.format(date_columns,start_date,end_date,to_sum)
		columns.append(end_date + ":" + data_type + ":100")
		cur_date = frappe.utils.data.add_days(end_date,1)
			
	return columns,date_columns