$(document).ready(function () {
    const ctx = document.getElementById("myChart").getContext("2d");

    const myChart = new Chart(ctx, {
      type: "line",
      data: {
        datasets: [{ label: "Temperature",  }],
      },
      options: {
        borderWidth: 3,
        borderColor: ['rgba(255, 99, 132, 1)',],
      },
    });

    function addData(label, data) {
      myChart.data.labels.push(label);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
      });
      myChart.update();
    }
  
    function removeFirstData() {
      myChart.data.labels.splice(0, 1);
      myChart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
      });
    }
  
    const MAX_DATA_COUNT = 10;
    //connect to the socket server.
    //   var socket = io.connect("http://" + document.domain + ":" + location.port);
    var socket = io.connect();
  
    function myFunction()
    {
    if (myChart.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData();
    }
    setTimeout(function(){addData('2022', Math.floor(Math.random()*10))},3000);
    
    }
    
    setInterval(myFunction, 3000);
  });








