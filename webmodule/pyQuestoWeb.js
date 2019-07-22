// On surveille le chargement d'un fichier
function checkFile() {
    document.getElementById('toto').addEventListener('change', chargerJSON, false)
}

// On vérifie qu'il s'agit bien d'un JSON compatible
function chargerJSON(evt) {
    // On crée un objet fichier à lire
    var reader = new FileReader();
    // Quand le fichier est chargé on l'exploite
    reader.onload = function(evt) {
        var leJSON = JSON.parse(evt.target.result)
        document.getElementById("result").innerHTML = "<p>propriétaire : "+leJSON.owner+"</p>"
    }
    // On lit le fichier du champ input qui a l'id "files"
    reader.readAsText(evt.target.files[0])
}

