## Panoramica

Questo progetto è stato sviluppato per il rilevamento automatico di fori e macchie in video utilizzando tecniche di visione artificiale. Il programma, tramite l'uso della libreria OpenCV, elabora ogni fotogramma di un video in ingresso e applica filtri di colore per individuare anomalie visive, come fori o macchie, su superfici o materiali. Quando vengono rilevate aree sospette, il programma disegna rettangoli e aggiunge etichette che indicano la presenza di "fori" o "macchie". I risultati possono essere visualizzati in tempo reale o salvati in un video di output per un'analisi successiva.

## Scopo del Programma

Il principale obiettivo di questo programma è automatizzare il processo di rilevamento di fori e macchie su superfici in movimento, come quelle di tessuti o materiali di vario tipo. In particolare, il programma è utile per applicazioni industriali, come l'ispezione di qualità di tessuti, dove è fondamentale identificare difetti o contaminazioni durante il processo produttivo. Il programma è in grado di gestire video in formato .mp4 o .avi e fornisce un output con tutte le aree difettose evidenziate per un'ulteriore analisi.

## Funzionamento del Codice

Il codice si compone di una funzione principale, `detect_holes_and_stains`, che si occupa di caricare il video, analizzare ogni fotogramma e identificare le aree problematiche. Il programma inizia verificando che il file video esista, altrimenti stampa un messaggio di errore e termina. Successivamente, apre il video tramite la funzione `cv2.VideoCapture` di OpenCV e legge le informazioni come la larghezza, l'altezza e i fotogrammi al secondo (FPS). Se viene fornito un percorso di output, il programma inizializza un oggetto `cv2.VideoWriter` per salvare il video elaborato.

Una volta acquisito ogni fotogramma del video, il programma converte il fotogramma da RGB a spazio di colore HSV, che permette di rilevare facilmente i colori specifici di fori e macchie. Le aree di colore bianco e arancione vengono utilizzate per il rilevamento dei fori, mentre macchie di colore nero, blu, verde e rosso vengono cercate per identificare macchie o difetti.

Per ciascuna di queste aree, vengono applicati filtri e operazioni morfologiche come la chiusura e l'apertura per affinare la maschera e migliorare la rilevazione. Successivamente, vengono trovati i contorni delle regioni sospette e, se l'area di un contorno rientra in una gamma predefinita, viene etichettata come "Foro" o "Macchia" e disegnato un rettangolo attorno alla zona difettosa.

## Elaborazione dei Fotogrammi

Ogni fotogramma del video viene elaborato singolarmente. Dopo aver letto un fotogramma, il programma converte l'immagine in spazio HSV (Tonalità, Saturazione, Valore), che consente di segmentare facilmente le aree colorate. Le maschere vengono create utilizzando intervalli di colore per ciascun tipo di difetto, come per i fori (bianco e arancione) e le macchie (nero, blu, verde, rosso). Le operazioni morfologiche vengono poi applicate per rimuovere rumori e migliorare la qualità del rilevamento.

### Rilevamento dei Fori

Il programma utilizza i contorni per rilevare i fori. Una volta creata una maschera combinata che include i colori indicativi di un foro, il programma trova i contorni di queste aree. Se l'area di un contorno è compresa in un intervallo predefinito, il programma disegna un rettangolo attorno al foro e lo etichetta come tale. Ogni foro viene identificato con il testo "Hole" sul video.

### Rilevamento delle Macchie

Simile al rilevamento dei fori, per le macchie vengono create maschere separate per ciascun colore rilevante. Dopo aver rilevato le macchie, il programma usa anche in questo caso i contorni per identificare le aree difettose. Le macchie vengono etichettate come "Stain" e cerchiate con un rettangolo nel fotogramma.

## Gestione dell'Output

Il programma è progettato per visualizzare il video in tempo reale mentre elabora i fotogrammi. Ogni fotogramma elaborato viene mostrato tramite la funzione `cv2.imshow`, che consente di osservare i risultati del rilevamento. Se un percorso di output è specificato, il programma salva il video elaborato in un file. Il salvataggio avviene utilizzando un oggetto `cv2.VideoWriter` che consente di scrivere i fotogrammi elaborati nel formato desiderato (ad esempio, .avi o .mp4).

## Considerazioni Finali

Il programma è uno strumento potente per l'ispezione automatica di difetti nei video, con applicazioni pratiche in vari settori industriali, come la produzione tessile e altre aree in cui la qualità dei materiali è fondamentale. La capacità di rilevare fori e macchie con precisione grazie all'analisi dei colori rende questo strumento utile per migliorare l'efficienza nei processi di ispezione visiva.

