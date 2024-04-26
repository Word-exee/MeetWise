function addLocationInputs() {
    var numberOfFriends = document.getElementById('numFriends').value;
    var container = document.getElementById('locationInputs');
    container.innerHTML = ''; // Clear previous inputs

    for (var i = 0; i < numberOfFriends; i++) {
        var input = document.createElement('input');
        input.type = 'text';
        input.name = 'friendLocation' + i;
        input.placeholder = 'Location of Friend ' + (i + 1);
        input.required = true;
        container.appendChild(input);
        container.appendChild(document.createElement('br'));
    }
}
function buildTable(data){
    let array = data.split(', '); // Assumes space as a delimiter
    let data = [];
    for (let i = 1; i < lines.length; i=+9){
        let chunk = array.slice(i, i + 9);
        data.push(chunk);
    }
    const table = document.getElementById('nestedArrayTable');
    const thead = table.getElementsByTagName('thead')[0];
    const tbody = table.getElementsByTagName('tbody')[0];
    // Assuming all rows are of equal length, setting up the headers
    if (data.length > 0) {
        let headerRow = thead.insertRow();
        for (let i = 0; i < data[0].length; i++) {
            let th = document.createElement('th');
            th.textContent = `Column ${i + 1}`;
            headerRow.appendChild(th);
        }
    }
    // Adding data to the table body
    data.forEach(subArray => {
        let row = tbody.insertRow();
        subArray.forEach(value => {
            let cell = row.insertCell();
            cell.textContent = value;
        });
    });

    MeetupLocationRecommender.write(finalArray);
}