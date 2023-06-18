// destination selection
// maps api

import React from 'react';
import dotenv from 'dotenv';

export default async function UserDashboard (props) {
    const [loc, setLoc] = useState('');
    const [finalLoc, setFinalLoc] = useState('');
    let results = "";
    const lim = 5;
    
    const handleLocChange = (e) => {
        setLoc(e.target.value);
    }

    const handleFinalLocChange = (e) => {
        setFinalLocChange(e.target.value);
    }

    const autofillDestination = await fetch("https://www.mapquestapi.com/search/v3/prediction?key=${process.env.MAPQUEST_API_KEY}&limit=${lim}&collection=address&q=${loc}")
        .then(res => res.json())
        .then(data => results = data.results);

    
    
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
                <select value={selectedOption} onChange={handleOptionChange}>
                    <option value="">Select an option</option>
                    <option value="option1">Option 1</option>
                    <option value="option2">Option 2</option>
                    <option value="option3">Option 3</option>
                </select>
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
    const select = document.createElement("select");
    select.setAttribute("value", loc);
    select.setAttribute("onChange", handleFinalLocChange);

    for (let i = 0; i < UserDashboard.lim; i++) {
        const option = document.createElement("option");
        
    }
}