function loadUser() {
    document.getElementById('toto').addEventListener('change', chargerJSON, false)
}

function chargerJSON(evt) {
    // On crée un objet fichier à lire
    var reader = new FileReader();
    // Quand le fichier est chargé on l'exploite
    reader.onload = function(evt) {
        var leJSON = JSON.parse(evt.target.result)
        document.getElementById("result").innerHTML = "<p>propriétaire : "+leJSON.owner+"</p>"
    }
    // On lit le fichier du champ input qui a l'id files
    reader.readAsText(evt.target.files[0])
}

/*
var template, data, html
    template = "<ul>{{#repo}}<li>{{nom}}</li>{{/repo}}</ul>"
    data = {
        "repo": [
            {"nom" : "Nom A"},
            {"nom" : "Nom B"},
            {"nom" : "Nom C"}
        ]
    }
    html = Mustache.render(template,data)
    document.getElementById("result").innerHTML = html*/