const ILovePDFApi = require('@ilovepdf/ilovepdf-nodejs');
const ILovePDFFile = require('@ilovepdf/ilovepdf-nodejs/ILovePDFFile');
const path = require('path');
const fs = require('fs');
const env = require('dotenv');

env.config();

const PUBLIC_KEY = process.env.PUBLIC_KEY;
const PRIVATE_KEY = process.env.PRIVATE_KEY;

const filePath = path.join(__dirname, 'files/ricavi_istituzionali.csv');
let totalDataRows = 0;
const rowsWithNoReceipt = [];

fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
        console.error('Errore nella lettura del file:', err);
        return;
    }

    const rows = data.trim().split('\n');
    const header = rows[0].split(',');
    totalDataRows = rows.length - 1;

    const receiptIndex = header.indexOf('receipt');

    for (let i = 1; i < rows.length; i++) {
        const cols = rows[i].split(',');

        const receipt = cols[receiptIndex]?.trim();
        if (receipt === 'NO') {
            rowsWithNoReceipt.push(i);
        }
    }
});

const instance = new ILovePDFApi(PUBLIC_KEY, PRIVATE_KEY);

const task = instance.newTask('merge');

async function mergePDFs(filePaths, outputFilePath) {
    try {
        const task = instance.newTask('merge');

        await task.start();

        for (const filePath of filePaths) {
            const file = new ILovePDFFile(filePath);
            await task.addFile(file);
        }

        await task.process();

        const data = await task.download();

        fs.writeFileSync(outputFilePath, data);
        console.log('File scaricato con successo in:', outputFilePath);
    } catch (error) {
        console.error('Errore durante l\'unione dei PDF:', error);
    }
}

const input_prima_nota = [
    'covers/cover_2.pdf',
    'tabs/tab_prima_nota.pdf'
];
const output_prima_nota = path.join(__dirname, 'finalized_docs', 'prima_nota_0325_sez22.pdf');

const input_estratto_conto = [
    'covers/cover_2.pdf',
    'tabs/tab_estratto_conto.pdf',
    'documents/estratto_conto.pdf',
    'documents/estratto_conto_paypal.pdf'
];
const output_estratto_conto = path.join(__dirname, 'finalized_docs', 'estratto_conto_0325_sez22.pdf');

const input_fatture_acquisto = [
    'covers/cover_2.pdf',
    'tabs/tab_fatture_acquisto.pdf'
];
const output_fatture_acquisto = path.join(__dirname, 'finalized_docs', 'fatture_acquisto_0325_sez22.pdf');

const input_ricavi_istituzionali = [
    'covers/cover_1.pdf',
    'tabs/tab_ricavi_istituzionali.pdf'
];
for (let i = 1; i <= 22; i++) {
    if (!rowsWithNoReceipt.includes(i)) {
        input_ricavi_istituzionali.push(`receipts/receipt_${i}.pdf`);
    }
}
const output_ricavi_istituzionali = path.join(__dirname, 'finalized_docs', 'ricavi_istituzionali_0325_sez22.pdf');

mergePDFs(input_prima_nota, output_prima_nota)
mergePDFs(input_estratto_conto, output_estratto_conto)
mergePDFs(input_fatture_acquisto, output_fatture_acquisto)
mergePDFs(input_ricavi_istituzionali, output_ricavi_istituzionali)