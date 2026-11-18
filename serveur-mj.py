#!/usr/bin/env python3
"""Serveur local du MJ virtuel (v1.0)

- sert l'app de jeu (jouer.html) et le banc d'essai (index.html) depuis ce dossier ;
- relaie les demandes de voix vers VoiceStudio (http://127.0.0.1:3900), sur le même Mac.

Comme la page et les voix viennent de la même adresse, ni le navigateur ni VoiceStudio
ne bloquent les appels, et un téléphone sur le même wifi peut jouer avec les voix du Mac.
Aucune installation : uniquement la bibliothèque standard de Python 3.
"""
import http.server
import os
import socket
import sys
import urllib.error
import urllib.request

PORT = int(os.environ.get("MJ_PORT", "8000"))
VOICESTUDIO = os.environ.get("MJ_VOICESTUDIO", "http://127.0.0.1:3900").rstrip("/")
DOSSIER = os.path.dirname(os.path.abspath(__file__))
RELAIS = ("/v1/", "/health")
ENTETES_IGNOREES = {"host", "origin", "referer", "connection", "content-length", "accept-encoding"}


def adresse_locale():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.0.1", 1))  # aucun paquet n'est envoyé
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "adresse-du-mac"


class Gestion(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOSSIER, **kwargs)

    def log_message(self, fmt, *args):
        sys.stdout.write("  " + (fmt % args) + "\n")

    def end_headers(self):
        # toujours la dernière version des pages
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _relayer(self):
        longueur = int(self.headers.get("Content-Length") or 0)
        corps = self.rfile.read(longueur) if longueur else None
        entetes = {k: v for k, v in self.headers.items() if k.lower() not in ENTETES_IGNOREES}
        req = urllib.request.Request(VOICESTUDIO + self.path, data=corps, headers=entetes, method=self.command)
        try:
            with urllib.request.urlopen(req, timeout=180) as rep:
                statut, contenu, ctype = rep.status, rep.read(), rep.headers.get("Content-Type", "application/octet-stream")
        except urllib.error.HTTPError as e:
            statut, contenu, ctype = e.code, e.read(), e.headers.get("Content-Type", "application/json")
        except (urllib.error.URLError, OSError) as e:
            statut, ctype = 502, "application/json"
            contenu = ('{"detail": "VoiceStudio ne répond pas sur %s : ouvre l\'app VoiceStudio sur ce Mac. (%s)"}'
                       % (VOICESTUDIO, str(e).replace('"', "'"))).encode("utf-8")
        self.send_response(statut)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(contenu)))
        self.end_headers()
        self.wfile.write(contenu)

    def do_GET(self):
        if self.path.startswith(RELAIS):
            return self._relayer()
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/jouer.html")
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith(RELAIS):
            return self._relayer()
        self.send_error(404)


def main():
    ip = adresse_locale()
    serveur = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Gestion)
    print()
    print("  MJ virtuel : serveur local lancé")
    print("  ─────────────────────────────────")
    print(f"  Sur ce Mac       : http://localhost:{PORT}/jouer.html")
    print(f"  Sur le téléphone : http://{ip}:{PORT}/jouer.html   (même wifi)")
    print(f"  Voix VoiceStudio : {VOICESTUDIO}")
    print()
    print("  Laisse cette fenêtre ouverte pendant la partie. Pour arrêter : ctrl + C.")
    print()
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\n  Serveur arrêté.")


if __name__ == "__main__":
    main()
