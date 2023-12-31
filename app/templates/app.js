import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js"; // Correct import for authentication

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
const auth = getAuth();

window.signup = function (e) {
  e.preventDefault();
  var firstname = document.getElementById("firstname").value;
  var lastname = document.getElementById("lastname").value;
  var email = document.getElementById("Email").value;
  var password = document.getElementById("password").value;

  createUserWithEmailAndPassword(auth, email, password)
    .then(function (userCredential) {
      var user = userCredential.user;
      alert("Signed up successfully");
      // Here you can handle additional user information like names if you're using Firestore or other databases
    })
    .catch(function (err) {
      alert("Signup error: " + err);
    });
};
