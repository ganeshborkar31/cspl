importScripts("https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging-compat.js");

// ✅ Replace with your Firebase config

firebase.initializeApp({
    apiKey: "AIzaSyAK2Nhhc4J2v64kWIhq4_d31pKdzMyHG3k",
    authDomain: "fire-base-push31.firebaseapp.com",
    projectId: "fire-base-push31",
    messagingSenderId: "665743733598",
    appId: "1:665743733598:web:39b249c8ede858f63c15cf",
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log("Background message received:", payload);
  const { title, body } = payload.notification;
  self.registration.showNotification(title, {
    body: body,
    icon: '/firebase-logo.png'
  });
});
