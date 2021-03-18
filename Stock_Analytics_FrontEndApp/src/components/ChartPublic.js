// EXTERNAL COMPONENT
import React, { useState } from "react";
import { Line, Bar } from "react-chartjs-2";

export default function ChartPublic(props) {
  const { data } = props;
  const [company, setCompany] = useState(data[0]);

  // Change the chart data according to the user selection
  const onSetCompany = (item) => {
    for (let i = 0; i < data.length; i++) {
      if (data[i].name === item) setCompany(data[i]);
    }
  };

  // Bar char for the volumes tradeb by the companies selected
  var companies = data.map((item) => item.name);
  var volumes = data.map((item) => item.volumes.replace(/,/g, "") / 1000000);
  const barChar = {
    labels: companies,
    datasets: [
      {
        label: "",
        data: volumes,
      },
    ],
  };

  // Line Chart of one company
  const chartData = {
    labels: ["Open", "High", "Low", "Close"],
    datasets: [
      {
        label: company.date,
        fill: true,
        borderColor: ["rgba(75,192,192,0.4)"],
        data: [
          company.open.replace(/,/g, ""),
          company.high.replace(/,/g, ""),
          company.low.replace(/,/g, ""),
          company.close.replace(/,/g, ""),
        ],
        backgroundColor: ["rgba(75,192,192,0.4)"],
        borderWidth: 4,
      },
    ],
  };

  return (
    <div>
      <div className="row">
        <div className="col pt-3">
          <br />
          <Bar
            data={barChar}
            options={{
              legend: { display: false },
              title: {
                display: true,
                text: "Volume traded by company (in million)",
              },
              scales: {
                yAxes: [
                  {
                    ticks: {
                      autoSkip: true,
                      maxTicksLimit: 10,
                      beginAtZero: true,
                    },
                    gridLines: { display: false },
                  },
                ],
                xAxes: [
                  {
                    gridLines: { display: false },
                  },
                ],
              },
            }}
          />
        </div>
        <div className="col">
          <div className="col-8">
            <select
              className="custom-select "
              value={company.name}
              onChange={(e) => onSetCompany(e.target.value)}
            >
              {data.map((item) => (
                <option key={item.symbol}>{item.name}</option>
              ))}
            </select>
          </div>

          <Line
            data={chartData}
            options={{
              responsive: true,
              title: {
                text: "Stock price variation: " + company.name,
                display: true,
              },
              scales: {
                yAxes: [
                  {
                    ticks: {
                      autoSkip: true,
                      maxTicksLimit: 10,
                      beginAtZero: false,
                    },
                    gridLines: { display: false },
                  },
                ],
                xAxes: [
                  {
                    gridLines: { display: false },
                  },
                ],
              },
            }}
          />
        </div>
      </div>
    </div>
  );
}
