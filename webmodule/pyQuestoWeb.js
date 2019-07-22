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
        try {
            var leJSON = JSON.parse(evt.target.result)
        }
        catch(erreur)  {
            document.getElementById("erreur").innerHTML = "JSON invalide !<br />"+ erreur
        }
        var template, data, html
        template = document.getElementById("tpl_owner").innerHTML
        datas = {
            "nom" : leJSON.owner[0].nom,
            "prenom" : leJSON.owner[0].prenom,
            "classe" : leJSON.owner[0].classe
        }
        html = Mustache.render(template,datas)
        document.getElementById("affichage").innerHTML = html

    }
    // On lit le fichier du champ input qui a l'id "files"
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