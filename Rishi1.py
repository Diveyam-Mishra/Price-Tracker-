from bs4 import BeautifulSoup
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go
from tkinter import simpledialog
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
def scrape_and_check(x,var_name,html_file_path='C:\\Users\\Asus\\Desktop\\Rishi\\downloaded_page.html', n=6,):
    global first_product_name
    download_html(x)
    with open(html_file_path, 'r') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    div_elements = soup.find_all('div', class_='dD8iuc')
    product_info_dict = {}
    for div in div_elements[:n]:
        div_text = ' '.join(div.stripped_strings)
        keywords = ['amazon', 'flipkart', 'croma','jiomart','from lotus electronics','samsung.com','reliance']
        found_keywords = [keyword for keyword in keywords if keyword in div_text.lower()]

        if found_keywords:
            product_name_div = div.find_previous_sibling('div', class_='rgHvZc')
            product_name = product_name_div.text.strip() if product_name_div else '(No product name found)'
            if first_product_name is None:
                first_product_name = product_name
                cleaned_product_name=first_product_name.split(" ")[0]
                first_product_name=cleaned_product_name
                if first_product_name in product_name:
                    print(f"{product_name}")
                    print(div_text)
                    product_price=div_text.split(".")[0]
                    cleaned = product_price.replace("₹", "").replace(",", "")
                    product_price=int(cleaned)
                    product_info_dict[product_name] = (product_price, var_name)
            else: 
                if first_product_name in product_name:
                    print(f"{product_name}")
                    print(div_text)
                    product_price=div_text.split(".")[0]
                    cleaned = product_price.replace("₹", "").replace(",", "")
                    product_price=int(cleaned)
                    product_info_dict[product_name] = (product_price, var_name)
                    all_product_info.update(product_info_dict)
    return product_info_dict
import requests
def download_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        with open("downloaded_page.html", "wb") as file:
            file.write(response.content)
        
    except requests.exceptions.RequestException as e:
        print("Error downloading HTML file:", e)
def clean_price_data(price_dict,tolerance_percent=0.17):
    total_price = sum(price[0] for price in price_dict.values())
    average_price = total_price / len(price_dict)
    min_price_threshold = (1 - 0.2) * average_price
    max_price_threshold = (1 + 0.2) * average_price
    adjusted_prices = {key: price for key, price in price_dict.items() if min_price_threshold <= price[0] <= max_price_threshold}  # Preserve entire tuple
    removed_items = {key: price for key, price in price_dict.items() if price[0] < min_price_threshold or price[0] > max_price_threshold}
    print(f"Adjusted prices for {len(adjusted_prices)} items:")
    for item, price in adjusted_prices.items():
        print(f"- {item}: {price[0]:.2f} (String Name: {price[1]})") 

    if removed_items:
        print(f"Removed {len(removed_items)} items outside price range:")
        for item, price in removed_items.items():
            print(f"- {item}: {price[0]:.2f} (outside {min_price_threshold:.2f}-{max_price_threshold:.2f} range) (String Name: {price[1]})")

    return adjusted_prices
p_name = simpledialog.askstring("Product Name", "Enter the product name :")

if p_name: 
    all_product_info = {}
    first_product_name = None
    name = p_name.replace(" ", "+")
Amazon_link="https://www.google.com/search?sca_esv=598437705&rlz=1C1RXQR_enIN1067IN1067&tbm=shop&sxsrf=ACQVn0_5yZbNELudH50Tz8xF9mOmSewt5w:1705268257052&q="+name+"&tbs=mr:1,merchagg:g140768507%7Cm141020976&sa=X&ved=0ahUKEwjg4NSl692DAxXGxDgGHRw9BTkQsysItAsoAA&biw=1536&bih=776&dpr=1.25"
scrape_and_check(Amazon_link,"Amazon",n=5)
Croma="https://www.google.com/search?sca_esv=598654967&rlz=1C1RXQR_enIN1067IN1067&tbm=shop&sxsrf=ACQVn09YteSFnGpZpQTiUGFK4ZD4TAuuMA:1705358533817&q="+name+"&tbs=mr:1,merchagg:m10736904&sa=X&ved=0ahUKEwiyjv3Mu-CDAxUzTmwGHSKdAwgQsysI7wkoAw&biw=1536&bih=776&dpr=1.25"
scrape_and_check(Croma,"Croma",n=3)
Jio="https://www.google.com/search?sca_esv=598654967&rlz=1C1RXQR_enIN1067IN1067&tbm=shop&sxsrf=ACQVn09oaWatVsDqFB9f9Gb0AU7wWYly-g:1705358903704&q="+name+"&tbs=mr:1,merchagg:g385715397%7Cm388119669&sa=X&ved=0ahUKEwjal639vOCDAxWPRmwGHWaiAu4QsysIrAsoFg&biw=1536&bih=776&dpr=1.25"
scrape_and_check(Jio,"Jio",n=4)
Lotus="https://www.google.com/search?sca_esv=598654967&rlz=1C1RXQR_enIN1067IN1067&tbm=shop&sxsrf=ACQVn0_cr6SibAyk5S96keG0DcwV_sEQhg:1705359357213&q="+name+"&tbs=mr:1,merchagg:m102111928&sa=X&ved=0ahUKEwiWn83VvuCDAxUWSWwGHeqJA08QsysIvQsoGA&biw=1536&bih=776&dpr=1.25"
scrape_and_check(Lotus,"Lotus",n=3)
Samsung="https://www.google.com/search?sca_esv=598654967&rlz=1C1RXQR_enIN1067IN1067&tbm=shop&sxsrf=ACQVn0-p9qcAI_AxdRURnCRH7K1gbJkfgQ:1705359747943&q="+name+"&tbs=mr:1,merchagg:g615260711%7Cm112558730&sa=X&ved=0ahUKEwjmx_WPwOCDAxXiwzgGHRzCAlwQsysI0wsoJw&biw=1536&bih=776&dpr=1.25"
scrape_and_check(Samsung,"Samung",n=3)
Digital="https://www.google.com/search?sca_esv=598654967&rlz=1C1RXQR_enIN1067IN1067&tbm=shop&sxsrf=ACQVn0_XDQnNbnGO5p88Sg8fg-AJuumnfA:1705360013965&q="+name+"&tbs=mr:1,merchagg:m120890194&sa=X&ved=0ahUKEwjmoOKOweCDAxUk7zgGHVCzDfYQsysIoAUoBg&biw=1536&bih=776&dpr=1.25"
scrape_and_check(Digital,"Reliance-Digital",n=5)
d = clean_price_data(all_product_info)
print(d)

product_names = list(d.keys())
product_prices = [price[0] for price in d.values()] 
average_price = sum(product_prices) / len(product_prices)

above_avg_data = [(name, price[0]) for name, price in d.items() if price[0] > average_price] 
below_avg_data = [(name, price[0]) for name, price in d.items() if price[0] <= average_price] 
price_differences = {name: price[0] - average_price for name, price in d.items()}  

colors = ['green' if value >= 0 else 'red' for value in price_differences.values()]

  

fig = go.Figure(go.Bar(
    x=list(price_differences.keys()),
    y=list(price_differences.values()),
    marker_color=colors,
    customdata=[price[1] for price in d.values()]
))
fig.add_hline(y=0, line_color='black', line_width=2, line_dash='dash', annotation_text='Average Price')
fig.update_traces(
    hovertemplate="Product: %{x}<br>Price Difference: %{y}<br>Website: %{customdata}"  
)
fig.update_layout(
    title="Product Prices Comparison",
    xaxis_title="Price Difference from Average",
    yaxis_title="Product Names", 
    autosize=True, 
    margin=dict(l=50, r=50, t=50, b=50) 
)
fig.show()



