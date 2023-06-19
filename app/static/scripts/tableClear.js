function tableClearScriptFunction(count) {
    count++;

    const table = document.getElementById('TBL');

    if (count === 7) {
        const rows = table.getElementsByTagName('tr');
        table.removeChild(rows[2]);
        count = 6;
    };
    
    return count;
};