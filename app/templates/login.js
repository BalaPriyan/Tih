import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js"; // Correct import for authentication

  // Your web app's Firebase configuration
  const firebaseConfig = {
    apiKey: "AIzaSyC00IrzoT1cuyyEsJRXeYdtumIu4byOL78",
    authDomain: "signup-for.firebaseapp.com",
    projectId: "signup-for",
    storageBucket: "signup-for.appspot.com",
    messagingSenderId: "793565065718",
    appId: "1:793565065718:web:da9ad3b16ec62bc24f57d7"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth();

window.login = function (e) {
  e.preventDefault();
  var email = document.getElementById("Email").value; // Get email value from input field
  var password = document.getElementById("password").value; // Get password value from input field

  signInWithEmailAndPassword(auth, email, password)
    .then(function (userCredential) {
      var user = userCredential.user;
      console.log(user.uid); // Output user UID to console
      alert("Logged in successfully");
    })
    .catch(function (err) {
      alert("Login error: " + err);
    });
};
