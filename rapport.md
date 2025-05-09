Le travail du projet précédent m'a permis d'avoir sur Kubernetes Elasticsearch et Kibana de disponible, le reste des tâches 
a du être accompli lors de ce sujet spécial : 

# Travail accompli : 
- Recherche des règles en vigueur et à respecter sur le traitement des données médicales 
- Mise en place d'une base de donnée MySQL, respectant ses conditions
- Mise en place d'un chiffrement pour cette base de donnée pour augmenter la sécurité de ces données

- Création d'un script shell permettant le déploiement automatique de la solution

# Mise en place de la base de donnée 

Pour le stockage des données médicale, il est recommandé de les désidentifier, ou alors de les anonymiser. 
Il est donc demandé d'enlever toutes les données confidentielles permettant de retrouver les personnes en lien avec ces données.

Pour ce faire, notre base de données comportera les champs suivants : 

- Identifiant 
- Tranche d'age 
- Information complémentaire et antécédent du patient (ces données seront chiffrés)

Ces données sont fixes, et comporteront une table avec ces informations, qui elle seront modifiés régulièrement à chaque 
prise de capteur : 

- Tension artérielle
- Fréquence cardiaque 
- Saturation en oxygène 
- Volume Expiratoire Maximal par Seconde (VEMS)
- Capacité Vitale forcée (CVF)

J'ai décidé de prendre des informations en lien avec la bronchopneumopathie chronique obstructive (BPCO), même si cela n'est 
pas suffisant pour déterminer une exacerbération de cela, comme indiqué dans le papier de recherche.

----- 

# Connexion de la base de donnée a elastic search 


