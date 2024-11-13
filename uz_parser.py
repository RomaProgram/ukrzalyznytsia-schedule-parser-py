from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import re

def parse_section(page, header_text):
    """
    Parses a specific section (Departures or Arrivals) from the schedule page.

    Args:
        page: The Playwright page object.
        header_text: The header text to locate the section (e.g., "Відправлення" or "Прибуття").

    Returns:
        A list of dictionaries containing the parsed schedule data.
    """
    section_data = []
    header_selector = f"h4:has-text('{header_text}')"
    header = page.query_selector(header_selector)
    if not header:
        print(f"Header for '{header_text}' not found.")
        return section_data

    # Assuming the next sibling is the table containing the schedule
    section_table = header.evaluate_handle("node => node.nextElementSibling")
    if not section_table:
        print(f"Table for '{header_text}' not found.")
        return section_data

    rows = section_table.query_selector_all("tr.StationBoardTableRow")

    for row in rows:
        # Extract train number
        train_number_elem = row.query_selector("td:nth-child(1) .Typography--monoText")
        train_number = train_number_elem.inner_text().strip() if train_number_elem else 'N/A'

        # Extract and format route
        route_elem = row.query_selector("td:nth-child(2) .Typography--monoText")
        route_text = route_elem.inner_text().strip() if route_elem else 'N/A'
        if "→" in route_text:
            from_location, to_location = map(str.strip, route_text.split("→", 1))
        else:
            from_location, to_location = route_text, "Unknown"
        formatted_route = f"from {from_location} to {to_location}"

        # Extract scheduled time
        scheduled_time_elem = row.query_selector("td:nth-child(3) .Typography--monoText")
        scheduled_time = scheduled_time_elem.inner_text().strip() if scheduled_time_elem else 'N/A'

        # Extract delay information
        delay_elem = row.query_selector("td:nth-child(2) .Typography--monoText + .Typography--monoText")
        delay_text = delay_elem.inner_text().strip() if delay_elem else ''
        delay_match = re.search(r"(\d+)\s?хв", delay_text)
        delay_minutes = int(delay_match.group(1)) if delay_match else None
        time_with_delay = f"{scheduled_time} (Delayed by {delay_minutes} min)" if delay_minutes else scheduled_time

        # Extract platform information
        platform_elem = row.query_selector("td:nth-child(4) .Typography--captionBold, td:nth-child(4) .Typography--monoText")
        platform = platform_elem.inner_text().strip() if platform_elem else '-'

        # Append the parsed data
        section_data.append({
            "trainNumber": train_number,
            "from": from_location,
            "to": to_location,
            "route": formatted_route,
            "scheduledTime": time_with_delay,
            "platform": platform
        })

    return section_data

def scrape_data(station_name):
    """
    Scrapes the departure and arrival schedule for a given train station.

    Args:
        station_name: The name of the train station to scrape data for.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        page.goto("https://booking.uz.gov.ua/schedule")

        try:
            # Wait for the main header to ensure the page has loaded
            page.wait_for_selector("h3", timeout=10000)  # 10 seconds timeout
        except PlaywrightTimeoutError:
            print("Error: The schedule page did not load properly.")
            browser.close()
            return

        if station_name != "Київ-Пас":
            try:
                # Click the "Change" button to select a different station
                page.click("button:has-text('Змінити')")

                # Wait for the search input to appear and fill it
                search_input = page.wait_for_selector("input[type='text']", timeout=5000)
                search_input.fill(station_name)

                # Wait for the suggestion list to appear and select the station
                suggestion_selector = f"li:has-text('{station_name}')"
                station_option = page.wait_for_selector(suggestion_selector, timeout=5000)
                station_option.click()

                # Wait for the network to be idle, indicating that the schedule has updated
                page.wait_for_load_state('networkidle', timeout=10000)
            except PlaywrightTimeoutError:
                print(f"Error: Unable to select station '{station_name}'. Please check the station name and try again.")
                browser.close()
                return

        # Parse departures and arrivals
        departures = parse_section(page, "Відправлення")
        arrivals = parse_section(page, "Прибуття")

        # Display the parsed data
        if departures:
            print(f"\nDepartures from {station_name}:")
            for dep in departures:
                print(dep)
        else:
            print(f"\nNo departure data found for {station_name}.")

        if arrivals:
            print(f"\nArrivals at {station_name}:")
            for arr in arrivals:
                print(arr)
        else:
            print(f"\nNo arrival data found for {station_name}.")

        # Clean up
        browser.close()

def main():
    station = input("Enter train station: ").strip()
    if not station:
        print("Error: Station name cannot be empty.")
        return
    scrape_data(station)

if __name__ == "__main__":
    main()
