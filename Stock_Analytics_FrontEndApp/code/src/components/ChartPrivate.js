// EXTERNAL COMPONENT
import React, { useState } from "react";
import { Line } from "react-chartjs-2";

export default function ChartPrivate(props) {
  const filtersList = [
    "Open price",
    "Highest price",
    "Lowes price",
    "Close price",
    "Volume traded",
  ];
  const { dataFiltered } = props;
  const [filter, setFilter] = useState(filtersList[4]);
  const titles = [
    "Open stock price by day",
    "Highest stock price by day",
    "Lowest stock price by day",
    "Close stock price by day",
    "Volumes traded by day (in million) ",
  ];

  const colors = [
    ["rgba(0,102,102,0.8)"],
    ["rgba(64,64,64,0.8)"],
    ["rgba(0,204,204,0.8)"],
    ["rgba(160,160,160,0.8)"],
    ["rgba(0,51,51,0.8)"],
    ["rgba(0,102,204,0.8)"],
    ["rgba(51,0,102,0.8)"],
    ["rgba(255,153,204,0.8)"],
    ["rgba(255,153,153,0.8)"],
  ];

  // Change the chart data according to the user selection
  const onSetFilter = (e) => {
    setFilter(e);
  };

  // Define the Companies  presented in the chart
  let companies = dataFiltered.map((item) => item.name);
  let uniqueCompanies = companies.filter((item, index) => {
    return companies.indexOf(item) === index;
  });
  uniqueCompanies.sort();

  // Get the dates from dataFiltered
  let dates = dataFiltered.map((item) => item.date);
  let uniqueDates = dates.filter((item, index) => {
    return dates.indexOf(item) === index;
  });

  // Filter the volumes by company
  function onFilter(company, filter) {
    let open = [];
    let high = [];
    let low = [];
    let close = [];
    let volumes = [];

    for (let i = 0; i < dataFiltered.length; i++) {
      if (company === dataFiltered[i].name) {
        open.push(dataFiltered[i].open.replace(/,/g, ""));
        high.push(dataFiltered[i].high.replace(/,/g, ""));
        low.push(dataFiltered[i].low.replace(/,/g, ""));
        close.push(dataFiltered[i].close.replace(/,/g, ""));
        volumes.push(dataFiltered[i].volumes.replace(/,/g, "") / 1000000);
      }
    }
    if (filter === filtersList[0]) return open;
    if (filter === filtersList[1]) return high;
    if (filter === filtersList[2]) return low;
    if (filter === filtersList[3]) return close;
    if (filter === filtersList[4]) return volumes;
  }

  // Define the data for the chart ( volumes, open, high, low or close)
  let objects = [];
  for (let i = 0; i < uniqueCompanies.length; i++) {
    let data = [];
    if (filter === filtersList[0])
      data = onFilter(uniqueCompanies[i], filtersList[0]);
    if (filter === filtersList[1])
      data = onFilter(uniqueCompanies[i], filtersList[1]);
    if (filter === filtersList[2])
      data = onFilter(uniqueCompanies[i], filtersList[2]);
    if (filter === filtersList[3])
      data = onFilter(uniqueCompanies[i], filtersList[3]);
    if (filter === filtersList[4])
      data = onFilter(uniqueCompanies[i], filtersList[4]);

    objects.push({
      label: uniqueCompanies[i],
      fill: false,
      borderColor: colors[i],
      data: data,
      borderWidth: 4,
    });
  }

  const chartAll_1 = {
    labels: uniqueDates,
    datasets: objects,
  };

  let title = "";
  if (filter === filtersList[0]) title = titles[0];
  if (filter === filtersList[1]) title = titles[1];
  if (filter === filtersList[2]) title = titles[2];
  if (filter === filtersList[3]) title = titles[3];
  if (filter === filtersList[4]) title = titles[4];

  return (
    <div>
      <div className="row">
        <div className="col"></div>
        <div className="col">
          <select
            className="custom-select "
            value={filter}
            onChange={(e) => onSetFilter(e.target.value)}
          >
            {filtersList.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </div>
        <div className="col"></div>
      </div>
      <Line
        data={chartAll_1}
        options={{
          responsive: true,
          title: {
            text: title,
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
  );
}
