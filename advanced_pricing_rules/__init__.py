__version__ = "0.0.1"

import erpnext.accounts.doctype.pricing_rule.utils as pricing_rule_utils
from advanced_pricing_rules.custom_pricing_rule import _get_pricing_rules_patch

#pricing_rule_module.apply_price_discount_rule = apply_price_discount_rule_patch
pricing_rule_utils._get_pricing_rules = _get_pricing_rules_patch
