from challenge.extensions.catalog.http_client import get_product_by_id


async def build_wishlist_response(wishlist):
    return [
        {
            'customer': item.customer.email,
            'product': await get_product_by_id(item.product_id)
        }
        for item in wishlist
    ]
