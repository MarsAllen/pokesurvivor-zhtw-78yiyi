/* ============ firebase-config.js — conexión con tu proyecto de Firebase ============
 * Pega aquí la configuración de tu app web de Firebase (Consola de Firebase >
 * Configuración del proyecto > Tus apps > SDK setup and configuration > Config).
 * Los pasos completos están en docs/FIREBASE.md.
 *
 * Estos datos NO son secretos: Firebase los diseña para ir en la web. Lo que
 * protege las partidas son las reglas de Firestore (firestore.rules).
 *
 * Si se pone a null, el juego funciona en modo local (sólo en el navegador).
 */
// zh-TW fork 自己的 Firebase 專案（Spark 免費方案，2026-10-16 建立）。
// Firestore 在 asia-east1（台灣）、Realtime Database 在 asia-southeast1（新加坡）。
// 不要啟用 Identity Platform（按使用者計費），也不要部署 functions/（需要付費方案）。
G.FIREBASE_CONFIG = {
  apiKey: 'AIzaSyDI069kqQPkd6cUdTsoW-7IsPPHzZnajJ8',
  authDomain: 'pokesurvivor-zhtw-78yiyi.firebaseapp.com',
  projectId: 'pokesurvivor-zhtw-78yiyi',
  storageBucket: 'pokesurvivor-zhtw-78yiyi.firebasestorage.app',
  messagingSenderId: '852689799516',
  appId: '1:852689799516:web:633f28bdf4f0e3f66a9999',
  databaseURL: 'https://pokesurvivor-zhtw-78yiyi-default-rtdb.asia-southeast1.firebasedatabase.app'
};

/* Ejemplo de cómo debe quedar:
G.FIREBASE_CONFIG = {
  apiKey: 'AIza...',
  authDomain: 'tu-proyecto.firebaseapp.com',
  projectId: 'tu-proyecto',
  storageBucket: 'tu-proyecto.firebasestorage.app',
  messagingSenderId: '1234567890',
  appId: '1:1234567890:web:abc123'
};
*/
