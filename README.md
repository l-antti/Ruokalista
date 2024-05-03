# Ruokalista
Sovelluksella voi helpottaa arjen ruokasuunnittelua.

Sovelluksen ominaisuuksia:
- kokoaa ruokalistan viikoksi 
- tekee kauppalistan valituista ruuista
- reseptejä pystyy selaamaan sekä etsimään nimellä tai haluamallaan raaka-aineella
- käyttäjä voi luoda tunnuksen sekä kirjautua sisään ja ulos
- käyttäjä voi lisätä uusia reseptejä
- ylläpitäjä voi muokata reseptejä



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



Käyttäjästä voi tehdä ylläpitäjän seuraavasti:
- avaa PSQL-tulkki $ psql 
- syötä komento UPDATE users SET admin = true WHERE username = 'käyttäjänimi'; , jossa 'käyttäjänimi' on sen käyttäjän nimi, jolle annetaan admin-oikeudet
 

