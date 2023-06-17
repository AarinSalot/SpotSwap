import React, { useState } from "react"
import ReactSwitch from 'react-switch';

export default function (props) {
  const [authMode, setAuthMode] = useState("signin");
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [isRenter, setIsRenter] = useState(false);

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin")
  }

  const handleNameChange = (e) => {
    setName(e.target.value);
  }

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  }

  const handlePhoneChange = (e) => {
    setPhone(e.target.value);
  }

  const handleIsRenterChange = val => {
    setIsRenter(val);
  }

  if (authMode === "signin") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form">
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Sign In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Enter email"
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="form-control mt-1"
                placeholder="Enter password"
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
            <p className="text-center mt-2">
              Forgot <a href="#">password?</a>
            </p>
          </div>
        </form>
      </div>
    )
  }

  console.log(name);
  console.log(isRenter);
  console.log(authMode);

  return (
    <div className="Auth-form-container">
      <form className="Auth-form">
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeAuthMode}>
              Sign In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>Full Name</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="e.g Jane Doe"
              onChange={handleNameChange}
            />
          </div>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="Email Address"
              onChange={handleEmailChange}
            />
          </div>
          <div className="form-group mt-3">
            <label>Phone number (XXX-XXX-XXXX)</label>
            <input
              type="phone"
              className="form-control mt-1"
              placeholder="Phone Number"
              onChange={handlePhoneChange}
            />
          </div>
          <div className="form-group mt-3">
            <label>Looking to rent out your spot?</label>
            <ReactSwitch
              checked={isRenter}
              onChange={handleIsRenterChange}
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
          <p className="text-center mt-2">
            Forgot <a href="#">password?</a>
          </p>
        </div>
      </form>
    </div>
  )
}