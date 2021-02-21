import requests
import tkinter as tk
from tkinter import ttk, StringVar
import json



# API-nyckel på Trafiklab.se
# En dictionary - som en uppslagsbok
stations_dict = {'Karlstad':'Ks', 'Arvika':'Ar', "Bäckebron":"Bäb", "Charlottenberg":"Cg", "Edane": "En", "Fagerås":"Fgå", "Frykåsen":"Frå", "Filipstad":"Fid", "Grums": "Gms", "Högboda":"Hbd", "Kil": "Kil", "Kolsnäs": "Kns", "Välsviken":"Kvä", "Kristinehamn": "Khn", "Lysvik":"Lyv", "Nässundet": "Nd", "Nykroppa": "Nka", "Oleby": "Ol", "Rottneros":"Rts" }

API_KEY = 'aa916ca49ce741d5bc78df1302631bfd'
#API_KEY = 'FYLL I DIN PERSONLIGA API-NYCKEL'


def getDepartures():
    with open('data.json', 'w') as f:
      #Hittar index från stations namn i Stations_Dict och skriver in den i data.json
      json.dump(list(stations_dict.values()).index(stations_dict[stationer.get()]), f)

    """
    Hämtar data från Trafikverket med ett POST-anrop
    """
    request = f"""<REQUEST>
<LOGIN authenticationkey="{API_KEY}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationer.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd(07:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(12:00:00)" />
</AND>
</OR>
</AND>
</FILTER>
<INCLUDE>LocationSignature</INCLUDE>
<INCLUDE>AdvertisedTrainIdent</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>TrackAtLocation</INCLUDE>
<INCLUDE>ToLocation</INCLUDE>
<INCLUDE>AdvertisedLocationName</INCLUDE>

</QUERY>
</REQUEST>"""

    # Här sker själva anropet
    url = 'https://api.trafikinfo.trafikverket.se/v1.3/data.json'
    response = requests.post(url, data = request, headers = {'Content-Type': 'text/xml'}, )

    # Formatera svaret från servern som ett json-objekt
    response_json = json.loads(response.text)
    departures = response_json["RESPONSE"]['RESULT'][0]['TrainAnnouncement']
    
    # Töm svarsrutan
    stationer_text.delete(1.0,"end")

    # Fyll i svarsrutan, med ett streck mellan varje post
    for dep in departures:
        stationer_text.insert(1., '\n- - - - - - - -\n\n')
        tillstationenKey = dep['ToLocation'][0]['LocationName']
        stationer_text.insert(1., tillstationenKey)
        stationer_text.insert(1., '\n- - - - - - - -\n')

        Spår ="Spår: " + dep['TrackAtLocation']
        stationer_text.insert(1., Spår)
        stationer_text.insert(1., '\n- - - - - - - -\n')

        tågnummer ="tågnummer: " + dep['AdvertisedTrainIdent']
        stationer_text.insert(1., tågnummer)
        stationer_text.insert(1., '\n- - - - - - - -\n')

        datum = "datum: " + dep['AdvertisedTimeAtLocation']
        stationer_text.insert(1., datum)
        stationer_text.insert(1., '\n----------------------------------------------------\n\n\n')
          
#----------------------

# Det grafiska gränssnittet
root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=1000)
canvas.configure(background='#FD6A02')
canvas.pack()


# Knapp
button=tk.Button(root, text='sök', fg='#06EB02', command= getDepartures)
button.configure(background='#453F34')
button.place(relwidth=0.2, height=50, relx=0.25, rely=0.80)


# Combobox med stationer. Läser in alla "uppslagsord" från stations_dict
#läser datan från data.json och använder indexet som current value efter att vi gör det till int
f = open ('data.json', "r") 
data = int(json.loads(f.read()))

stationer = ttk.Combobox(canvas, state='readonly')
stationer['values'] = list(stations_dict.keys())
stationer.current(data)
stationer.place(relwidth=0.2, height=50, relx=0.55, rely=0.80)

# Textruta
stationer_text = tk.Text(canvas)
stationer_text.place(relx=0.15, rely=0.09, relwidth=0.7, relheight=0.7)
stationer_text.configure(background='#453F34', fg='#06EB02')

root.mainloop()
