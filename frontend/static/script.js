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
                        <td><button value = "Delete" id=${app[0]} class="delete"></td>
                        <td><button value = "Edit" id=${app[0]+10} class="edit"></td>`;
        tbody.appendChild(row);
    })

    let deleteButtons = document.querySelectorAll(".delete");
    let editButtons = document.querySelectorAll(".edit");

    edit_delete_listeners(deleteButtons, editButtons)
}

let edit_delete_listeners = (deleteButtons, editButtons) => {
    deleteButtons.forEach(button =>{
        let id = button.getAttribute("id")
        button.addEventListener("click", () => delete_app(id));
    });

    editButtons.forEach(button =>{
        let id = button.getAttribute("id")
        button.addEventListener("click", () => edit_app(id));
    });
}

let edit_app = (id) =>{

}

let delete_app = (id) =>{
     const isConfirmed = window.confirm("Are you sure you want to delete this application?\nThis action CANNOT be undone!");

    // Check if the user confirmed the deletion
    if (isConfirmed) {
        console.log(`Deleting application with ID: ${id}`);
    } else {
        // The user clicked 'Cancel' or closed the dialog
        console.log('Deletion canceled');
    }
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
