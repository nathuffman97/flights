<html>
<head>
  <title>Available Cities</title>
  <link rel="stylesheet" type="text/css" href="natStyle.css">
</head>

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
    include("pdo-mine.php");
    $dbh = dbconnect();
  } catch (PDOException $e) {
    print "Error connecting to the database: " . $e->getMessage() . "<br/>";
    die();
  }
  try {
    $st = $dbh->prepare("SELECT DISTINCT destination FROM trip WHERE NOT destination LIKE ? ORDER BY destination LIMIT 25");
    $st -> execute(array('RDU'));
    if (($myrow = $st->fetch())) {
?>

<?php
  try {
     $st2 =$dbh->prepare("SELECT city FROM airport WHERE callsign IN (SELECT DISTINCT destination FROM trip WHERE NOT destination LIKE ?) ORDER BY callsign LIMIT 25");
     $st2->execute(array('RDU'));
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

<div class="form">
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
<br><?= $st->rowCount() ?> city/cities found in the database.<br/>
<div class="button"> <input type="submit" value="GO!"/></div>
</form>
</div>
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

