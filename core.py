from playwright.async_api import Page, Locator
from pydantic import BaseModel
import time

with open("/mnt/a/downloads/Lin_Mei_Experiened_Level_Software.pdf", "rb") as f:
    b64 = f.read()

class Item(BaseModel):
    label: str
    type: str
    id: str
    answer: str 


async def click_apply_button(page: Page):
    try:
        await page.get_by_role("button", name="Apply Now").first.wait_for(state="attached")
        apply_button = page.get_by_role("button", name="Apply Now").first
        print("Checking for 'Apply' button...")
        if await apply_button.count() > 0:
            async with page.expect_navigation():
                await apply_button.first.click()
                print("Clicked 'Apply' button")
        else:
            print("No 'Apply' button found")
    except Exception as e:
        print(f"Error clicking apply button: {e}")

async def click_accept_cookies(page: Page):
    try:
        await page.get_by_role("button", name="Accept").wait_for(state="attached")
        accept_button = page.get_by_role("button", name="Accept")
        print("Checking for 'Accept Cookies' button...")
        # await accept_button.wait_for(state="visible", timeout=5000)
        if await accept_button.count() > 0:
            async with page.expect_navigation():
                await accept_button.first.click()
                print("Accepted cookies")
        else:
            print("No 'Accept Cookies' button found")
    except Exception as e:
        print(f"Error accepting cookies: {e}")

async def extract_fields(page: Page):
    # await page.locator("form").wait_for(state="attached")
    form = page.locator("form")
    button = page.locator("form").locator("button")
    with open('/mnt/a/projects/python/oracle_automation/form_html.txt', 'a') as file:
        file.write(await form.inner_html())
        file.write("\n")
        file.write("\n")
        file.write("next page of form from here\n")
        file.write("\n")
        file.write("\n")
        file.write("\n")
    print(button)
    return await form.inner_html()


async def click_next_button(page: Page):
    form = page.locator("form")
    next_button = form.locator("button[type='submit']")
    if await next_button.count() > 0:
        print("Clicking 'Next' button to proceed to the next page...")
        async with page.expect_navigation():
            print("Next button found, clicking...")
            await next_button.first.click()
            print("Clicked 'Next' button")


async def enter_data(page: Page, fields: list[Item]):
    form = page.locator("form")
    for field in fields:
        if field.type == "text":
            print(f"Filling text field {field.label} with value: {field.answer}")
            input_elem = form.locator(f"input[id='{field.id}']")
            if await input_elem.count() > 0:
                await input_elem.first.fill(f"{field.answer}")
                print(f"Filled text field {field.label} with value: {field.answer}")
        elif field.type == "email":
            print(f"Filling email field {field.label} with value: {field.answer}")
            email_elem = form.locator(f"input[id='{field.id}']")
            if await email_elem.count() > 0:
                await email_elem.first.fill(f"{field.answer}")
                print(f"Filled email field {field.label} with value: {field.answer}")
        elif field.type == "multiselect":
            print(f"Filling multiselect field {field.label} with value: {field.answer}")
            select_elem = form.locator(f"select[multiple][id='{field.id}']")
            if await select_elem.count() > 0:
                options = select_elem.locator("option")
                for option in await options.all():
                    if await option.inner_text() in field.answer:
                        await option.set_checked(True)
                print(f"Selected options in multiselect field {field.label}: {field.answer}")
        elif field.type == "select":
            print(f"Filling select field {field.label} with value: {field.answer}")
            select_elem = form.locator(f"select[id='{field.id}']")
            if await select_elem.count() > 0:
                await select_elem.first.select_option(value=field.answer)
                print(f"Selected option in select field {field.label}: {field.answer}")
        elif field.type == "checkbox":
            print(f"Setting checkbox field {field.label} to: {field.answer}")
            checkbox_elem = form.locator(f"input[id='{field.id}']")
            if await checkbox_elem.count() > 0:
                print(f"Setting checkbox field {field.label} to: {field.answer}")
                # await checkbox_elem.set_checked(field.answer == "true")
                await checkbox_elem.first.dispatch_event("click")
                print(f"Set checkbox field {field.label} to: {field.answer}")
        elif field.type == "radio":
            print(f"Setting radio field {field.label} to: {field.answer}")
            radio_elems = form.locator(f"input[type='radio'][name='{field.id}']")
            for radio in await radio_elems.all():
                if await radio.get_attribute("value") == field.answer:
                    await radio.check()
                    print(f"Checked radio button in field {field.label} with value: {field.answer}")
        elif field.type == "date":
            print(f"Filling date field {field.label} with value: {field.answer}")
            date_elem = form.locator(f"input[type='date'][id='{field.id}']")
            if await date_elem.count() > 0:
                await date_elem.fill(field.answer)
                print(f"Filled date field {field.label} with value: {field.answer}")
        elif field.type == "file":
            print(f"Uploading file for field {field.label}")
            file_input = form.locator(f"input[type='file']")
            if await file_input.count() > 0:
                await file_input.first.set_input_files(files=[{"name": "resume.pdf", "mimeType": "application/pdf", "buffer": b64}])
                time.sleep(20)
                print(f"Uploaded file to field {field.label}: {field.answer}")
        elif field.type == "special_select":
            print(f"Setting special select field {field.label} with value: {field.answer}")
            special_select_elem = form.locator(f"span[id='{field.id}_fakeSelected_icimsDropdown']")
            if await special_select_elem.count() > 0:
                await special_select_elem.evaluate('(element, html) => element.innerHTML = html', field.answer)
                print(f"set special_select to field {field.label} with the valuse: {field.answer}")
