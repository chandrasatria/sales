# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "sales"
app_title = "Sales"
app_publisher = "Frappe"
app_description = "Sales"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/home_developer/css/home_developer.css"
# app_include_js = "/assets/home_developer/js/home_developer.js"

# include js, css files in header of web template
# web_include_css = "/assets/home_developer/css/home_developer.css"
# web_include_js = "/assets/home_developer/js/home_developer.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "home_developer.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "home_developer.install.before_install"
# after_install = "home_developer.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "home_developer.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

fixtures = [
	{"dt":"Print Format", "filters": {"doc_type": "SKPJB"}},
	{"dt":"Custom Field"}
]
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
	#	"before_cancel": "home_developer.home_developer.doctype.skjb.skjb.remove_from_skjb",
	#	"validate":"home_developer.home_developer.doctype.skjb.skjb.add_to_skjb"
# 		"on_cancel": "method",
# 		"on_trash": "method"
	},
	"Lead":{
		"validate":"sales.custom.check_stock"
	},
	"Customer":{
		"validate":"sales.custom.get_lead_source"
	}
 }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"home_developer.tasks.all"
# 	],
	"daily": [
#		"home_developer.home_developer.doctype.skjb.skjb.skjb_create_sales_invoice"
	],
# 	"hourly": [
# 		"home_developer.tasks.hourly"
# 	],
# 	"weekly": [
# 		"home_developer.tasks.weekly"
# 	]
# 	"monthly": [
# 		"home_developer.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "home_developer.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "home_developer.event.get_events"
# }
