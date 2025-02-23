# projekt_sachy spracováno v pythonu pomocí pygame

návod na instalaci pygame : 

O hře:
Normální hra šachu. pro dva hráče jsou implementovány pravidla(en pesant, rošáda, povýšení pěšce), také lze hrát ve dvou režimech rapid a blitz.

Jak hrát hru:
Hra se ovládá jednoduše pomocí klávesnice (TAB, ENTER) a pohyb s figurakmi pomocí myši

TO DO LIST:
Implementace Multiporocesingu který bude v průběhu hry počítat šanci na šach mat v dalších 5 tazích
Rozdělení projektu do více souborů pro větší přehlednost kodu
Optimalizovat a implementovat pomocí multiprocesingu funkci chance 
opravit fukci del_king_move která by měla  omezovat králi když je v šachu udělat tah ve který ho dostane do dalšího šachu

FIXED:
přidání souboru draw.py do kterého jsou vloženy funkce vykreslující.
