// @TODO: Complete the following function that builds the metadata panel

// Use `d3.json` to fetch the metadata for a sample
  // Use d3 to select the panel with id of `#sample-metadata`

  // Use `.html("") to clear any existing metadata

  // Use `Object.entries` to add each key and value pair to the panel
  // Hint: Inside the loop, you will need to use d3 to append new
  // tags for each key-value in the metadata.

  // BONUS: Build the Gauge Chart
  // buildGauge(data.WFREQ);

  function buildMetadata(sample) {
    d3.json(`/metadata/${sample}`).then((data) => {
      var PANEL = d3.select("#sample-metadata");
      PANEL.html("");
      Object.entries(data).forEach(([key, value]) => {
        PANEL.append("h6").text(`${key}: ${value}`);
      });

      // BONUS: Build the Gauge Chart
      buildGauge(data.WFREQ);
    });
  }


function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(`/samples/${sample}`).then((data) => {
    var ids = data.otu_ids;
    var labels = data.otu_labels;
    var values = data.sample_values;


    // @TODO: Build a Bubble Chart using the sample data
    var LayoutBubble = {
      margin: { t: 0 },
      xaxis: { title: "Id's" }
      hovermode: "closest",
      };

      var DataBubble = [
      {
        x: ids,
        y: values,
        text: labels,
        mode: "markers",
        marker: {
          color: ids,
          size: values,
          }
      }
    ];

    Plotly.plot("bubble", DataBubble, LayoutBubble);

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).

    var pie_data = [
      {
        values: values.slice(0, 10),
        labels: ids.slice(0, 10),
        hovertext: labels.slice(0, 10),
        hoverinfo: "hovertext",
        type: "pie"
      }
    ];

    var pie_layout = {
      margin: { t: 0, l: 0 }
    };

    Plotly.plot("pie", pie_data, pie_layout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();