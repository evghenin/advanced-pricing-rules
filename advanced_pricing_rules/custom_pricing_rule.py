import copy
import json
import frappe
from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_price_discount_rule
from erpnext.accounts.doctype.pricing_rule.utils import get_pricing_rules
from erpnext.stock.get_item_details import get_price_list_rate_for

@frappe.whitelist()
def apply_price_discount_rule_patch(pricing_rule, item_details, args=None):
    if 'advanced_pricing_rules' in frappe.get_installed_apps():
        cpr = copy.copy(pricing_rule);
        if cpr.get("rate_or_discount") == "Rate from Price List" and cpr.get("custom_rate_from_price_list"):
            ctx = frappe._dict(
                {
                    "price_list": cpr.get("custom_rate_from_price_list"),
                    "uom": args.get("uom"),
                    "transaction_date": args.get("transaction_date"),
                    "customer": args.get("customer"),
                    "supplier": args.get("supplier"),
                    "qty": args.get("qty"),
                }
            )

            cpr.rate_or_discount = "Rate"
            cpr.rate = get_price_list_rate_for(ctx, args.get("item_code"))

    return apply_price_discount_rule(cpr, item_details, args)
