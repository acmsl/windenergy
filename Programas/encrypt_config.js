// Node.js script para encriptar mhn.json y crear mhn.enc
// Requiere instalar crypto-js: npm install crypto-js

const CryptoJS = require('crypto-js');
const fs = require('fs');

// Uso: node encrypt_config.js inputfile outputfile key
const args = process.argv.slice(2);
if (args.length < 3) {
	console.error('Uso: node encrypt_config.js <inputfile> <outputfile> <key>');
	process.exit(1);
}
const [inputFile, outputFile, passphrase] = args;

const json = fs.readFileSync(inputFile, 'utf8');
const encrypted = CryptoJS.AES.encrypt(json, passphrase).toString();
fs.writeFileSync(outputFile, encrypted);

console.log('Archivo encriptado creado:', outputFile);