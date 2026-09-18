# Test cases (written from a manual walkthrough of saucedemo.com)

All cases automated.

## Login (`/`)
| ID | Steps | Expected | Test |
|---|---|---|---|
| L1 | standard_user / secret_sauce | redirect to `/inventory.html` | ✅ `test_valid_login` |
| L2 | locked_out_user / secret_sauce | error "Sorry, this user has been locked out." | ✅ `test_locked_out_user` |
| L3 | standard_user / wrong | error "Username and password do not match any user in this service" | ✅ `test_wrong_password` |
| L4 | submit with both fields empty | error "Username is required" | ✅ `test_empty_fields` |
| L5 | username only, empty password | error "Password is required" | ✅ `test_empty_password` |
| L6 | performance_glitch_user | logs in but slowly (>5s) | ✅ `test_performance_glitch_user_logs_in` |

## Inventory (`/inventory.html`)
| ID | Steps | Expected | Test |
|---|---|---|---|
| I1 | click "Add to cart" on one item | cart badge shows 1, button becomes "Remove" | ✅ `test_add_one_item` |
| I2 | add two, remove one | badge shows 1 | ✅ `test_add_two_remove_one` |
| I3 | sort Name (A to Z) / (Z to A) | items alphabetically ordered / reversed | ✅ `test_sort_by_name` |
| I4 | sort Price (low to high) / (high to low) | prices ascending / descending | ✅ `test_sort_by_price` |
| I5 | click item name | item detail page, back button returns to list | ✅ `test_item_detail_and_back` |
| I6 | burger menu → Logout | back to login page | ✅ `test_logout` |

## Cart (`/cart.html`)
| ID | Steps | Expected | Test |
|---|---|---|---|
| C1 | add two items, open cart | both listed with name, price, qty 1 | ✅ `test_cart_shows_added_items` |
| C2 | click Remove on one | only the other remains | ✅ `test_remove_item_in_cart` |
| C3 | Continue Shopping | back to inventory, badge count preserved | ✅ `test_continue_shopping_preserves_cart` |
| C4 | Checkout with empty cart | proceeds to step one (site allows it) | ✅ `test_checkout_with_empty_cart_proceeds` |

## Checkout (`/checkout-step-one.html` → `-two` → `-complete`)
| ID | Steps | Expected | Test |
|---|---|---|---|
| K1 | fill first/last/zip, Continue, Finish | overview subtotal = sum of prices, total = subtotal + tax, "Thank you for your order!" | ✅ `test_full_checkout_flow` |
| K2 | empty first name | error "Error: First Name is required" | ✅ `test_missing_first_name_shows_error` |
| K3 | empty last name / empty zip | "Last Name is required" / "Postal Code is required" | ✅ `test_missing_field_shows_error` |
| K4 | Cancel on step one | back to cart, items intact | ✅ `test_cancel_on_step_one_returns_to_cart` |
| K5 | Cancel on overview | back to inventory | ✅ `test_cancel_on_overview_returns_to_inventory` |
| K6 | Back Home on complete page | inventory, cart badge cleared | ✅ `test_back_home_clears_cart` |

## Personas (`problem_user`, `error_user`, `visual_user`)
| ID | Steps | Expected | Test |
|---|---|---|---|
| P1 | each persona logs in | lands on inventory | ✅ `test_persona_can_log_in` |
| P2 | each persona adds one item | badge shows 1 | ✅ `test_persona_can_add_to_cart` |
| P3 | problem_user sorts Z-A | order unchanged (site bug) | ✅ xfail `test_problem_user_sort` |
| P4 | problem_user fills checkout info | last name dropped, stays on step one (site bug) | ✅ xfail `test_problem_user_checkout_info` |
| P5 | error_user sorts | "Sorting is broken!" alert (site bug) | ✅ xfail `test_error_user_sort` |
| P6 | error_user clicks Finish | nothing happens (site bug) | ✅ xfail `test_error_user_finish` |

## Visual (`tests/visual/`, Windows only)
| ID | Steps | Expected | Test |
|---|---|---|---|
| V1 | open login page, full-page screenshot | ≤2% pixels differ from `visual/baselines/login_page.png` | ✅ `test_login_page` |
| V2 | standard_user login, product grid loaded, screenshot | ≤2% pixels differ from `inventory_page.png` | ✅ `test_inventory_page` |
| V3 | add Backpack + Bike Light, open cart, screenshot | ≤2% pixels differ from `cart_page.png` (badge 2, two rows) | ✅ `test_cart_page_with_items` |
| V4 | visual_user login, inventory screenshot vs the standard_user `inventory_page.png` | layout broken: dog image, shifted cart icon/titles/button, random prices (site bug, ~3% changed) | ✅ xfail `test_visual_user_inventory_matches_standard` |

A pixel counts as changed only if any RGB channel differs by >32/255. Missing baseline → test skips after writing it; `--update-baselines` rewrites them. Skipped on Linux/macOS (font rendering; see README).

Known site bugs are `xfail(strict=True)`: a screenshot of the broken state is attached to the report, and the test turns red if saucedemo ever fixes it.
