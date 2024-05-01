document.addEventListener('DOMContentLoaded', function() {
    const sentimentCells = document.querySelectorAll('.sentiment');
    
    sentimentCells.forEach(cell => {
        let sentimentValue = cell.innerText.trim();
        let emoji = '';
        switch(sentimentValue) {

            case '[5]':
                emoji = '😊';
                break;
            case '[4]':
                emoji = '😀';
                break;
            case '[3]':
                emoji = '🙂';
                break;
            case '[2]':
                emoji = '😐';
                break;
            case '[1]':
                emoji = '☹';
                break;
            default:
                emoji = '😑'; // Unknown sentiment
        }
        cell.innerText = emoji;
    });
});