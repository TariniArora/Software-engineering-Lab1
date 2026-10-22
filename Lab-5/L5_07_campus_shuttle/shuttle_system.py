
"""Manage campus shuttle routes, trip logs, and driver assignments."""

import json
import secrets
from datetime import datetime

MIN_CAPACITY = 10

INITIAL_ROUTES = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}

DRIVERS = ("Prakash", "Leela", "Imran", "Tom")


def add_trip_log(route_data, route_id, passenger_count, logs=None):
    """Record a valid passenger count for an existing route."""
    if route_id not in route_data:
        raise KeyError(f"Unknown route: {route_id}")

    if (
        isinstance(passenger_count, bool)
        or not isinstance(passenger_count, int)
        or passenger_count < 0
    ):
        raise ValueError("Passenger count must be a non-negative integer.")

    if logs is None:
        logs = []

    route_data[route_id]["trips"].append(passenger_count)
    timestamp = datetime.now().isoformat(timespec="seconds")
    logs.append(f"{timestamp}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_data, route_id):
    """Remove a route and report whether it existed."""
    return route_data.pop(route_id, None) is not None


def average_load(route_data, route_id):
    """Return a route's average passenger count, or None if unavailable."""
    if route_id not in route_data:
        return None

    trips = route_data[route_id]["trips"]
    if not trips:
        return None

    return sum(trips) / len(trips)


def underused_routes(route_data):
    """Return routes with recorded average loads below the minimum."""
    flagged = []

    for route_id in route_data:
        average = average_load(route_data, route_id)
        if average is not None and average < MIN_CAPACITY:
            flagged.append(route_id)

    return flagged


def assign_driver(route_id, route_data):
    """Assign a randomly selected driver to an existing route."""
    if route_id not in route_data:
        raise KeyError(f"Unknown route: {route_id}")

    return secrets.choice(DRIVERS)


def sync_fleet_data(file="fleet.json", route_data=None):
    """Save route data to JSON and return the data read back."""
    if route_data is None:
        route_data = INITIAL_ROUTES.copy()

    with open(file, "w", encoding="utf-8") as fleet_file:
        json.dump(route_data, fleet_file, indent=4)

    with open(file, "r", encoding="utf-8") as fleet_file:
        return json.load(fleet_file)


def main():
    """Run a demonstration of the campus shuttle system."""
    routes = {
        route_id: {
            "name": details["name"],
            "trips": details["trips"].copy(),
        }
        for route_id, details in INITIAL_ROUTES.items()
    }
    logs = []

    add_trip_log(routes, "R1", 32, logs)
    add_trip_log(routes, "R1", 28, logs)
    add_trip_log(routes, "R2", 4, logs)

    try:
        add_trip_log(routes, "R2", -6, logs)
    except ValueError as error:
        print("Rejected trip:", error)

    try:
        add_trip_log(routes, "R3", "full", logs)
    except ValueError as error:
        print("Rejected trip:", error)

    print("Driver for R1:", assign_driver("R1", routes))
    print("Underused:", underused_routes(routes))
    print("R1 average:", average_load(routes, "R1"))

    routes = sync_fleet_data(route_data=routes)

    remove_route(routes, "R3")
    choice = input("Route to look up (Enter for R2): ").strip() or "R2"

    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("Unknown route:", choice)

    print("R3 average:", average_load(routes, "R3"))


if __name__ == "__main__":
    main()
