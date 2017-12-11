<html>
<head><title>Available Cities</title></head>
<body>
<?php
  if (!isset($_GET['direction'])) {
    echo "You need to specify a direction. Please <a href='index.php'>try again</a>.";
    die();
  }
  $direction = $_GET['direction'];
?>

<h1>Available Cities</h1>

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
    $st = $dbh->query("SELECT DISTINCT destination FROM trip WHERE NOT destination LIKE 'RDU' ORDER BY destination");
    if (($myrow = $st->fetch())) {
?>

<?php
  try {
     $st2 = $dbh->query("SELECT city FROM airport WHERE callsign IN (SELECT DISTINCT destination FROM trip WHERE NOT destination LIKE 'RDU') ORDER BY callsign");
//     $st2->execute(array($myrow[0]));
     $myrow2 = $st2->fetch();
  } catch (PDOException $e) {
     print "Error connecting to the database: " . $e->getMessage() . "<br/>";
     die();
  }
?>

<?php 
$action = "";
if ($direction){
  $action = "Departure";
}
else{
  $action = "Arrival";
}
?>

<form method="post" action="dates.php">
Select a city:<br/>
<?php
      do {
        // echo produces output HTML:
        echo "<input type='radio' name='destination' value='" . $action . "|" . $myrow[0] . "'/>";
        echo $myrow[0] . ", " . $myrow2[0] . "<br/>";
	$myrow2 = $st2->fetch();
      } while ($myrow = $st->fetch());
      // Below we will see the use of a "short open tag" that is equivalent
      // to echoing the enclosed expression.
?>
<?= $st->rowCount() ?> city/cities found in the database.<br/>
<input type="submit" value="GO!"/>
</form>
<?php
    } else {
      echo "There are no cities in the database.";
    }
  } catch (PDOException $e) {
    print "Database error: " . $e->getMessage() . "<br/>";
    die();
  }
?>
</body>
</html>

