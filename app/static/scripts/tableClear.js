let CTXD2 = 0;

function tableClearScriptFunction(info) {
    CTXD2++;

    const table = document.getElementById('TBL');

    if (CTXD2 === 7) {
        const rows = table.getElementsByTagName('tr');
        table.removeChild(rows[2]);
        CTXD2 = 6;
    };

    return CTXD2;
};