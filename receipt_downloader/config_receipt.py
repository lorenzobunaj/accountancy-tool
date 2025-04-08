def config_receipt(data, name, subject, date, amount):
    receipt_data = data["data"]

    receipt_data["visible_subject"] = subject
    receipt_data["amount_net"] = amount
    receipt_data["amount_gross"] = amount
    receipt_data["entity"]["name"] = name
    receipt_data["date"] = date

    item_data = receipt_data["items_list"][0]
    item_data["name"] = subject
    item_data["net_price"] = amount
    item_data["gross_price"] = amount
    item_data["amount_net"] = amount
    item_data["description"] = subject

    payment_data = receipt_data["payments_list"][0]
    payment_data["amount"] = amount
    payment_data["due_date"] = date
    payment_data["paid_date"] = date

    return data
