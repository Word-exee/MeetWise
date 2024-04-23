document.getElementById('numFriends').addEventListener('change', function() {
    const number = this.value;
    const locationContainer = document.getElementById('friendsLocations');
    locationContainer.innerHTML = ''; // Clear previous inputs

    for (let i = 0; i < number; i++) {
        const inputGroup = document.createElement('div');
        inputGroup.className = 'input-group';
        const label = document.createElement('label');
        label.textContent = `Friend ${i + 1} Location:`;
        const input = document.createElement('input');
        input.type = 'text';
        input.name = `friend${i}Location`;
        input.required = true;
        
        inputGroup.appendChild(label);
        inputGroup.appendChild(input);
        locationContainer.appendChild(inputGroup);
    }
});

document.getElementById('locationForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Add here your AJAX call to Flask backend
});
