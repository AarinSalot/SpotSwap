// import React, { useState } from 'react';
// import "./Login.css";
// import "bootstrap/dist/css/bootstrap.min.css"


// const Login = () => {
//   const [name, setName] = useState('');
//   const [email, setEmail] = useState('');
//   const [phone, setPhone] = useState('');
//   const [isRenter, setIsRenter] = useState(false);

//   const handleNameChange = (event) => {
//     setName(event.target.value);
//   };

//   const handleEmailChange = (event) => {
//     setEmail(event.target.value);
//   };

//   const handlePhoneChange = (event) => {
//     setPhone(event.target.value);
//   };

//   const handleIsRenterChange = (event) => {
//     setIsRenter(event.target.value);
//   };

//   const handleLogin = () => {
//     console.log(name);
//     console.log(email);
//     console.log(phone);
//     console.log(isRenter);
//   };

//   return (
//     <div>
//       <h2>Login</h2>
//       <div>
//         <label htmlFor="name">Name:</label>
//         <input
//           type="text"
//           id="name"
//           value={name}
//           onChange={handleNameChange}
//         />
//       </div>
//       <div>
//         <label htmlFor="email">Email:</label>
//         <input
//           type="text"
//           id="email"
//           value={email}
//           onChange={handleEmailChange}
//         />
//       </div>
//       <div>
//         <label htmlFor="phone">Phone:</label>
//         <input
//           type="text"
//           id="phone"
//           value={phone}
//           onChange={handlePhoneChange}
//         />
//       </div>
//       <div>
//         <label htmlFor="isRenter">Renting out your spot?:</label>
//         <input
//           type="checkbox"
//           id="isRenter"
//           value={isRenter}
//           onChange={handleIsRenterChange}
//         />
//       </div>
//       <button onClick={handleLogin}>Login</button>
//     </div>
//   );
// };

// export default Login;




import "bootstrap/dist/css/bootstrap.min.css"
import "./Login.css"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Auth from "./Auth"

function Login() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/auth" element={<Auth />} />
      </Routes>
    </BrowserRouter>
  )
}

export default Login