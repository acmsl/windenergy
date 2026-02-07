// Ejemplo: desencriptar un archivo de configuración en el frontend usando CryptoJS
// 1. Instala CryptoJS en tu proyecto (o usa CDN)
// <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>

// 2. Supón que el archivo mhn.enc contiene el JSON encriptado con AES y una clave compartida
// Ejemplo de uso:
async function fetchAndDecryptConfig(configFile, passphrase) {
  const res = await fetch(configFile);
  if (!res.ok) throw new Error('No se pudo cargar el archivo encriptado');
  const encryptedText = await res.text();
  // Desencriptar usando CryptoJS
  const decrypted = CryptoJS.AES.decrypt(encryptedText, passphrase);
  const jsonStr = decrypted.toString(CryptoJS.enc.Utf8);
  if (!jsonStr) throw new Error('Clave incorrecta o archivo corrupto');
  return JSON.parse(jsonStr);
}

// Ejemplo de llamada:
// fetchAndDecryptConfig('mhn.enc', 'mi_clave_secreta').then(config => {
//   console.log('Config desencriptado:', config);
// });

// Para encriptar el archivo en el backend o local:
// const CryptoJS = require('crypto-js');
// const fs = require('fs');
// const json = fs.readFileSync('mhn.json', 'utf8');
// const encrypted = CryptoJS.AES.encrypt(json, 'mi_clave_secreta').toString();
// fs.writeFileSync('mhn.enc', encrypted);
