function guardar() {
    let n = document.getElementById("nombre").value
    let a = document.getElementById("apellido").value
    let d = parseFloat(document.getElementById("DNI").value)
    let t = parseInt(document.getElementById("telefono").value)
    


    let alumno = {
        nombre: n,
        apellido: a,
        DNI: d,
        telefono: t
        
    }
    let url = "http://localhost:5000/alumnos"
    var options = {
        body: JSON.stringify(alumno),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            alert("Grabado")
            // Devuelve el href (URL) de la página actual
            window.location.href = "./alumnos.html";  
            // Handle response we get from the API
        })
        .catch(err => {
            //this.errored = true
            alert("Error al grabar" )
            console.error(err);
        })
}

