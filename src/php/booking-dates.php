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
    if ($st->rowCount() == 0) {
      die('There are no flights that fit those in the database.');
    }
    $myrow = $st->fetch();

    $min = 10000000000;
    do{
      if ($myrow[0] < $min){
        $min = $myrow[0];
        $date = $myrow[1];
      }
    }
    while ($myrow = $st->fetch());

    echo "Best Price: ", $min;

    echo "<br/>\n";

    echo "Booking Date: ", $date;

  } catch (PDOException $e) {
    print "Database error: " . $e->getMessage() . "<br/>";
    die();
  }
?>
<br><a href='index.php'>Start over</a>
</body>
</html>

