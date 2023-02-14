# PROGRAM IMPORTS
import re
import urllib.request as urllib_request
import customtkinter as ctk


'''

This program is designed to take a url from the user and scrape its contents for more urls, then scrape their contents, etc until it runs out o new urls to scrape.

Then takes all the text from the whole domain and dumps it into a regular expression before spitting out all emails and phone numbers it could find.

Designed to make it easier to find contact details for a business through difficult to navigate websites.

'''


# REGEX FILTER FOR WEBSITE TEXT
def regex_search(text):
	phoneRegex = re.compile(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}')
	emailRegex = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))')

	matches = []
	for groups in phoneRegex.findall(text):
		matches.append(groups)
	for groups in emailRegex.findall(text):
		matches.append(groups[0])

	if len(matches) > 0:
		results = '\n'.join(matches)
	else:
		results = "No contact details found on this site..."

	return results


# WEB SCRAPER FOR TEXT TO REGEX FILTER
def scrape_for_html(url: str):
  page = urllib_request.urlopen(url)
  html_raw = page.read()
  html = html_raw.decode("utf-8")

  # The below is excluded due to an exception being thrown...

  # urlRegex = re.compile(r'(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*))')

  # new_urls = []
  # new_urls = append_urls_if_not_present(urlRegex, new_urls, url, html)

  # if len(new_urls) > 0:
  #   html = iterate_new_urls(html, urlRegex, new_urls, url)

  return html


# ITERATES THROUGH SCRAPES OF URLS FOUND AND GRABS ALL TEXT FROM THE DOMAIN.
# def iterate_new_urls(html, urlRegex, new_urls, original_url):
#   for index in range(len(new_urls)):
#     new_page = urllib_request.urlopen(new_urls[index])
#     new_html_raw = new_page.read()
#     TODO Fix "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"
#     new_html = new_html_raw.decode("utf-8")
#     html = str(html).join('\n' + new_html)

#     new_urls = append_urls_if_not_present(urlRegex, new_urls, original_url, new_html)

#   return html


# FILTERS URLS ALREADY IN LIST FROM BEING ADDED INFINITELY.
# def append_urls_if_not_present(urlRegex, new_urls, original_url, html):
#   for groups in urlRegex.findall(html):
#     if groups not in new_urls:
#       if groups != original_url:
#         new_urls.append(groups)

#   return new_urls


# WINDOW FOR RESULTS DISPLAY
class URLScrapeResult(ctk.CTkToplevel):
  def __init__(self, url: str, results, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.title(f"Scrape Result: '{url}'")
    self.geometry("500x300")
    self.minsize(300, 200)

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.results = ctk.CTkTextbox(self)
    self.results.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    self.results.insert("0.0", results)

# FRAME FOR MAIN APP WINDOW WIDGETS
class MyFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)

    self.label = ctk.CTkLabel(self, text="Enter Website URL")
    self.label.pack(padx=20, pady=(20,10))

    self.entry = ctk.CTkEntry(self, placeholder_text="https://www.example.com/page", width=250)
    self.entry.pack(padx=20, pady=10)

    self.button = ctk.CTkButton(self, text="Scrape Site", command=self.submit_url)
    self.button.pack(padx=20, pady=(10,20))

    self.scrape_window = None

	# MAIN APP FUNCTION
  def submit_url(self):
    url = self.entry.get()

    # text_for_search = "This is a test message... 07952075867 is a phone nummber and hunter.oliver0512@gmail.com is an email."
    # - OLD TEST CODE
    text_for_search = scrape_for_html(url)

    regex_results = regex_search(text_for_search)

    if self.scrape_window is None or not self.scrape_window.winfo_exists():
      self.scrape_window = URLScrapeResult(url, regex_results)
    else:
      self.scrape_window.focus()


# MAIN APP WINDOW CLASS
class AppURLWindow(ctk.CTk):
  def __init__(self):
    super().__init__()
    self.title("URL Contact Scraper")
    self.geometry("400x200")
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.my_frame = MyFrame(master=self)
    self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    self.geometry("400x200")
    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.my_frame = MyFrame(master=self)
    self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


# RUN MAIN APP
app = AppURLWindow()
app.mainloop()