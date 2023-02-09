<center> <h1>Sebastian Rychert</h1> </center>
<center> <h2>Memory Game</h2> </center>

### **Komunikacja**

Komunikacja odbywa się bezpośrednio między graczami poprzez gniazda datagramowe (UDP), co może umożliwić granie na różnych komputerach przez sieć. Czytanie nadchodzących komunikatów odbywa się w wydzielonych wątkach, które następnie umieszczają wiadomości w kolejce do wykorzystania przez program i interfejs graficzny.

```python
def read(gui_queue):
    move, adres = UDPSocket.recvfrom(bufSize)
    # put a move into queue for GUI
    gui_queue.put(move.decode())

# ...
gui_queue = queue.Queue()

threading.Thread(target=read, args=(gui_queue,), daemon=True).start()
```

### **Użytkowanie programu**

1. Każdy z graczy uruchamia program oraz podaje informacje sieciowe, wypełniając odpowiednie pola w oknie.

    - W przypadku podania niepoprawnych informacji pojawia się komunikat tekstowy sygnalizujący błąd

2. Po podaniu kompletu informacji pojawia się okno oczekiwania na drugiego gracza.
3. W momencie gotowości obu graczy gra się rozpoczyna. Wyświetla się okno z planszą 6×4, która jest założona z 24 mniejszych czarnych kwadratów.
4. Rozgrywkę rozpoczyna gracz, który jako pierwszy zgłosił gotowość.
5. Gracz który "posiada" turę odkrywa 2 kwadraty za pomocą myszki, ruchy te są widoczne dla drugiego gracza.

    - Jeżeli kolory odkrytych kwadratów są różne, gracz traci turę, a kwadraty zostają ukryte
    - W przypadku gdy kolory odkrytych kart są takie same gracz otrzymuje punkt oraz kolejną turę
    - Informacje o turze oraz punktacji graczy umieszczone są nad planszą

6. Jeżeli któryś z graczy rozłączy się w trakcie gry, w oknie przeciwnika pojawia się odpowiedni komunikat oraz gra się kończy.
7. Gra kończy się w momencie odkrycia wszystkich kwadratów.
8. Gracze otrzymują informacje o wygranej/przegranej/remisie.

![Ustawienie gry](/lab11/docs/game_setup_1.png) <br/>
![Ustawienie gry błąd](/lab11/docs/game_setup_2.png) <br/>
![Ekran oczekiwania](/lab11/docs/wait.png) <br/>
![Przykład rozgrywki](/lab11/docs/game_example.gif) <br/>
