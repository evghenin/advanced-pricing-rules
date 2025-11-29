__version__ = "0.0.1"

import frappe
import erpnext.accounts.doctype.pricing_rule.pricing_rule as pricing_rule_module
import erpnext.accounts.doctype.pricing_rule.utils as pricing_rule_utils
import erpnext.stock.get_item_details as get_item_details
from advanced_pricing_rules.custom_pricing_rule import apply_price_discount_rule_patch

pricing_rule_module.apply_price_discount_rule = apply_price_discount_rule_patch
