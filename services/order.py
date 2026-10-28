from django.db import transaction

from db.models import Order, Ticket

from django.contrib.auth import get_user_model
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str | None = None) -> None:
    user_model = get_user_model()
    user = user_model.objects.get(username=username)

    if date is not None:
        order = Order.objects.create(created_at=date, user=user)
    else:
        order = Order.objects.create(user=user)

    for ticket in tickets:
        Ticket.objects.create(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
