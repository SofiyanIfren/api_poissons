var lat = 46.798211;
var lon = 2.45167;

function initMap() {
    macarte = L.map('map').setView([lat, lon], 6);
    
	L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'//,
		//maxZoom: 18,
        //minZoom: 7
    }).addTo(macarte);

    for (var data = 0; data < data_json.length; data ++){
        coordonnees = data_json[data]["coordonn�es de la station"];
        nom_poisson = data_json[data]["nom commun du poisson"];
        nom_cours_eau = data_json[data]["nom du cours d'eau"];
        nom_station = data_json[data]["nom de la station de p�che"];
        nombre_operations = data_json[data]["nombre d'operations men�es"];

        console.log(nom_poisson);

        if (nom_poisson === "Perche"){ // A changer en fonction du poisson pour lequel on veut obtenir des données
            document.getElementById('poisson').innerHTML = nom_poisson;
            // Il nous faut inverser latitude et longitude pour Leaflet
            var coordonnees_json = $.parseJSON(coordonnees);
            var longitude = coordonnees_json[0];
            var latitude = coordonnees_json[1];
            // On ajoute un marqueur par valeur, aux coordonnées correspondantes
            var marker = L.marker([latitude, longitude])
            marker.bindPopup("- Nom de la station:</br><b>" + nom_station + "</b></br>- Nom du cours d'eau:</br><b>" + nom_cours_eau + "</b></br>- Nombre d'opérations:</br><b>" + nombre_operations).addTo(macarte) + "</b>";
        } 
    }
}

$(document).ready(function() {
    initMap();
});
