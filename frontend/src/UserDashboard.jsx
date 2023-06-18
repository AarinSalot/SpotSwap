// destination selection
// maps api

import React, { useState } from 'react'
// import 'dotenv/config'
import cors from 'cors';
import openai from 'openai';
import { Configuration, OpenAIApi } from "openai";
const configuration = new Configuration({
    organization: "org-tjIV1GRkqtPxOQkDXsPsm8J3",
    apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);
// const response = await openai.listEngines();

export default function UserDashboard (props) {
    const [loc, setLoc] = useState('');
    // const [finalLoc, setFinalLoc] = useState('');
    let results = "";
    const lim = 5;
    let lat = "";
    let lon = "";

    // console.log(lim);
    
    const handleLocChange = (e) => {
        setLoc(e.target.value);
        // autofillDestination();
        // createDropdown();
    }

    const handleFinalLocChange = (e) => {
        setFinalLoc(e.target.value);
    }

    // curl -X POST https://api.openai.com/v1/chat/completions \
    // -H "Content-Type: application/json" \
    // -H "Authorization: Bearer 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" \
    // -H "OpenAI-Organization: org-tjIV1GRkqtPxOQkDXsPsm8J3" \
    // -d '{
    //   "model": "gpt-3.5-turbo",
    //   "messages": [{"role": "user", "content": "Give me the latitude and longitude of this address: 2500 durant avenue, berkeley, ca 94704. Separate with a space."}]
    // }'
  

    // app.use(cors());
    // console.log(loc);
    // const API_KEY = "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";
    // const prompt = "Give me the latitude and longitude of this address: " + loc + ". Separate with a space.";
    // fetch('https://api.openai.com/v1/chat/completions', {
    //     method: 'POST',
    //     mode: 'cors',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'Authorization': `Bearer ${API_KEY}`,
    //         "OpenAI-Organization": "org-tjIV1GRkqtPxOQkDXsPsm8J3"
    //     },
    //     body: JSON.stringify({
    //         model: "gpt-3.5-turbo",
    //         messages: prompt,
    //         max_tokens: 50
    //     })
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         console.log(data.choices[0]);
    //         const latlon = data.choices[0].message.content.split(" ");
    //         lat = latlon[0];
    //         lon = latlon[1];
    //         console.log(lat);
    //         console.log(lon);
    //     })
    //     .catch(error => {
    //         // Handle any errors
    //         console.error(error);
    //     });

    // process.env.MAPQUEST_API_KEY
    // const autofillDestination = fetch(`https://www.mapquestapi.com/search/v3/prediction?key=` + "Xcf1BjBLN6l9W5jGyAzczPy4n0tkz5md" + "&limit=" + lim + "&collection=address&q=" + loc)
    //     .then(res => res.json())
    //     .then(data => results = data.results);

    // fetch(`https://www.mapquestapi.com/searchahead/v3/query?key=kVDBqxLbcgFv7OqbiZWc2OQwGC1ukAYj&q=${loc}`)
    //     .then(response => response.json())
    //     .then(data => {
    //         // Handle the response data here
    //         results = data;
    //     })
    //     .catch(error => {
    //         // Handle any errors here
    //         console.error(error);
    //     });
    
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