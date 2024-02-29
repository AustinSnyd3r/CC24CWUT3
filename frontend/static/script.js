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
                        <td><button value = "Edit" id=${app[0]} class="edit"></td>`;
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

let delete_app = (id) =>{
     const isConfirmed = window.confirm(`Are you sure you want to delete application: ${id}`);

    // Check if the user confirmed the deletion
    if (isConfirmed) {
        // Make an AJAX request to the backend
        fetch(`/applications/delete/${id}`, {
            method: 'DELETE',  // Assuming you are using DELETE method for deletion
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                console.log(`Deletion request for application ${id} successful`);
                fetch_applications();
            } else {
                console.log(`Deletion request for application ${id} failed`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
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
let addApplication = () => {
        let company = document.getElementById('company').value;
        let position = document.getElementById('position').value;
        let status = document.getElementById('status').value;

        fetch("/applications/add/" + company + "/" + position + "/" + status, {
            method: 'GET'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error adding application");
            }
            fetch_applications();
            return response.text();
        })
        .then(data => {
            alert(data); // Display the response from the server
        })
        .catch(error => {
            console.error("Error adding application:", error.message);
        });
    }

let edit_app = (id) =>{
    let table = document.getElementById("editTable")
    table.classList.remove("hide");
    let id_holder = document.getElementById("id_holder");
    id_holder.value = id;
    console.log(id);
}

let edit_submit = () =>{
    let table = document.getElementById("editTable");
    let company = document.getElementById("company_edit").value;
    let position = document.getElementById("position_edit").value;
    let status = document.getElementById("status_edit").value;
    let id = document.getElementById("id_holder").value;
    console.log(company);
    console.log(position);
    console.log(status);

    fetch(`/applications/edit/${company}/${position}/${status}/${id}`, {
            method: 'GET',  // Assuming you are using DELETE method for deletion
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                console.log(`Edit request for application ${id} successful`);
                alert("Application edited!");
                fetch_applications();
                table.classList.add("hide");
            } else {
                console.log(`Edit request for application ${id} failed`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}





document.addEventListener('DOMContentLoaded', function() {
    //load the applications on page load
    fetch_applications();
    let add = document.getElementById("addButton");
    add.addEventListener("click", addApplication)

    let editSubmit = document.getElementById("editButton");
    editSubmit.addEventListener("click", edit_submit)

});
