<?php
  if (!isset($_POST['depart_time'])) {
    echo "You need to specify a departure time. Please <a href='index.php'>try again</a>.";
       die();
  }
  $temp = explode("|",$_POST['depart_time']);
  $date = $temp[0];
  $city1 = $temp[1];
  $city2 = $temp[2];

  // In production code, you might want to "cleanse" the $drinker string
  // to remove potential hacks before doing something with it (e.g.,
  // passing it to the DBMS).  That said, using prepared statements
  // (see below for details) can prevent SQL injection attack even if
  // $drinker contains potentially malicious character sequences.
?>

<html>
<head><title>Best Price: From <?= $city1 ?> to <?= $city2 ?></title></head>
<body>


<?php
   // including FusionCharts PHP wrapper for graphs
   include("fusioncharts.php");
?>

<html>
  <head>
  <title>FusionCharts XT - Column 2D Chart - Data from a database</title>
    <link  rel="stylesheet" type="text/css" href="css/style.css" />
    <!-- including FusionCharts core package JS files -->
    <script src="fusioncharts.js"></script>
    <script src="fusioncharts.charts.js"></script>
    <script src="fusioncharts.theme.zune.js"></script>
    <script src="fusioncharts.theme.ocean.js"></script>
    <script src="fusioncharts.theme.carbon.js"></script>
    <script src="fusioncharts.theme.fint.js"></script>
  </head>
</html>

<h1>Best Price: From <?= $city1 ?> to <?= $city2 ?> on <?= $date ?></h1>
<?php
  try {
    // Including connection info (including database password) from outside
    // the public HTML directory means it is not exposed by the web server,
    // so it is safer than putting it directly in php code:
    include("/etc/php/7.0/pdo-mine.php");
    $dbh = dbconnect();
  } catch (PDOException $e) {
    print "Error connecting to the database: " . $e->getMessage() . "<br/>";
    die();
  }
  try {
    // One could construct a parameterized query manually as follows,
    // but it is prone to SQL injection attack:
    // $st = $dbh->query("SELECT address FROM Drinker WHERE name='" . $drinker . "'");
    // A much safer method is to use prepared statements:
    $st = $dbh->prepare("SELECT price, booking_date FROM trip, flight, connectingflight where trip.origin = ? and trip.destination = ? and trip.id = connectingflight.trip_id and flight.id = connectingflight.flight_id and date(flight.depart_time) = ?");
    $st->execute(array($city1, $city2, $date));
    //printf("\n %d rows \n", $st->rowCount());


    if ($st->rowCount() == 0) {
      die('There are no flights that fit those in the database.');
    }


        // Forming the JSON chart data array needed for the graph plugin to process data 
  // creating an associative array to store the chart attributes        
      // The `$arrData` array holds the chart attributes and data
          $arrData = array(
              "chart" => array(
                  "caption" => "Minimum Ticket Price vs. Date",
                  "xAxisName" => "Date",
        			"yAxisName" => "Price (In USD)",
        			"numberPrefix" => "$",
                  "showValues" => "0",
                  "theme" => "ocean"
                )
            );

    $arrData["data"] = array();



    $myrow = $st->fetch();

    $min = 10000000000;

    $chartMin = 10000000000;
    $counter = 0;

    do{
      //printf("\n %s \n", $myrow[1]);
      if ($myrow[0] < $min){
        $min = $myrow[0];
        $date = $myrow[1];
      }

      if ($counter == 0) {
      	$thisDate = $myrow[1];
      }
      
      if ($thisDate == $myrow[1]) {
      	if($myrow[0] < $chartMin) {
      		$chartMin = $myrow[0];
      	}
      } else {
      	array_push($arrData["data"], array(
            "label" => $thisDate,
            "value" => $chartMin
            )
        );
        $thisDate = $myrow[1];
        $chartMin = $myrow[0];
      }
      $counter++;
		

    }
    while ($myrow = $st->fetch());

    echo "Best Price: ", $min;

    echo "<br/>\n";

    echo "Booking Date: ", $date;




    // iterating over each data and pushing it into $arrData array
    //printf("\n %d rows \n", $st->rowCount());

    // $myyrow = $st->fetch();
    // do {
    //   printf("\n %s \n", $myyrow[1]);  
        
    // }
    // while ($myyrow = $st->fetch());

  } catch (PDOException $e) {
    print "Database error: " . $e->getMessage() . "<br/>";
    die();
  }


    //echo sizeof($arrData);
    $jsonEncodedData = json_encode($arrData);


/*Create an object for the column chart using the FusionCharts PHP class constructor. Syntax for the constructor is ` FusionCharts("type of chart", "unique chart id", width of the chart, height of the chart, "div id to render the chart", "data format", "data source")`. Because we are using JSON data to render the chart, the data format will be `json`. The variable `$jsonEncodeData` holds all the JSON data for the chart, and will be passed as the value for the data source parameter of the constructor.*/

          $columnChart = new FusionCharts("column2d", "myFirstChart" , 600, 300, "chart-1", "json", $jsonEncodedData);

          // Render the chart
          $columnChart->render();


?>

<div id="chart-1"><!-- Fusion Charts will render here--></div>


<br><a href='index.php'>Start over</a>
</body>
</html>

