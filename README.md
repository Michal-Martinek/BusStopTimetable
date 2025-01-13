This project is originally _stolen_ from [my friend](https://www.instagram.com/matygam09), who made it as his semester project.

## Original README
> Moje semestrální práce se zabývá vytvořením webu, který má za úkol zobrazovat odjezdy MHD ve stanicích PID.  
>  
> Používá pro to volně dostupná data ze serveru Golemio. https://api.golemio.cz/pid/docs/openapi/  
>  
> Uživatel si nejprve zvolí zastávku, která se následně přesune do samotné aplikace, která stahuje a zobrazuje data odjezdů.  
>  
> Na stránce s odjezdy dole se také nachází mapa spojů v Praze (tam by se do budoucna dalo implementovat např. zoomování do zastávky zvolené uživatelem, filtrace spojů, ...).  
>  
> Zatím je tam mapa jen jako doplňující možnost zobrazení spojů.  
>  
> Kód má dohromady okolo 260 řádků.  
>  
> Nachází se zde 2 html šablony, python aplikace a soubor s upravenými daty zastávek.  
>  
> !!!! Pro spuštění kódu je třeba otevřít soubor app.py a následovat pokyny v něm napsané !!!!  
>  
> Poté se ve složce nachází zdrojový soubor zastávek a python aplikace, která slouží k upravení dat zastávek do konečné formy.  
>  
> -> tu jsem vytvořil, abych snížil potřebná data, ve kterých uživatel hledá, taky abych měl přímo v jednom listu v souboru všechny zastávky.  
>  
> Tedy by mělo jít stáhnout ze serverů PIDu soubor se zastávkami (pokud chceme aktualizovat stávající) a použít na něj danou funkci.  


## Further possibilities
* udelat html hezci a modernejsi
* ta mapa pid, ktera je tam ted jenom vlozena, se da docela jednodusse upravovat a filtrovat a pridavat souradnice, tim ze to funguje na stejem systemu. Teoreticky by stacilo upravit tu funkci, ktera si taha data z puvodnich zastavek a dela ten ciste zastavkovy soubor-tak tam pridat, aby tam dala i souradnice.
* To si muzes vyzkouset, kdyz na te strance treba zazoomojes, posunes se a filtrujes, jak se meni ta adresa
* Příklad: https://mapa.pid.cz/?filter=&zoom=11.0&lon=14.4500&lat=50.0800