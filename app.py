import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = requests.utils.default_headers()
headers.update({
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
})

st.title('Competitive LOL Stats Explorer')

st.markdown("""
This app performs simple webscraping of LOL competitive stats data!
* **Python libraries:** [pandas](https://pandas.pydata.org/), [streamlit](https://streamlit.io/), [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* **Data source:** [gol.gg](https://gol.gg)
""")

champs = {
    'LeBlanc': 'Leblanc',
    'Wukong': 'MonkeyKing',
    'Renata Glasc': 'Renata',
    'Dr. Mundo': 'DrMundo',
    'KhaZix': 'Khazix',
    'VelKoz': 'Velkoz'
}

def image(name):
    nombre = name
    if nombre in champs.keys():
        final = champs[name]
    else:
        final = nombre.replace(' ', '')
    return(f"<img src='http://ddragon.leagueoflegends.com/cdn/12.9.1/img/champion/{final}.png"
        f"""' style='display:block;margin-left:auto;margin-right:auto;width:30px;border:0;'><div style='text-align:center'>{name}"""
         "</div>")

def flag(name):
    return(f"<img src='https://countryflagsapi.com/png/{name}"
        f"""' style='display:block;margin-left:auto;margin-right:auto;width:30px;border:0;'><div style='text-align:center'>{name}"""
         "</div>")

limit = st.slider(label= 'Number of data to show', max_value=150, min_value=10)

tournaments = []

url = "https://gol.gg/champion/list/season-S12/split-ALL/tournament-ALL/"
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'html.parser')
form = soup.find('select', id='cbtournament')
values = form.findChildren('option')

for val in values[1:]:
    tournaments.append(val.text)

st.sidebar.header('Tournament Input')
competition = st.sidebar.selectbox('Tournament : ', tournaments)
option = st.sidebar.selectbox('Data from : ', ['Teams', 'Players', 'Champion'])

@st.cache
def load_data(option, tournament, number):
    url = f"https://gol.gg/{option.lower()}/list/season-S12/split-ALL/tournament-{tournament}/"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    table = pd.read_html(soup.prettify())[-1]
    df = pd.DataFrame(table)
    if 'Champion' in df.columns:
        df['Champion'] = df['Champion'].apply(lambda x: image(x))
    elif 'Country' in df.columns:
        df['Country'] = df['Country'].apply(lambda x: flag(x))
    return df[:number]

data = load_data(option, competition, limit)

st.header(f"""Display *{option}* Stats of *{competition}* """)
st.write(data.to_html(escape=False, index=False), unsafe_allow_html=True)
