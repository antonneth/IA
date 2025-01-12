MODEL APROXIMATIU DE PROJECTE DE DECODIFICACIO DE LA PERCEPCIÓ VISUAL HUMANA
Hem decidit programar-ho en Python perquè es llenguatge de programació més versàtil que hi ha, a més a més hi han moltes llibreries relacionades amb la neurociència, la biblioteca d’arxius anomenada nilearn que utilitzarem per automatitzar molts processos com el preprocessament serà una d’elles. O també img2fmri que utilitza un model de difusió latent per generar imatges.
 Dintre del repositori n’hi han molts arxius, com el paquet de Python: IMG2FMRI per predir respostes de fMRI a nivell de grup a estímuls visuals mitjançant xarxes neuronals profundes https://github.com/dpmlab/img2fmri, però m’enfocaré en només 3 arxius el qual he 
programat i donaré una explicació adequada per cadascuna d’elles.
Codi 1
El primer arxiu s’anomena main.py i és el que inicialitza els 2 fitxers restants i connecta la seva informació. Té el següent codi:
Codi 2
El segon arxiu s’anomena NSDcache.py i és el que inicialitzara la descàrrega de la base de dades de NSD per la transferència d’arxius mitjançant Amazon AWS. Hem implementat “boto3” per una eficient descarrega en Python en tot el programa, podeu consultar la documentació en: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
I per últim el tercer codi que ve executat per main.py després que finalitzi la descàrrega inicialitzada per NSDcache.py és el codi principal on té com a funció extreure tots els arxius que hem instal·lat anteriorment i llegir les dades 4D mesurades en vòxels en un conjunt de dades 2D. Amb aquestes dades 2D entrena un model d’aprenentatge automàtic que associa imatges relacionades amb l’estímul que li correspon amb les dades, faltaria un llarg de procés de preprocessament de les dades però agafem les dades d’entrenament de la carpeta nsddata_timeseries on ja les conte preprocessades
3.3.1 Consideracions tècniques
És important destacar que aquest projecte està pensat com una demostració teòrica i pràctica sobre com es podria implementar un sistema per analitzar dades de ressonància magnètica funcional utilitzant eines avançades com el Natural Scenes Dataset (NSD), AWS i biblioteques de Python especialitzades com nilearn. Tot i això, cal tenir en compte els següents punts:
Requisits tècnics i de recursos:
El Natural Scenes Dataset (NSD) ocupa gairebé 13 TB de dades. Per tant, per executar aquest codi, és imprescindible disposar d'un sistema amb prou capacitat d'emmagatzematge i recursos computacionals adequats. Recomanem utilitzar serveis al núvol com AWS o una màquina d'alt rendiment.
Els serveis com AWS poden implicar costos addicionals. Assegura't de tenir un pressupost adequat si planeges reproduir el projecte complet.
Execució parcial del codi:
Per tal de fer que aquest projecte sigui accessible, es poden executar parts del codi de manera local (per exemple, la preparació del dataset o la implementació d'un model d'aprenentatge automàtic més senzill amb dades simulades).
Hem inclòs comentaris i exemples en el codi perquè sigui fàcilment adaptable a les necessitats del lector.
Limitacions actuals:
Algunes seccions del codi (com l’entrenament del model o la integració amb Stable Diffusion) poden requerir treball addicional per ajustar-se a dades específiques o entorns computacionals.
El projecte no pretén ser completament funcional sense modificacions per part del lector. L’objectiu és servir de guia o punt de partida per a investigacions o treballs més avançats.
