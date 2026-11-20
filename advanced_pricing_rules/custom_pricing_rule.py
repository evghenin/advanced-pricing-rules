import frappe
from erpnext.accounts.doctype.pricing_rule.utils import _get_pricing_rules
from erpnext.stock.get_item_details import get_price_list_rate_for

def _get_pricing_rules_patch(apply_on, args, values):
    pricing_rules = _get_pricing_rules(apply_on, args, values)
    applicable_rules = []

    for rule in pricing_rules:
        if rule.get("rate_or_discount") == "Rate from Price List" and rule.get("custom_rate_from_price_list"):
            alt_rate = _get_rate_from_price_list(rule, args)
            # No Item Price in the target list: drop the rule. Keeping it would
            # stamp pricing_rules on a line whose price never changed, and POS Next
            # then treats the line as a promotion and blocks a manual discount.
            if alt_rate is None:
                continue

            standard_rate = (
                args.get("price_list_rate")
                or args.get("base_price_list_rate")
                or 0
            )

            # Apply discount amount as positive difference when alt_rate is lower.
            rule["rate_or_discount"] = "Discount Amount"
            rule["discount_amount"] = max(0, float(standard_rate) - float(alt_rate))

        applicable_rules.append(rule)

    return applicable_rules


def _get_rate_from_price_list(rule, args):
    """Return the item rate from the rule's price list, or None when it has none."""
    ctx = frappe._dict(
        {
            "price_list": rule.get("custom_rate_from_price_list"),
            "uom": args.get("uom"),
            "stock_uom": args.get("stock_uom"),
            "conversion_factor": args.get("conversion_factor"),
            "transaction_date": args.get("transaction_date") or args.get("posting_date"),
            "customer": args.get("customer"),
            "supplier": args.get("supplier"),
            "qty": args.get("qty"),
            "batch_no": args.get("batch_no"),
        }
    )
    return get_price_list_rate_for(ctx, args.get("item_code"))