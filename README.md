# FLEXT-Oracle-WMS

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Oracle-WMS** is the specialized framework for integrating with Oracle Warehouse Management Systems (WMS). It provides typed access to the LGF Cloud API, handling complex entities like inventory, shipments, and orders with enterprise reliability.

Part of the [FLEXT](https://github.com/flext/flext) ecosystem.

## 🚀 Key Features

- **LGF API Client**: Complete coverage of key WMS Cloud REST endpoints (v10+).
- **Entity Discovery**: Dynamic schema introspection for WMS entities and custom fields.
- **Authentication**: Secure support for OAuth2, Basic Auth, and IDCS integration.
- **Resilient Operations**: Built-in retry mechanisms, rate limiting, and circuit breakers.
- **FLEXT Integration**: Designed to work seamlessly with `flext-tap-oracle-wms` and `flext-monitor`.

## 📦 Installation

Install via Poetry:

```bash
poetry add flext-oracle-wms
```

## 🛠️ Usage

### Client Setup

Initialize the client with your WMS instance details:

```python
from flext_oracle_wms import FlextOracleWmsClient, WmsSettings

config = WmsSettings(
    base_url="https://wms-test.oraclecloud.com",
    username="api_user",
    password="super_secure_password"
)

client = FlextOracleWmsClient(config)
```

### Fetching Inventory

Retrieve inventory snapshots with filters:

```python
result = client.inventory.list(
    warehouse="WH1",
    item_code="SKU-12345",
    quantity__gt=0
)

if result.is_success:
    for item in result.value:
        print(f"Location: {item.location}, Qty: {item.quantity}")
```

### Creating an Order

Submit a new outbound order to the WMS:

```python
order = {
    "order_nbr": "OUT-999",
    "facility_code": "FAC-01",
    "order_type": "SALES",
    "ship_to_name": "ACME Corp"
}

response = client.orders.create(payload=order)
if response.is_success:
    print(f"Order Created: {response.value.id}")
```

## 🏗️ Architecture

This library serves as the WMS domain layer:

- **API Mapping**: Maps complex LGF endpoints to clean Python methods.
- **Data Models**: Pydantic models for strict typing of WMS entities.
- **Error Handling**: Standardized `FlextResult` wrapper for all API interactions.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on adding support for new API entities.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
