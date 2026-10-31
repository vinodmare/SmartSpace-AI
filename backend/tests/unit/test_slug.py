from app.utils.slug import slugify


def test_slugify() -> None:
    assert slugify("Luma Grand Hall!") == "luma-grand-hall"

