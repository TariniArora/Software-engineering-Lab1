def is_caught(basket_rect, obj):
    return (
        basket_rect.left <= obj.x <= basket_rect.right
        and basket_rect.top <= obj.y + obj.radius
        and obj.y - obj.radius <= basket_rect.bottom
    )