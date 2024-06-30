import asyncio
import logging

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from app.config import Config


class ForexFactoryScraperService:

    def __init__(self, url):
        self.url = url
        self.logger = logging.getLogger(__name__)
        self.logger.debug(self.url)

    def get_calendar(self):
        return asyncio.run(self.get_calendar_async())

    async def get_calendar_async(self):
        days_array = []
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True, devtools=False, chromium_sandbox=False)
                context = await browser.new_context()
                page = await context.new_page()

                await page.set_extra_http_headers(Config.EXTRA_HTTP_HEADERS)
                await page.goto(self.url, wait_until="domcontentloaded")

                # Add your scraping logic here using selectors or other methods
                try:
                    # Extract the calendar days state and array if they exist
                    data = await page.evaluate('''() => {
                        if (typeof window.calendarComponentStates === 'undefined') { return null }
                        const states = window.calendarComponentStates;
                        const daysArray = states[1]?.days || [];
                        return { states, daysArray };
                    }''')

                    if data and 'daysArray' in data:
                        days_array = data.get('daysArray')

                except PlaywrightTimeoutError as e:
                    dd = f'Failed to load the calendar: {str(e)}'
                    logging.error(dd)

                # await page.wait_for_timeout(30000)  # in milliseconds
        except Exception as e:
            dd = f'An error occurred: {str(e)}'
            self.logger.error(dd)

        return days_array
