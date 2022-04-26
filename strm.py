import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

st.title('Web Scraping')

base_url = st.text_input('enter base url')
option = st.selectbox(
     'Which product are you looking for?',
     ('DMC Natura XL', 'Drops Safran', 'Drops Baby Marino Mix', 'Style Craft Special Double Knit'))
st.write('You selected:', option)

end_url = {'DMC Natura XL':'wolle/dmc/dmc-natura-xl?sqr=dmc%20nat',
           'Drops Safran':'artikel/35246/drops-safran-60-moss-green.html?sqr=drops%20sa',
           'Drops Baby Marino Mix':'artikel/35226/drops-baby-merino-mix-48-blush.html?sqr=drops%20bab',
           'Style Craft Special Double Knit':'wolle/stylecraft/stylecraft-special-dk?sqr=stylecraft%20special%20'}
full_url = base_url+end_url[option]
name = []
price = []
composition = []
needle_size = []
if st.button('Get Results'):
     response = requests.get(full_url)
     content = response.text
     soup = BeautifulSoup(content, features="html.parser")


     def parser():
          title = soup.find(class_="wrapper100 wrapper100-page").h1.text.strip()
          name.append(title)
          cost = soup.find(class_="product-price-amount").text.strip()
          price.append(cost)
          for x in soup.select('div#pdetailTableSpecs tr'):
               if x.select('td')[0].text == 'Zusammenstellung':
                    composition.append(x.select('td')[1].text)
               if x.select('td')[0].text == 'Nadelstärke':
                    needle_size.append(x.select('td')[1].text)
     parser()
     product_details = pd.DataFrame({"Name": name, "Price": price, "Composition": composition, "Needle Size": needle_size})
     st.write(product_details)