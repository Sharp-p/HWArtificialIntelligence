(define (domain LiquidSort)
    (:requirements :adl :typing)
    (:types
        beaker color level - object
    )

    (:predicates
        ; --- STATICI (Geometria) ---
        ; Definisce la sequenza dei livelli: (succ l0 l1), (succ l1 l2)...
        ; l0 è un livello fittizio che rappresenta il fondo/vuoto.
        (succ ?l1 ?l2 - level)

        ; Identifica il livello "zero" (il fondo sotto il primo slot)
        (is-bottom ?l - level)

        ; --- DINAMICI (Stato del gioco) ---
        ; Inserisce il colore C nel beaker B al livello L
        (has-color ?b - beaker ?l - level ?c - color)

        ; Definisce il livello più alto occupato nel beaker.
        ; Se il beaker è vuoto, il top è l0.
        (top ?b - beaker ?l - level)
    )

    (:action pour-chunk-1
        :parameters (
            ?from - beaker     ; Da dove prendo
            ?to - beaker       ; Dove verso
            ?c - color         ; Il colore che sposto

            ; Variabili per i livelli ORIGINE
            ?l-src-top - level ; Il livello attuale pieno in FROM (es. l3)
            ?l-src-below - level ; Il livello sotto (es. l2)

            ; Variabili per i livelli DESTINAZIONE
            ?l-dest-top - level ; Il livello attuale pieno in TO (es. l0 se vuota)
            ?l-dest-new - level ; Il livello che riempiremo (es. l1)
        )
        :precondition (and
            ; 1. Non posso versare nello stesso beaker
            (not (= ?from ?to))

            ; 2. Gestione PUNTATORI (Top e Succ)
            (top ?from ?l-src-top)        ; Il from è pieno fino a src-top
            (succ ?l-src-below ?l-src-top); src-below sta subito sotto src-top
            (top ?to ?l-dest-top)         ; Il to è pieno fino a dest-top
            (succ ?l-dest-top ?l-dest-new); dest-new è il prossimo spazio libero

            ; 3. CONTROLLO COLORE SORGENTE (Deve esserci il colore C)
            (has-color ?from ?l-src-top ?c)

            ; 4. VINCOLO CHUNK
            ; Questa azione è valida SOLO SE sotto non c'è lo stesso colore.
            ; Altrimenti dovrei usare pour-chunk-2.
            (or
                (is-bottom ?l-src-below)  ; O sono arrivato al fondo
                (not (has-color ?from ?l-src-below ?c)) ; O il colore sotto è diverso
            )

            ; 5. VINCOLO DESTINAZIONE
            ; La destinazione deve essere vuota (top è bottom)
            ; OPPURE avere lo stesso colore in cima.
            (or
                (is-bottom ?l-dest-top)
                (has-color ?to ?l-dest-top ?c)
            )
        )
        :effect (and
            ; Aggiorna puntatori top
            (not (top ?from ?l-src-top))
            (top ?from ?l-src-below)

            (not (top ?to ?l-dest-top))
            (top ?to ?l-dest-new)

            ; Sposta il liquido
            (not (has-color ?from ?l-src-top ?c))
            (has-color ?to ?l-dest-new ?c)
        )
    )

    (:action pour-chunk-2
        :parameters (
            ?from - beaker ?to - beaker ?c - color

            ; Livelli Origine (Dall'alto verso il basso)
            ?l-src-1 - level  ; Top attuale
            ?l-src-2 - level  ; Sotto top
            ?l-src-3 - level  ; Sotto ancora (il punto di stacco)

            ; Livelli Destinazione (Dal basso verso l'alto)
            ?l-dest-0 - level ; Top attuale
            ?l-dest-1 - level ; Primo spazio libero
            ?l-dest-2 - level ; Secondo spazio libero
        )
        :precondition (and
            (not (= ?from ?to))

            ; --- Struttura Origine ---
            (top ?from ?l-src-1)
            (succ ?l-src-2 ?l-src-1)
            (succ ?l-src-3 ?l-src-2)

            ; Devono esserci 2 unità dello stesso colore
            (has-color ?from ?l-src-1 ?c)
            (has-color ?from ?l-src-2 ?c)

            ; VINCOLO CHUNK: Sotto le 2 unità deve finire il blocco
            (or
                (is-bottom ?l-src-3)
                (not (has-color ?from ?l-src-3 ?c))
            )

            ; --- Struttura Destinazione ---
            (top ?to ?l-dest-0)
            (succ ?l-dest-0 ?l-dest-1)
            (succ ?l-dest-1 ?l-dest-2) ; Deve esserci spazio per 2!

            ; Compatibilità colore destinazione
            (or
                (is-bottom ?l-dest-0)
                (has-color ?to ?l-dest-0 ?c)
            )
        )
        :effect (and
            ; Aggiorna puntatori top
            (not (top ?from ?l-src-1))
            (top ?from ?l-src-3)          ; Il nuovo top scende di 2

            (not (top ?to ?l-dest-0))
            (top ?to ?l-dest-2)           ; Il nuovo top sale di 2

            ; Sposta i liquidi
            (not (has-color ?from ?l-src-1 ?c))
            (not (has-color ?from ?l-src-2 ?c))
            (has-color ?to ?l-dest-1 ?c)
            (has-color ?to ?l-dest-2 ?c)
        )
    )

    (:action pour-chunk-3
        :parameters (
            ?from - beaker ?to - beaker ?c - color

            ; from beaker levels from top to bottom
            ?l-src-1 - level ; this is the top of color c
            ?l-src-2 - level
            ?l-src-3 - level
            ?l-src-4 - level ; this will be a different color and new top

            ; to beaker from top to new top
            ?l-dest-0 - level ; this is the top and is color c
            ?l-dest-1 - level
            ?l-dest-2 - level
            ?l-dest-3 - level ; this will be the new top
        )
        :precondition (and
            (not (= ?from ?to))
            ; FROM BEAKER STRUCTURE
            ; correct sequence of levels
            (top ?from ?l-src-1)
            (succ ?l-src-2 ?l-src-1)
            (succ ?l-src-3 ?l-src-2)
            (succ ?l-src-4 ?l-src-3)

            ; correct quantity of liquid of color ?c
            (has-color ?from ?l-src-1 ?c)
            (has-color ?from ?l-src-2 ?c)
            (has-color ?from ?l-src-3 ?c)

            ; lower level of from is bottom or different color
            (or
                (is-bottom ?l-src-4)
                (not (has-color ?from ?l-src-4 ?c))
            )

            ; TO BEAKER STRUCTURE
            ; correct sequence of levels
            (top ?to ?l-dest-0) ; guarantees that there is space on top
            (succ ?l-dest-0 ?l-dest-1)
            (succ ?l-dest-1 ?l-dest-2)
            (succ ?l-dest-2 ?l-dest-3) ; must exist 3 levels after the current top

            ; compability color - destination
            (or
                (is-bottom ?l-dest-0)
                (has-color ?to ?l-dest-0 ?c)
            )
        )
        :effect (and
            ; update se top sequence of from beaker
            (not (top ?from ?l-src-1))
            (top ?from ?l-src-4)

            ; setting new top of to beaker
            (not (top ?to ?l-dest-0))
            (top ?to ?l-dest-3)

            ; removing 3 colors from beaker
            (not (has-color ?from ?l-src-1 ?c))
            (not (has-color ?from ?l-src-2 ?c))
            (not (has-color ?from ?l-src-3 ?c))
            ; adding 3 colors to beaker
            (has-color ?to ?l-dest-1 ?c)
            (has-color ?to ?l-dest-2 ?c)
            (has-color ?to ?l-dest-3 ?c)
        )
    )
    (:action pour-chunk-4
        :parameters (
            ?from - beaker ?to - beaker ?c - color

            ; from beaker levels from top to bottom
            ?l-src-1 - level ; this is the top of color c
            ?l-src-2 - level
            ?l-src-3 - level
            ?l-src-4 - level 
            ?l-src-5 - level ; this is bottom of the beaker and will be the new top

            ; to beaker from top to new top
            ?l-dest-0 - level ; this is the top (l0) and the bottom
            ?l-dest-1 - level
            ?l-dest-2 - level
            ?l-dest-3 - level
            ?l-dest-4 - level ; this will be the new top
        )
        :precondition (and
            (not (= ?from ?to))
            ; FROM BEAKER STRUCTURE
            ; correct sequence of levels
            (top ?from ?l-src-1)
            (succ ?l-src-2 ?l-src-1)
            (succ ?l-src-3 ?l-src-2)
            (succ ?l-src-4 ?l-src-3)
            (succ ?l-src-5 ?l-src-4)

            ; correct quantity of liquid of color ?c
            (has-color ?from ?l-src-1 ?c)
            (has-color ?from ?l-src-2 ?c)
            (has-color ?from ?l-src-3 ?c)
            (has-color ?from ?l-src-4 ?c)

            ; lower level of from has to be the bottom (the bottom has no color)
            (is-bottom ?l-src-5)

            ; TO BEAKER STRUCTURE
            ; correct sequence of levels
            (top ?to ?l-dest-0) ; guarantees that there is space on top
            (succ ?l-dest-0 ?l-dest-1)
            (succ ?l-dest-1 ?l-dest-2)
            (succ ?l-dest-2 ?l-dest-3) 
            (succ ?l-dest-3 ?l-dest-4) ; must exist 4 levels after the current top

            ; compability color - destination
            (is-bottom ?l-dest-0)
        )
        :effect (and
            ; update se top sequence of from beaker
            (not (top ?from ?l-src-1))
            (top ?from ?l-src-5)

            ; setting new top of to beaker
            (not (top ?to ?l-dest-0))
            (top ?to ?l-dest-4)

            ; removing 4 colors from beaker
            (not (has-color ?from ?l-src-1 ?c))
            (not (has-color ?from ?l-src-2 ?c))
            (not (has-color ?from ?l-src-3 ?c))
            (not (has-color ?from ?l-src-4 ?c))
            ; adding 4 colors to beaker
            (has-color ?to ?l-dest-1 ?c)
            (has-color ?to ?l-dest-2 ?c)
            (has-color ?to ?l-dest-3 ?c)
            (has-color ?to ?l-dest-4 ?c)
        )
    )
)
