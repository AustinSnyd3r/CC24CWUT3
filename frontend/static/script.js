"use strict"


let clear_table = () =>{
    let body = document.getElementById("appsBody");

     while (body.firstChild) {
         body.removeChild(body.firstChild);
     }
}

//
let handle_applications = (apps) =>{
    clear_table()
    const tbody = document.getElementById('appsBody');
    apps.forEach(app => {
        let row = document.createElement('tr');
        row.innerHTML = `
                         <td>${app[0]}</td>
                         <td>${app[2]}</td>
                         <td>${app[3]}</td>
                         <td>${app[4]}</td>
                         <td>${app[5]}</td>
                        <td><button value = "Delete" id=${app[0]}></td>
                        <td><button value = "Edit" id=${app[0]}></td>`;
        tbody.appendChild(row);
    })

    document.querySelectorAll("")
}

//Fetches the applications from python file.
let fetch_applications = () => {
    fetch('/applications')
        .then(response => response.json())
        .then(handle_applications)
        .catch(error => console.error('Error fetching applications:', error));
};

document.addEventListener('DOMContentLoaded', function() {
    //load the applications on page load
    fetch_applications();

    //make a button to load applications if they edited one or something
    let load = document.getElementById("load");
    load.addEventListener("click", fetch_applications);

});
