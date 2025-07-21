# Advanced Pricing Rules

This is a custom app for **ERPNext**, enhancing the standard pricing and discount mechanisms in sales-related documents.

## Features

This app provides the following enhancements:

1. **"Ignore Pricing Rules" checkbox**  
   Added at the Item level in the following documents:
   - Quotation
   - Sales Order
   - Sales Invoice
   - Delivery Note  
   When checked, pricing rules will be bypassed for that specific item.

2. **New pricing option: "Rate from Price List"**  
   Introduced in the `Rate or Discount` field of **Pricing Rule**.  
   When selected, a new field `Rate from Price List` appears, allowing the user to choose a specific **Price List** from which the item price should be fetched directly.

These improvements allow greater flexibility when applying pricing rules, overriding them per item and selectively using custom price lists.

## 📘 Use Case: Applying a Pricing Rule with "Rate from Price List"

This example demonstrates how to configure a dynamic pricing rule that fetches the rate from a specific price list when a quantity threshold is met.

### Step-by-Step

1. **Create Price List: `Standard Selling`**
   - Go to **Selling > Price List**
   - Click **Add Price List**
   - Set:
     - **Price List Name**: `Standard Selling`
     - **Selling**: ✔️
     - **Currency**: e.g., `EUR`
   - Save

2. **Create Price List: `Wholesale Selling`**
   - Repeat the steps above
   - Set **Price List Name**: `Wholesale Selling`

3. **Create an Item**
   - Go to **Stock > Item**
   - Click **Add Item**
   - Set:
     - **Item Code**: `ITEM-001`
     - **Item Name**: `Example Product`
   - Save

4. **Add Item Prices**
   - Go to **Stock > Item Price**
   - Create two records:
     - One for `Standard Selling` with rate `100 EUR`
     - One for `Wholesale Selling` with rate `80 EUR`

5. **Create a Pricing Rule**
   - Go to **Selling > Pricing Rule**
   - Click **Add Pricing Rule**
   - Set:
     - **Apply On**: `Item Code`
     - **Item Code**: `ITEM-001`
     - **Min Qty**: `10`
     - **Rate or Discount**: `Rate from Price List`
     - **Rate from Price List**: `Wholesale Selling`
   - Save and Submit

### ✅ Result

When adding `ITEM-001` to a **Sales Order**:

- If **Qty < 10**, the price will be taken from the `Standard Selling` price list
- If **Qty ≥ 10**, the price will be overridden using the rate from the `Wholesale Selling` price list

This allows you to define quantity-based pricing logic that pulls directly from different price lists.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app advanced_pricing_rules
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/advanced_pricing_rules
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
