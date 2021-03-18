import React from "react";

export default function Loading() {
  return (
    <div className="d-flex justify-content-center">
      <div className="spinner-border text-info" role="status">
        <span className="sr-only">Loading...</span>
      </div>
      <h2 className="font1"> LOADING...</h2>
    </div>
  );
}
