# [sternwarte-kreuznach.de](https://sternwarte-kreuznach.de/)

Die Website wird mithilfe des **hugo** static site generator (SSG) gebaut und mithilfe von Github Actions automatisch bereitgestellt.

## Entwicklungsanweisungen

Um den **Live-Entwicklungsserver** zu starten, verwende

```
hugo server
```

oder wenn die Seite nicht richtig neu lädt, mit der zusätzlichen Flag `--disableFastRender`.

Um auch **Entwürfe** (drafts) mitauszugeben:

```
hugo server -D
```

Um den Live-Server von **anderen Geräten im Netwerk** erreichbar zu machen, verwende:

```
hugo server -D --bind 0.0.0.0
```
