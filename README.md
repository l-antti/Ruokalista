# Ruokalista
Sovelluksella voi helpottaa arjen ruokasuunnittelua.

Sovelluksen ominaisuuksia:
- kokoaa ruokalistan viikoksi 
- tekee kauppalistan valituista ruuista
- käyttäjä voi luoda tunnuksen sekä kirjautua sisään ja ulos
- käyttäjä voi lisätä uusia reseptejä ja selata jo olemassa olevia reseptejä
- käyttäjä pystyy etsimään reseptejä nimellä tai tietyllä raaka-aineella
- ylläpitäjä voi luoda resepteille luokkia (_katsotaan kerkiänkö tätä_)
- ylläpitäjä voi muokata tai poistaa reseptejä  (_katsotaan kerkiänkö tätä_)



Asennusohjeet:
- kloonaa repositio omalle koneellesi.
- siirry ruokalista_sovellus kansioon ja luo sinne .env-tiedosto. Määritään tiedostoon kaksi riviä:
    - DATABASE_URL=postgresql:///<käyttänimi>
    - SECRET_KEY=<salainen_avain>
- aktivoi virtuaaliympäristö komennolla: $ python3 - m venv venv 
- $ source venv/bin/activate
- varmista requirements.txt-tiedostosta, että riippuvuudet ovat ajantasalla komennolla: (venv) $ pip install -r requirements.txt
- luo tietokannan tarvitsemat taulut tiedostosta schema.sql komennolla: (venv) $ psql < schema.sql
- käynnistä sovellus komennolla: (venv) $ flask run



Välipalautus 3:
Sovellus hyvässä mallissa. Raaka-aineiden kirjaaminen erikseen ja koostaminen yhdeksi kauppalistaksi on aiheuttanut hieman päänvaivaa, joten luultavasti ylläpitjän ominaisuudet jäävät tällä kertaa pois.

Tähän mennessä tehtynä:
- tunnuksen luonti ja kirjautuminen
- uusien reseptien lisäys
- reseptien selausnäkymä
- viikon menun arvonta ja muokkaus
  
Välipalautus 2:
Sovelluksen perusrakenne alkaa hahmottumaan. Joitakin syötteen varmennuksia puuttuu vielä sekä ruokalista-arvonta ja kauppalistan koonti. 

