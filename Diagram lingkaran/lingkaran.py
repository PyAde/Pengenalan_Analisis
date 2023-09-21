import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import re


url = "https://karir.com/search?context=welcome_main_search&q=programmer&location=&IREFERRER=https%253A%2F%2Fcolab.research.google.com%2F&LREFERRER=https%253A%2F%2Fcolab.research.google.com%2F&ILANDPAGE=https%253A%2F%2Fkarir.com%2F&VISITS=1"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
lowkers = soup.find_all(class_="columns opportunity")
posisi = []
instansi = []
gaji = []
lokasi = []

for info in lowkers:
    s1 = info.select("a")
    s2 = s1[0].select("h4")
    posisi.append(s2[0].get_text())
    lokasi.append(info.find("span", class_="tdd-location").get_text())
    instansi.append(info.find("div", class_="tdd-company-name h8 --semi-bold").get_text())
    
    gaji_element = info.find("span", string=re.compile(r'IDR'))  
    if gaji_element:
        gaji_text = gaji_element.text
    else:
        gaji_text = "Gaji Kompetitif"  
    
    gaji.append(gaji_text)
lowkers_df = pd.DataFrame({
    "Posisi": posisi,
    "Instansi": instansi,
    "Gaji": gaji,
    "Lokasi": lokasi
})
def extract_salary(gaji_text):
    if "Gaji Kompetitif" in gaji_text:
        return None  
    match = re.search(r'\d+\.\d+|\d+', gaji_text)
    if match:
        return float(match.group())
    else:
        return None 
lowkers_df['Gaji_Numerik'] = lowkers_df['Gaji'].apply(extract_salary)
median_gaji = lowkers_df['Gaji_Numerik'].median()
lowkers_df = lowkers_df.sort_values(by='Gaji_Numerik', ascending=False)
gaji_per_posisi = lowkers_df.groupby('Posisi')['Gaji_Numerik'].sum().reset_index()
fig = px.pie(
    gaji_per_posisi,
    names='Posisi',
    values='Gaji_Numerik',
    title='Persentase Gaji Berdasarkan Posisi Pekerjaan',
)

fig.show()

