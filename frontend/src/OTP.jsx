import React from 'react';

export default function OTP (props) {
    return (
        <div className="Auth-form-container">
          <form className="Auth-form">
            <div className="Auth-form-content">
              <h3 className="Auth-form-title">Verification</h3>
        
              <div className="form-group mt-3">
                <label>Enter OTP</label>
                <input
                  type="otp"
                  className="form-control mt-1"
                  placeholder="XXX-XXX"
                />
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