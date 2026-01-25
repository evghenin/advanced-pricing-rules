import frappe
from erpnext.accounts.doctype.pricing_rule.utils import _get_pricing_rules
from erpnext.stock.get_item_details import get_price_list_rate_for

def _get_pricing_rules_patch(apply_on, args, values):
    pricing_rules = _get_pricing_rules(apply_on, args, values)

    for rule in pricing_rules:
        if rule.get('rate_or_discount') == 'Rate from Price List' and rule.get("custom_rate_from_price_list"):
            standard_rate = (
                args.get("price_list_rate")
                or args.get("base_price_list_rate")
                or 0
            )

            ctx = frappe._dict(
                {
                    "price_list": rule.get("custom_rate_from_price_list"),
                    "uom": args.get("uom"),
                    "transaction_date": args.get("transaction_date"),
                    "customer": args.get("customer"),
                    "supplier": args.get("supplier"),
                    "qty": args.get("qty"),
                }
            )

            alt_rate = get_price_list_rate_for(ctx, args.get("item_code")) or 0

            # Apply discount amount as positive difference when alt_rate is lower.
            discount_amount = max(0, float(standard_rate) - float(alt_rate))

            # Switch rule type to Discount Amount so ERPNext applies it correctly.
            rule["rate_or_discount"] = "Discount Amount"
            rule["discount_amount"] = discount_amount

    return pricing_rules