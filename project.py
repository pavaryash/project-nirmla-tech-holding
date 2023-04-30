import requests
import xml.etree.ElementTree as ET

# retrieve orders from the storefront REST API
rest_url = 'https://example.com/orders'
rest_response = requests.get(rest_url)
orders = rest_response.json()

# transform orders to SOAP format
soap_orders = []
for order in orders:
    soap_order = ET.Element('Order')
    ET.SubElement(soap_order, 'ID').text = str(order['id'])
    ET.SubElement(soap_order, 'CustomerName').text = order['customer']['name']
    ET.SubElement(soap_order, 'CustomerEmail').text = order['customer']['email']
    for item in order['items']:
        soap_item = ET.SubElement(soap_order, 'Item')
        ET.SubElement(soap_item, 'SKU').text = item['sku']
        ET.SubElement(soap_item, 'Quantity').text = str(item['quantity'])
    soap_orders.append(soap_order)

# send orders to the fulfillment center SOAP API
soap_url = 'https://example.com/fulfillment'
headers = {'content-type': 'application/xml'}
for soap_order in soap_orders:
    soap_data = ET.tostring(soap_order)
    soap_response = requests.post(soap_url, data=soap_data, headers=headers)
    if soap_response.status_code != 200:
        # handle error or retry logic here
        pass

# handle response from the fulfillment center
fulfillment_response = soap_response.text
# transform fulfillment response back to REST format if necessary
