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
// Example array of arrays

