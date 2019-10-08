# Customer
## [GET] /customer/{email}/

### Response
```json
{
    "name": "Bruce Dicknson",
    "email": "bruce@ironmaiden.com",
    "id": 1
}
```

## [POST] /customer/{email}/

### Request
```json
{
    "name": "Bruce Dicknson"
}
```

### Response
```json
{
    "name": "Bruce Dicknson",
    "email": "bruce@ironmaiden.com",
    "id": 1
}
```

## [PUT] /customer/{email}/

### Request
```json
{
    "name": "Bruce Dicknson"
}
```

## [DELETE] /customer/{email}/

# Customer wishlist
## [GET] /customer/{email}/wishlist/

### Response
```json
[
    {
        "customer": "bruce@ironmaiden.com",
        "product": {
            "price": 1699.0,
            "image": "http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg",
            "brand": "bébé confort",
            "id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f",
            "title": "Cadeira para Auto Iseos Bébé Confort Earth Brown"
        }
    }
]
```

## [POST] /customer/{email}/wishlist/

### Request
```json
{
    "product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
}
```

### Response
```json
{
    "customer": "bruce@ironmaiden.com",
    "product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
}
```