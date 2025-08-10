from playwright.async_api import Page, expect
from time import sleep
from pydantic_ai.tools import RunContext
from config import b64, Item, Profile_agent
from dataclasses import dataclass
from typing import List, Dict


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
    sleep(4)
    form = page.locator("form")
    button = page.locator("form").locator("button")
    # with open('/mnt/a/projects/python/oracle_automation/form_html.txt', 'a') as file:
    #     file.write(await form.inner_html())
    #     file.write("\n")
    #     file.write("\n")
    #     file.write("next page of form from here\n")
    #     file.write("\n")
    #     file.write("\n")
    #     file.write("\n")
    print(button)
    return await form.inner_html()


async def click_next_button(page: Page):
    form = page.locator("form")
    next_button = form.locator("button[type='submit']")
    print(f"next_button {next_button}")
    if await next_button.count() > 0:
        async with page.expect_navigation():
            await next_button.first.click()
    else:
        print("button submit not found")
        buttons = await form.locator("button").all()
        # print(f"next_button {buttons}")
        for button in buttons:
            # print(f"button value {await button.text_content()}")
            button_text = await button.text_content()
            if button_text is None:
                continue
            if button_text.strip() == "Next":
                async with page.expect_navigation():
                    await button.click()
            elif button_text.strip() == "Submit":
                async with page.expect_navigation():
                    await button.click()
                    
@Profile_agent.tool
async def get_education_fields(ctx: RunContext[Page], apply_flow_block_id: str) -> str:
    print(f"called the tool for the get field of the education field with id {apply_flow_block_id}")
    article = ctx.deps.locator(f"apply-flow-block[id='{apply_flow_block_id}']")
    print("\n")
    print("\n")
    print("\n")
    print(f"inner html: {await article.inner_html()}")
    print("\n")
    print("\n")
    print("\n")
    delete_buttons = article.locator("button[title='Delete']")
    count = await delete_buttons.count()
    for i in range(count):
        await delete_buttons.nth(0).click()
        await ctx.deps.wait_for_timeout(500)
        # print(f"all delete_buttons that present {delete_buttons}")
        # for delete_button in delete_buttons:
        #     await delete_button.click()
        #     sleep(2)
    sleep(1)
    education_button = article.get_by_text("Add Education")
    await education_button.click()
    sleep(1)
    return await article.inner_html()

@Profile_agent.tool
async def enter_the_education_fields(ctx: RunContext[Page], fields: list[Item], apply_flow_block_id: str) -> str:
    print(f"call the tool for entering the data for the education field with fields {fields}")
    article = ctx.deps.locator(f"apply-flow-block[id='{apply_flow_block_id}']")
    for field in fields:
        if field.type == "combobox":
            print(f"Filling combobox field {field.label} with value: {field.answer}")
            combobox_elem = article.locator(f"input[id='{field.id}']")
            if await combobox_elem.count() > 0:
                await combobox_elem.first.fill(f"{field.answer}")
                sleep(3)
                await ctx.deps.keyboard.press("Enter")
                print(f"Filled combobox field {field.label} with value: {field.answer}")
    sleep(1)
    education_button = article.get_by_text("Add Education")
    await education_button.click()
    sleep(1)
    return "done"




async def enter_data(page: Page, fields: list[Item]):
    form = page.locator("form")
    for field in fields:
        if field.type == "text":
            print(f"Filling text field {field.label} with value: {field.answer}")
            input_elem = form.locator(f"input[id='{field.id}']")
            if await input_elem.count() > 0:
                await input_elem.first.fill(f"{field.answer}")
                print(f"Filled text field {field.label} with value: {field.answer}")
        elif field.type == "button":
            try:
                print(f"pressing the buttont with the text: {field.answer}")
                # button_elems = await form.get_by_text(f"{field.answer}").all()
                button_elems = form.get_by_label(f"{field.label}")
                button = button_elems.get_by_text(f"{field.answer}")
                await button.click()
            except:
                continue
        elif field.type == "email":
            print(f"Filling email field {field.label} with value: {field.answer}")
            email_elem = form.locator(f"input[id='{field.id}']")
            if await email_elem.count() > 0:
                try:
                    print(f"email that is there {await page.input_value(f"input[id='{field.id}']")}")
                    if await page.input_value(f"input[id='{field.id}']") == field.answer:
                        continue
                    await email_elem.first.fill(f"{field.answer}")
                    print(f"Filled email field {field.label} with value: {field.answer}")
                except:
                    continue
        elif field.type == "combobox":
            print(f"Filling combobox field {field.label} with value: {field.answer}")
            combobox_elem = form.locator(f"input[id='{field.id}']")
            if await combobox_elem.count() > 0:
                await combobox_elem.first.fill(f"{field.answer}")
                sleep(3)
                await page.keyboard.press("Enter")
                print(f"Filled combobox field {field.label} with value: {field.answer}")
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
                sleep(20)
                print(f"Uploaded file to field {field.label}: {field.answer}")
        elif field.type == "special_select":
            print(f"Setting special select field {field.label} with value: {field.answer}")
            special_select_elem = form.locator(f"span[id='{field.id}_fakeSelected_icimsDropdown']")
            if await special_select_elem.count() > 0:
                await special_select_elem.evaluate('(element, html) => element.innerHTML = html', field.answer)
                print(f"set special_select to field {field.label} with the valuse: {field.answer}")


@dataclass
class combobox_value:
    combobox_id: str
    dropdown_button_id: str

@Profile_agent.tool
async def get_combobox_values(ctx: RunContext[Page], ids: List[combobox_value]) -> Dict[str, List[str]]:
    """Get values of comboboxes for the given IDs by clicking dropdown buttons and extracting options."""
    print(f"Getting values for comboboxes with IDs: {[id.combobox_id for id in ids]}")
    values = {}
    
    for combo in ids:
        try:
            # Click the dropdown button to open options
            dropdown_button = ctx.deps.locator(f"button[id='{combo.dropdown_button_id}']")
            if await dropdown_button.count() > 0:
                await dropdown_button.click()
                sleep(4)
                
                # Wait for dropdown options to appear
                # Assuming the dropdown modal/container follows the pattern: {combobox_id}-cx-select_modal
                dropdown_modal = ctx.deps.locator(f"div[id='{combo.combobox_id}-cx-select__modal']")
                await dropdown_modal.wait_for(state="visible", timeout=5000)
                sleep(4)
                # print(f"inner_html {await dropdown_modal.inner_html()}")
                # sleep(30)
                
                # Get all option elements
                option_elements = await dropdown_modal.locator(f"span[class='cx-select__list-item--content']").all()
                
                # Extract text from all options
                option_values = []
                
                for options in option_elements:
                    option_text = await options.inner_html()
                    if option_text.strip():
                        option_values.append(option_text.strip())
                
                values[combo.combobox_id] = option_values
                
                # Close dropdown by clicking elsewhere or pressing Escape
                await ctx.deps.keyboard.press("Escape")
                
            else:
                print(f"Dropdown button with ID {combo.dropdown_button_id} not found")
                values[combo.combobox_id] = []
                
        except Exception as e:
            print(f"Error getting values for combobox {combo.combobox_id}: {e}")
            values[combo.combobox_id] = []

    print(f"the value that are geted from the combobox {values}") 
    return values
