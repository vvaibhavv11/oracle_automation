from playwright.async_api import async_playwright, Page
from playwright_stealth import Stealth
from pydantic_ai import Agent, BinaryContent
import asyncio
from core import click_accept_cookies, click_apply_button, extract_fields, enter_data, click_next_button
from config import Item, b64, Profile_agent
import time
import os

async def ask_ai(page:Page, fields: str, b64: bytes) -> list[Item]:
    """Ask the AI to fill the fields based on the resume."""
    response = await Profile_agent.run(
        [
            "You are given a resume and a json object of fields, fill the fields with the answers from the resume.",
            f"Here is the fields to fill: {fields}",
            "Here is the resume in base64 format:",
            BinaryContent(data=b64, media_type="application/pdf"),
        ],
        deps=page
    )
    print("AI response:", response.output)
    return response.output

async def wait_for_page_load(page: Page):
    try:
        await page.wait_for_load_state("load")
        time.sleep(4)
        # frame_locator = page.frame_locator("iframe#icims_content_iframe")
        await page.locator("form").wait_for(state="attached")
    except Exception as e:
        print(f"Error waiting for page load: {e}")

async def main():
    try:
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch_persistent_context(user_data_dir="/home/vaibhav/.config/chromium",headless=False,args=['--disable-blink-features=AutomationControlled'])
            page = await browser.new_page()
            job_url = f"{os.getenv('JOB_URL')}"
            await page.goto(job_url)
            await page.wait_for_load_state("load")
            await click_accept_cookies(page)
            await click_apply_button(page)
            while True:
                await wait_for_page_load(page)
                form_html = await extract_fields(page)
                # print("Extracted form HTML:", form_html)
                form_ans =  await ask_ai(page, form_html, b64)
                await enter_data(page, form_ans)
                await click_next_button(page)

            # time.sleep(20)
            await browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())