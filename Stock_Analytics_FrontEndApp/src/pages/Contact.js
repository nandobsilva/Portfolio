// ESTERNAL COMPONENT
import React from "react";
import NavBar from "../components/NavBar";

// INTERNAL COMPONENT
import Footer from "../components/Footer";

export default function Contact() {
  const onSubimit = () => {
    alert("Thank tou for your contact. We will get in touch soon.");
  };
  return (
    <React.Fragment>
      <div>
        {localStorage.getItem("token") === null && (
          <NavBar menu={"contactPublic"} />
        )}
        {localStorage.getItem("token") !== null && (
          <NavBar menu={"contactPrivate"} />
        )}
        <div className="row  mt-5 justify-content-center ">
          <div className="col-sm-6">
            <form>
              <div className="form-group">
                <h2 className="font">Get in touch</h2>
                <input
                  type="text"
                  className="form-control"
                  id="fullName"
                  placeholder="Full Name"
                />
              </div>
              <div className="form-group">
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  placeholder="Email Address"
                />
              </div>
              <div className="form-group">
                <textarea
                  className="form-control"
                  id="exampleFormControlTextarea1"
                  rows="3"
                ></textarea>
              </div>
              <button
                type="submit"
                className="btn btn-info btn-lg btn-block"
                onClick={onSubimit}
              >
                Submit
              </button>
            </form>
          </div>
        </div>
      </div>
      <div className="container fixed-bottom mt-4">
        <Footer />
      </div>
    </React.Fragment>
  );
}
