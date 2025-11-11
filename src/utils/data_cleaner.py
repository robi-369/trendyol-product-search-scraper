thondef clean_product_data(data):
    cleaned_data = []
    for product in data:
        cleaned_product = {key: value if value else "N/A" for key, value in product.items()}
        cleaned_data.append(cleaned_product)
    return cleaned_data