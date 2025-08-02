import copy
import json
import frappe
from frappe.utils import flt
from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule, get_pricing_rule_for_item, \
    apply_price_discount_rule
from erpnext.accounts.doctype.pricing_rule.utils import get_pricing_rules
from erpnext.stock.get_item_details import get_price_list_rate_for, get_item_price, apply_price_list_on_item, \
    get_item_details, process_args


@frappe.whitelist()
def apply_pricing_rule_patch(args, doc=None):
    if 'advanced_pricing_rules' in frappe.get_installed_apps():
        if getattr(args, "custom_ignore_pricing_rule", False):
            args.ignore_pricing_rule = 1

    return apply_pricing_rule(args, doc)


@frappe.whitelist()
def get_pricing_rule_for_item_patch(args, doc=None, for_validate=False, **kwargs):
    args_copy = copy.deepcopy(args)

    if 'advanced_pricing_rules' in frappe.get_installed_apps():
        if isinstance(doc, str):
            doc = json.loads(doc)

        if doc:
            doc = frappe.get_doc(doc)

        item_doc = next((item for item in doc.items if item.name == args_copy.child_docname), None)

        if getattr(item_doc, "custom_ignore_pricing_rule", False):
            args_copy.ignore_pricing_rule = 1

    return get_pricing_rule_for_item(args_copy, doc, for_validate, **kwargs)


@frappe.whitelist()
def apply_price_list_on_item_patch(args, doc=None):
    args_copy = copy.deepcopy(args)

    if 'advanced_pricing_rules' in frappe.get_installed_apps():
        if isinstance(doc, str):
            doc = json.loads(doc)

        if doc:
            doc = frappe.get_doc(doc)

        item_doc = next((item for item in doc.items if item.name == args_copy.child_docname), None)

        if getattr(item_doc, "custom_ignore_pricing_rule", False):
            args_copy.ignore_pricing_rule = 1

    return apply_price_list_on_item(args_copy, doc)


@frappe.whitelist()
def get_item_details_patch(args, doc=None, for_validate=False, overwrite_warehouse=True):
    args_copy = process_args(args)

    if 'advanced_pricing_rules' in frappe.get_installed_apps():
        if isinstance(doc, str):
            doc = json.loads(doc)

        if doc:
            doc = frappe.get_doc(doc)

        if getattr(args_copy, "child_docname", False):
            item_doc = next((item for item in doc.items if item.name == args_copy.child_docname), None)

            if getattr(item_doc, "custom_ignore_pricing_rule", False):
                args_copy.ignore_pricing_rule = 1

    return get_item_details(args_copy, doc, for_validate, overwrite_warehouse)


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
