let get_email_data = ()  =>{
    return fetch('/emails/render')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Handle the JSON data received from the server
            console.log(data);
            return data;
        })
        .catch(error => {
            console.error('Error fetching emails:', error);
        });
}

let fill_page = () => {
    get_email_data().then(data => {
        const table = document.getElementById("emailsTableBody");
        data.forEach(rowData => {
            // Create a new row element
            const row = document.createElement("tr");

            // Iterate over the rowData and append cells to the row
            rowData.forEach(cellData => {
                const cell = document.createElement("td");

                if(cellData === 0){
                    cellData = "Unsure";
                }else if(cellData === 1){
                    cellData = "Positive News"
                }else if(cellData === -1){
                    cellData = "Negative news"
                }

                cell.textContent = cellData;
                //console.log(cell);
                row.appendChild(cell);
            });

            // Append the row to the table
            table.appendChild(row);
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fill_page();
});