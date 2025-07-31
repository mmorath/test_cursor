# File: backend/app/services/logistics_service.py
# Path: backend/app/services/logistics_service.py

"""
Core logistics management service.
"""

import logging
from typing import List, Dict, Any, Optional
from collections import defaultdict

from ..models import (
    Article,
    Project,
    PickingOrder,
    Picker,
    MaterialCart,
    StatusEnum,
)

logger = logging.getLogger(__name__)


class LogisticsService:
    """Core logistics management service."""

    def __init__(self):
        """Initialize the logistics service."""
        self.orders: List[PickingOrder] = []
        self.pickers: List[Picker] = []
        self.carts: List[MaterialCart] = []

    def add_order(self, order: PickingOrder) -> None:
        """Add a new picking order."""
        self.orders.append(order)
        logger.info(f"Added order {order.order_id}")

    def assign_order_to_picker(self, order_id: str, picker_id: str) -> bool:
        """Assign an order to a picker."""
        order = self.get_order_by_id(order_id)
        picker = self.get_picker_by_id(picker_id)

        if not order or not picker:
            logger.warning(f"Order {order_id} or picker {picker_id} not found")
            return False

        if order.status != StatusEnum.OFFEN:
            logger.warning(f"Order {order_id} is not open for assignment")
            return False

        if picker.current_order:
            logger.warning(f"Picker {picker_id} already has an active order")
            return False

        order.assigned_picker = picker_id
        order.status = StatusEnum.IN_BEARBEITUNG
        picker.current_order = order_id

        logger.info(f"Assigned order {order_id} to picker {picker_id}")
        return True

    def assign_cart_to_picker(self, picker_id: str, cart_id: str) -> bool:
        """Assign a material cart to a picker."""
        picker = self.get_picker_by_id(picker_id)
        cart = self.get_cart_by_id(cart_id)

        if not picker or not cart:
            logger.warning(f"Picker {picker_id} or cart {cart_id} not found")
            return False

        if not cart.is_available:
            logger.warning(f"Cart {cart_id} is not available")
            return False

        cart.assigned_picker = picker_id
        cart.is_available = False

        logger.info(f"Assigned cart {cart_id} to picker {picker_id}")
        return True

    def pick_article(
        self, order_id: str, article_id: str, quantity: int, picker_id: str
    ) -> bool:
        """Record picking of an article."""
        order = self.get_order_by_id(order_id)
        if not order:
            logger.warning(f"Order {order_id} not found")
            return False

        article = self.get_article_by_id(order.project, article_id)
        if not article:
            logger.warning(
                f"Article {article_id} not found in order {order_id}"
            )
            return False

        if article.status != StatusEnum.OFFEN:
            logger.warning(f"Article {article_id} is not open for picking")
            return False

        if quantity > article.menge:
            logger.warning(
                "Picking quantity %d exceeds required %d",
                quantity,
                article.menge,
            )
            return False

        # Update article status
        if quantity == article.menge:
            article.status = StatusEnum.ABGESCHLOSSEN
        else:
            article.status = StatusEnum.IN_BEARBEITUNG

        article.anzahl_auf_wagen = quantity
        article.kommisionierer = picker_id
        article.anzahl_aktion += 1

        # Update picker statistics
        picker = self.get_picker_by_id(picker_id)
        if picker:
            picker.total_picks_today += 1

        logger.info(
            f"Picked {quantity} of article {article_id} from order {order_id}"
        )
        return True

    def pick_article_by_position(
        self, order_id: str, position: int, quantity: int, picker_id: str
    ) -> bool:
        """Record picking of an article by position."""
        order = self.get_order_by_id(order_id)
        if not order:
            logger.warning(f"Order {order_id} not found")
            return False

        article = self.get_article_by_position(order.project, position)
        if not article:
            logger.warning(
                f"Article at position {position} not found in order {order_id}"
            )
            return False

        if article.status != StatusEnum.OFFEN:
            logger.warning(
                f"Article at position {position} is not open for picking"
            )
            return False

        if quantity > article.menge:
            logger.warning(
                f"Picking quantity {quantity} exceeds required {article.menge}"
            )
            return False

        # Update article status
        if quantity == article.menge:
            article.status = StatusEnum.ABGESCHLOSSEN
        else:
            article.status = StatusEnum.IN_BEARBEITUNG

        article.anzahl_auf_wagen = quantity
        article.kommisionierer = picker_id
        article.anzahl_aktion += 1

        # Update picker statistics
        picker = self.get_picker_by_id(picker_id)
        if picker:
            picker.total_picks_today += 1

        logger.info(
            f"Picked {quantity} of article {article.artikel} (pos {position}) from order {order_id}"
        )
        return True

    def complete_order(self, order_id: str) -> bool:
        """Mark an order as completed."""
        order = self.get_order_by_id(order_id)
        if not order:
            return False

        # Check if all articles are completed
        completed_articles = len(
            [
                a
                for a in order.project.articles
                if a.status == StatusEnum.ABGESCHLOSSEN
            ]
        )
        total_articles = len(order.project.articles)

        if completed_articles < total_articles:
            logger.warning(
                f"Order {order_id} is not complete: "
                f"{completed_articles}/{total_articles} articles"
            )
            return False

        order.status = StatusEnum.ABGESCHLOSSEN

        # Release picker and cart
        if order.assigned_picker:
            picker = self.get_picker_by_id(order.assigned_picker)
            if picker:
                picker.current_order = None

        logger.info(f"Completed order {order_id}")
        return True

    def get_order_by_id(self, order_id: str) -> Optional[PickingOrder]:
        """Get order by ID."""
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def get_picker_by_id(self, picker_id: str) -> Optional[Picker]:
        """Get picker by ID."""
        for picker in self.pickers:
            if picker.picker_id == picker_id:
                return picker
        return None

    def get_cart_by_id(self, cart_id: str) -> Optional[MaterialCart]:
        """Get cart by ID."""
        for cart in self.carts:
            if cart.cart_id == cart_id:
                return cart
        return None

    def get_article_by_id(
        self, project: Project, article_id: str
    ) -> Optional[Article]:
        """Get article by ID from a project."""
        for article in project.articles:
            if article.artikel == article_id:
                return article
        return None

    def get_article_by_position(
        self, project: Project, position: int
    ) -> Optional[Article]:
        """Get article by position from a project."""
        for article in project.articles:
            if article.position == position:
                return article
        return None

    def get_open_orders(self) -> List[PickingOrder]:
        """Get all open orders."""
        return [
            order for order in self.orders if order.status == StatusEnum.OFFEN
        ]

    def get_orders_by_picker(self, picker_id: str) -> List[PickingOrder]:
        """Get orders assigned to a specific picker."""
        return [
            order
            for order in self.orders
            if order.assigned_picker == picker_id
        ]

    def get_available_carts(self) -> List[MaterialCart]:
        """Get all available carts."""
        return [cart for cart in self.carts if cart.is_available]

    def get_orders_by_priority(self) -> List[PickingOrder]:
        """Get orders sorted by priority."""
        return sorted(self.orders, key=lambda x: x.priority, reverse=True)

    def calculate_route_optimization(self, order: PickingOrder) -> List[str]:
        """Calculate optimal picking route for an order."""
        locations = [article.lagerplatz for article in order.project.articles]

        # Group by zone and sort within zones
        zone_groups = defaultdict(list)
        for location in locations:
            zone = location[:3] if len(location) >= 3 else location
            zone_groups[zone].append(location)

        # Sort locations within each zone
        for zone in zone_groups:
            zone_groups[zone].sort()

        # Combine zones in logical order
        optimized_route = []
        for zone in sorted(zone_groups.keys()):
            optimized_route.extend(zone_groups[zone])

        return optimized_route

    def get_system_overview(self) -> Dict[str, Any]:
        """Get system overview statistics."""
        total_articles = sum(
            len(order.project.articles) for order in self.orders
        )
        picked_articles = sum(
            len(
                [
                    a
                    for a in order.project.articles
                    if a.status == StatusEnum.ABGESCHLOSSEN
                ]
            )
            for order in self.orders
        )

        return {
            "total_orders": len(self.orders),
            "open_orders": len(self.get_open_orders()),
            "completed_orders": len(
                [
                    o
                    for o in self.orders
                    if o.status == StatusEnum.ABGESCHLOSSEN
                ]
            ),
            "total_articles": total_articles,
            "picked_articles": picked_articles,
            "total_weight": sum(
                order.project.total_weight for order in self.orders
            ),
            "active_pickers": len(
                [p for p in self.pickers if p.current_order]
            ),
            "available_carts": len(self.get_available_carts()),
            "completion_rate": (
                (
                    len(
                        [
                            o
                            for o in self.orders
                            if o.status == StatusEnum.ABGESCHLOSSEN
                        ]
                    )
                    / len(self.orders)
                    * 100
                )
                if self.orders
                else 0
            ),
            "efficiency_score": (
                (picked_articles / total_articles * 100)
                if total_articles > 0
                else 0
            ),
        }


# EOF
