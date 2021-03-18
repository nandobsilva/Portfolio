// EXTERNAL COMPONENTS
import { useState, useEffect } from "react";
import axios from "axios";

// INTERNAL COMPONENTS
export default function GetData() {
  //const url = "http://131.181.190.87:3000/stocks/symbols";
  const url = "http://localhost:3000/stocks/symbols";
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Get data from the database
  useEffect(() => {
    axios
      .get(url)
      .then((res) => res.data)
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((e) => {
        console.log(e.error + " " + e.message);
        setError(e);
        setLoading(false);
      });
  }, []);

  // Sort the industry data get from the database
  let industry = data.map((item) => item.industry);
  let uniqueIndustry = industry.filter((item, index) => {
    return industry.indexOf(item) === index;
  });
  uniqueIndustry.push("All industries");
  uniqueIndustry.sort();

  return {
    data,
    loading,
    error,
    uniqueIndustry,
  };
}
