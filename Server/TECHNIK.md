# IchLebe  (Technik)

__IchLebe__ ist eine Client-Server Applikation

## virtuelle umgebung für python

    cd <das Arbeitsdirectory>
    python3 -m venv env
    source env/bin/activate             (Linux)
    cd env\Scripts; activate; cd ..\..  (Windows)

Nun steht im Terminal in der Kommandozeite am Anfang (env)

## setup environment

??

## app starten

Die App starten. Es wird kein Webserver benötigt. Flask/Python bringt einen Webserver mit.

### In der Entwicklung

Starten wärend der Entwicklung.

Es gibt mehrere Möglichkeiten das Programm 

1. In der Konsole folgendes ausführen:
    flask --app main.py --debug run --port 5000

2. In der Main.py / App.py
    if __name__ == "__main__":
        app.run(host="127.0.0.1", port=5005, debug=True)

Die zweite Möglichkeit hat den Nachteil, dass sie bei einem Programmierfehler abbricht.


### in der Bereitstellung

In der Bereitstellung wird der wcgi? wenserver waitress verwendet

    if __name__ == '__main__':
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)







## Server

Der Server ist eine Api geschrieben in Python und Flask.

    Prog:       Python
    Module:     Flask
    Datenbank:  Sqlite

### imports

    pip install flask
    pip install bootstrap-flask
    pip install flask-wtf
    pip install wtforms             (Eventuell schon installiert)
    pip install flask-sqlalchemy
    pip install flask-login
    pip install bcrypt

### Docu

Die Doku
    https://getbootstrap.com/docs/5.0/components/navbar/

Die CDN
    https://getbootstrap.com/docs/5.0/getting-started/introduction/



### Hardware
Die Hardware ist ein Raspberry PI

### Serversoftware
Apache oder 

### Hosting
Ich hoste bei mir zu Hause. 

### DNS
Dyndns stellt eine Dynamische IP bereit.




## Client
Der Client ist eine Handyapp.

    Prog:       Html, Javascript
    Module:     
    OS:         Android



