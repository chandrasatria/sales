# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext.controllers.trends import get_period_date_ranges, get_period_month_ranges

def execute(filters=None):
	columns, data = [], []
	
	columns = get_columns(filters)
	cost_centers = get_cost_centers(filters)
	period_month_ranges = get_period_month_ranges(filters["period"], filters["fiscal_year"])
	
	begin_month = []
	end_month = []
	if filters.get("period") == "Monthly" :
		begin_month = [1,2,3,4,5,6,7,8,9,10,11,12]
		end_month = [1,2,3,4,5,6,7,8,9,10,11,12]
	elif filters.get("period") == "Quarterly" :
		begin_month = [1,4,7,10]
		end_month = [3,6,9,12]
	elif filters.get("period") == "Half-Yearly" :
		begin_month = [1,7]
		end_month = [6,12]
	elif filters.get("period") == "Yearly" :
		begin_month = [1]
		end_month = [12]
	
	cc_columns = ""
	gle_columns = ""
	skpjb_columns = ""
	for i in range(0,len(begin_month)) :
		begin = begin_month[i]
		end = end_month[i]
		cc_columns = """{0}, IFNULL(gle.`biaya_{1}`,0), IFNULL(skpjb.`omzet_{1}`,0) """.format(cc_columns,begin)
		gle_columns = """{0}, SUM(IF(MONTH(gle.`posting_date`)>={1} AND MONTH(gle.`posting_date`)<={2},gle.`debit`,0)) AS `biaya_{1}` """.format(gle_columns,begin,end)
		skpjb_columns = """{0}, SUM(IF(MONTH(skpjb.`posting_date`)>={1} AND MONTH(skpjb.`posting_date`)<={2},skpjb.`harga_jual`,0)) AS `omzet_{1}` 
			""".format(skpjb_columns,begin,end)
		
		
	
	data = frappe.db.sql(""" 
		SELECT cc.`name` {0} FROM `tabCost Center`cc 
		LEFT JOIN 
		(
			SELECT gle.`cost_center` {1} FROM `tabGL Entry`gle
			#WHERE gle.`fiscal_year`="{3}" AND gle.`company`="{4}"
			GROUP BY gle.`cost_center`
		)gle ON gle.`cost_center` = cc.`name`
		LEFT JOIN
		(
			SELECT cc.`name` {2} FROM `tabSKPJB`skpjb JOIN `tabKavling`k ON k.`name`=skpjb.`kavling`
			JOIN `tabCost Center`cc 
			ON cc.`company` = k.`company` 
			AND cc.`lead_source`=skpjb.`lead_source`
			WHERE k.`company`="{4}" AND YEAR(skpjb.`posting_date`)={3} AND skpjb.`docstatus`=1 
		)skpjb ON skpjb.`name`=cc.`name`
		WHERE cc.`company` ="{4}"
		
		""".format(cc_columns,gle_columns,skpjb_columns,filters.get("fiscal_year"),filters.get("company")))
		

	return columns, data
	
def get_columns(filters):
	columns = ["Cost Center:Link/Cost Center:120"]

	arr_month = []
	if filters.get("period") == "Monthly" :
		arr_month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	elif filters.get("period") == "Quarterly" :
		arr_month = ["Jan-Mar","Apr-Jun","Jul-Sep","Oct-Dec"]
	elif filters.get("period") == "Half-Yearly" :
		arr_month = ["Jan-Jun","Jul-Dec"]
	elif filters.get("period") == "Yearly" :
		arr_month = ["Jan-Dec"]
	
	for month in arr_month :
		str_month = "(" + month + ")"
		columns.append("Biaya "+str_month+":Currency:100")
		columns.append("Omzet "+str_month+":Currency:100")
	
	return columns
	
def get_cost_centers(filters):
	
	return frappe.db.sql_list("""select name from `tabCost Center` where company="{0}" 
		order by lft """.format(filters.get("company")))
		
