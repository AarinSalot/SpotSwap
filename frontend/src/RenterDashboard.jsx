// destination selection
// maps api

import React, { useState } from 'react'
// import 'dotenv/config'

export default function RenterDashboard (props) {
    const [loc, setLoc] = useState('');
    // const [finalLoc, setFinalLoc] = useState('');
    let results = "";
    const lim = 5;
    
    const handleLocChange = (e) => {
        setLoc(e.target.value);
        // autofillDestination();
        // createDropdown();
    }

    const handleFinalLocChange = (e) => {
        setFinalLoc(e.target.value);
    }

    return (
        <div className="Auth-form-container">
          <form className="Auth-form">
            <div className="Auth-form-content">
              <h3 className="Auth-form-title">Dashboard</h3>
        
              <div className="form-group mt-3">
                <label>Where do you want to go?</label>
                <input
                  type="otp"
                  value={loc}
                  className="form-control mt-1"
                  placeholder="Enter destination"
                  onChange={handleLocChange}
                />
                {/* <select id="dropdown" value={loc} onChange={handleFinalLocChange}>

                </select> */}
              </div>
              <div className="d-grid gap-2 mt-3">
                <button type="submit" className="btn btn-primary">
                  Submit
                </button>
              </div>
            </div>
          </form>
        </div>
      )
}

function createDropdown () {
    // for every value in results, add to dropdown
    const dropdown = document.getElementById("dropdown");
    
    for (let i = 0; i < UserDashboard.lim; i++) {
        const option = document.createElement("option");
        option.value = UserDashboard.results[i];
        dropdown.appendChild(option);
    }
}