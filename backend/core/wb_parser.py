import requests
from loguru import logger
from pydantic import ValidationError

from .exceptions import WbApiError
from .models import Product
from .schemas import WbProductRawSchema


def fetch_wb_products(
    query: str, page: int = 1, limit: int = 50, dest: int = 12358595
) -> list[WbProductRawSchema]:
    url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
    params = {
        "query": query,
        "page": page,
        "limit": limit,
        "resultset": "catalog",
        "dest": dest
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url, params=params, headers=headers, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logger.debug(data)
        products_raw = data.get("data", {}).get("products", [])
        return [WbProductRawSchema(**p) for p in products_raw]

    except ValidationError as e:
        logger.warning("Validation error in data from WB: %s", e)
        raise WbApiError(
            "Invalid data received from WB API"
        ) from e

    except (requests.RequestException, ValueError) as e:
        logger.error("Request to WB API failed: %s", e)
        raise WbApiError(
            "Failed to fetch data from WB API"
        ) from e


def parse_and_save_products(query: str) -> int:
    products = fetch_wb_products(query)

    created = 0
    for product in products:
        obj, _ = Product.objects.update_or_create(
            name=product.name,
            defaults={
                "price": product.priceU // 100,
                "discount_price": product.salePriceU // 100,
                "rating": product.rating,
                "reviews_count": product.feedbacks,
            }
        )
        created += 1

    return created
