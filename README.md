# IPPcode24 Parser

Skript začíná kontrolou argumentu --help pomocí knihovny sys. Alternativní způsob zpracování argumentů
by bylo použít knihovnu argparse, nicméně kvůli absenci implementace bonusových rozšíření je potřeba
zpracovat právě jeden argument, --help. Díky tomuto faktu byl zvolen jednodušší způsob pomocí knihovny
sys.
Díky faktu, že špatný počet hlaviček v IFJ kódu (jiný počet než 1) vrací speciální chybovou hlášku, se jako další
musí speciálně zkontrolovat, zda náhodou daný soubor neobsahuje více nebo méně než jednu hlavičku a vrátit
daný chybový kód.
Pro vytváření samotného XML souboru se používá knihovna xlm.etree.ElementTree, která je dle mého
úsudku nejjednodušším způsobem na vytvoření XML stromu, proto se jako další vytvoří kořenový element pro
výsledný XML soubor.
Následně jde kód cyklem řádek po řádku, odstraní komentáře, prázdné řádky a zpracuje samotné instrukce,
přičemž si také uchovává jejich počet s každou iterací.
Instrukce se stejným formátem argumentů jsou seskupeny do stejné case v python verzi switche: match.
Podle daného typu argumentu se následně kontroluje jeho správnost voláním funkcí regex%x%Match(), kde
%x% kontroluje daný typ argumentu: Var, Sym, Label. Každá tato funkce má v sobě regex, který
samotný kontroluje správnost již dříve zmíněného formátu daného argumentu a vrací bool hodnotu podle
výsledku dané kontroly.
Po každé této kontrole se vytváří SubElement kořenového stromu root s příslušným formátem.
Soubor ukončuje cyklus s koncem vstupního souboru IFJ kód. Po tomto cyklu se upraví odsazení výsledného
stromu, zakóduje se do utf-8 a vypíše se do stdout.
