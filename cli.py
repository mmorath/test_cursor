"""
Command Line Interface for Logistics Management System.
"""

import click
import json
import sys
from pathlib import Path

from app.data_loader import DataLoader
from app.core import LogisticsManager
from app.models import Picker, MaterialCart, StatusEnum
from config import settings


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Logistics Management System CLI."""
    pass


@cli.command()
@click.option('--data-dir', default='docs/data', help='Data directory path')
def validate(data_dir):
    """Validate data files and structure."""
    click.echo("Validating data files...")

    try:
        loader = DataLoader(data_dir)

        # Load and validate CSV data
        csv_articles = loader.parse_csv_articles()
        click.echo(f"✓ Loaded {len(csv_articles)} articles from CSV")

        # Load and validate JSON data
        json_projects = loader.parse_json_projects()
        click.echo(f"✓ Loaded {len(json_projects)} projects from JSON")

        # Validate data consistency
        validation_report = loader.validate_data_consistency(csv_articles)

        click.echo("\nValidation Report:")
        click.echo(f"  Total Articles: {validation_report['total_articles']}")
        click.echo(f"  Valid Articles: {validation_report['valid_articles']}")
        click.echo(f"  Invalid Articles: {validation_report['invalid_articles']}")
        click.echo(f"  Missing Stock: {validation_report['missing_stock']}")
        click.echo(f"  Weight Issues: {validation_report['weight_issues']}")

        click.echo("\n✓ Data validation completed successfully")

    except Exception as e:
        click.echo(f"✗ Validation failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--data-dir', default='docs/data', help='Data directory path')
@click.option('--output', default='processed_orders.json', help='Output file name')
def process(data_dir, output):
    """Process data and create picking orders."""
    click.echo("Processing data...")

    try:
        loader = DataLoader(data_dir)
        projects = loader.parse_json_projects()
        orders = loader.create_picking_orders(projects)

        # Export processed data
        loader.export_processed_data(orders, output)

        click.echo(f"✓ Processed {len(orders)} orders")
        click.echo(f"✓ Exported to {output}")

    except Exception as e:
        click.echo(f"✗ Processing failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--data-dir', default='docs/data', help='Data directory path')
def stats(data_dir):
    """Show system statistics."""
    click.echo("Loading system data...")

    try:
        # Initialize system
        loader = DataLoader(data_dir)
        manager = LogisticsManager()

        # Load data
        projects = loader.parse_json_projects()
        orders = loader.create_picking_orders(projects)

        for order in orders:
            manager.add_order(order)

        # Add sample pickers and carts
        sample_pickers = [
            Picker(picker_id="P001", name="John Doe", employee_number="EMP001"),
            Picker(picker_id="P002", name="Jane Smith", employee_number="EMP002"),
            Picker(picker_id="P003", name="Bob Johnson", employee_number="EMP003")
        ]

        sample_carts = [
            MaterialCart(cart_id="C001", capacity=500.0),
            MaterialCart(cart_id="C002", capacity=750.0),
            MaterialCart(cart_id="C003", capacity=1000.0)
        ]

        manager.pickers.extend(sample_pickers)
        manager.carts.extend(sample_carts)

        # Get statistics
        stats = manager.get_system_overview()

        click.echo("\nSystem Statistics:")
        click.echo(f"  Total Orders: {stats['total_orders']}")
        click.echo(f"  Open Orders: {stats['open_orders']}")
        click.echo(f"  Completed Orders: {stats['completed_orders']}")
        click.echo(f"  Total Articles: {stats['total_articles']}")
        click.echo(f"  Picked Articles: {stats['picked_articles']}")
        click.echo(f"  Total Weight: {stats['total_weight']:.2f} kg")
        click.echo(f"  Active Pickers: {stats['active_pickers']}")
        click.echo(f"  Available Carts: {stats['available_carts']}")
        click.echo(f"  Completion Rate: {stats['completion_rate']:.1f}%")
        click.echo(f"  Efficiency Score: {stats['efficiency_score']:.1f}%")

    except Exception as e:
        click.echo(f"✗ Failed to load statistics: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('order_id')
@click.option('--data-dir', default='docs/data', help='Data directory path')
def order_info(order_id, data_dir):
    """Show detailed information about a specific order."""
    click.echo(f"Loading order {order_id}...")

    try:
        # Initialize system
        loader = DataLoader(data_dir)
        manager = LogisticsManager()

        # Load data
        projects = loader.parse_json_projects()
        orders = loader.create_picking_orders(projects)

        for order in orders:
            manager.add_order(order)

        # Get order
        order = manager.get_order_by_id(order_id)
        if not order:
            click.echo(f"✗ Order {order_id} not found", err=True)
            sys.exit(1)

        # Generate report
        report = manager.generate_picking_report(order_id)

        click.echo(f"\nOrder Information:")
        click.echo(f"  Order ID: {report['order_id']}")
        click.echo(f"  Project: {report['project_number']}")
        click.echo(f"  Status: {report['status']}")
        click.echo(f"  Completion: {report['completion_percentage']:.1f}%")
        click.echo(f"  Total Articles: {report['total_articles']}")
        click.echo(f"  Completed Articles: {report['completed_articles']}")
        click.echo(f"  Total Weight: {report['total_weight']:.2f} kg")
        click.echo(f"  Assigned Picker: {report['assigned_picker'] or 'None'}")

        click.echo(f"\nArticles:")
        for article in report['articles']:
            status_icon = "✓" if article['status'] == "Abgeschlossen" else "○"
            click.echo(f"  {status_icon} {article['artikel']} - {article['bezeichnung']}")
            click.echo(f"    Required: {article['required_quantity']}, "
                      f"Picked: {article['picked_quantity']}, "
                      f"Location: {article['location']}")

    except Exception as e:
        click.echo(f"✗ Failed to load order information: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('order_id')
@click.option('--data-dir', default='docs/data', help='Data directory path')
def route(order_id, data_dir):
    """Show optimized picking route for an order."""
    click.echo(f"Calculating route for order {order_id}...")

    try:
        # Initialize system
        loader = DataLoader(data_dir)
        manager = LogisticsManager()

        # Load data
        projects = loader.parse_json_projects()
        orders = loader.create_picking_orders(projects)

        for order in orders:
            manager.add_order(order)

        # Get order
        order = manager.get_order_by_id(order_id)
        if not order:
            click.echo(f"✗ Order {order_id} not found", err=True)
            sys.exit(1)

        # Calculate route
        route = manager.calculate_route_optimization(order)

        click.echo(f"\nOptimized Picking Route for Order {order_id}:")
        for i, location in enumerate(route, 1):
            click.echo(f"  {i:2d}. {location}")

    except Exception as e:
        click.echo(f"✗ Failed to calculate route: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--data-dir', default='docs/data', help='Data directory path')
def list_orders(data_dir):
    """List all orders with basic information."""
    click.echo("Loading orders...")

    try:
        # Initialize system
        loader = DataLoader(data_dir)
        manager = LogisticsManager()

        # Load data
        projects = loader.parse_json_projects()
        orders = loader.create_picking_orders(projects)

        for order in orders:
            manager.add_order(order)

        click.echo(f"\nOrders ({len(orders)} total):")
        click.echo(f"{'Order ID':<20} {'Project':<10} {'Status':<15} "
                  f"{'Articles':<8} {'Weight':<8} {'Priority':<8}")
        click.echo("-" * 80)

        for order in sorted(manager.orders, key=lambda x: x.order_id):
            status_icon = "✓" if order.status == StatusEnum.ABGESCHLOSSEN else "○"
            click.echo(f"{order.order_id:<20} {order.project.projekt_nr:<10} "
                      f"{status_icon} {order.status.value:<13} "
                      f"{len(order.project.articles):<8} "
                      f"{order.project.total_weight:<7.1f} "
                      f"{order.priority:<8}")

    except Exception as e:
        click.echo(f"✗ Failed to load orders: {e}", err=True)
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration."""
    click.echo("Current Configuration:")
    click.echo(f"  App Name: {settings.app_name}")
    click.echo(f"  Version: {settings.app_version}")
    click.echo(f"  Host: {settings.host}")
    click.echo(f"  Port: {settings.port}")
    click.echo(f"  Data Directory: {settings.data_directory}")
    click.echo(f"  Log Level: {settings.log_level}")
    click.echo(f"  Debug Mode: {settings.debug}")


if __name__ == '__main__':
    cli()