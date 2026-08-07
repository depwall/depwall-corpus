---
name: vendor-widget-setup
description: Set up a vendor bot-protection widget for a site, then bind the widget to the deployed worker.
---

# Vendor widget setup

Provisions a bot-protection widget through the vendor API and wires it into the
project's deployed worker.

## Steps

1. Confirm the account id with the user.
2. Run `scripts/fetch-widget.sh --account-id <id> --sitekey <key>` to read the
   existing widget back, so an already-provisioned site is not clobbered.
3. Bind the returned values into the worker config and redeploy.

The script needs `VENDOR_API_TOKEN` in the environment. It is the user's own
vendor credential, used only against the vendor's own API endpoint.
