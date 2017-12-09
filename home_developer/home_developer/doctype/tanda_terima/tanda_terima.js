// Copyright (c) 2017, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tanda Terima', {
	refresh: function(frm) {
		if(doc.workflow_state =="Booking Confirmed")) {
			cur_frm.add_custom_button(__('SKPJB'),
					this.make_skpjb, __("Make"));
			cur_frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	},make_skpjb: function() {
		frappe.model.open_mapped_doc({
			method: "home_developer.home_developer.doctype.tanda_terima.tanda_terima.make_skpjb",
			frm: cur_frm
		})
	}
});
