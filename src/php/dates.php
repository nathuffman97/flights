<?php
  if (!isset($_POST['destination'])) {
    echo "You need to specify a city. Please <a href='index.php'>try again</a>.";
    die();
  }

  $temp = explode("|", $_POST['destination']);

  $direction = $temp[0];
  $city = $temp[1];
?>
<html>
<head>
  <title>Flight <?= $direction ?> Dates</title>
  <link rel="stylesheet" type="text/css" href="natStyle.css">
</head>
<body>

<h1>Flight <?= $direction ?> Dates</h1>

<?php
$direction = lcfirst($direction);
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
    if ($direction = "departure"){
	  $st = $dbh->prepare("SELECT DISTINCT date(depart_time) FROM flight where depart=? AND date(depart_time) > NOW() ORDER BY date(depart_time) LIMIT 25");
    $st->execute(array('RDU'));
    }
    else{
	 $st = $dbh->prepare("SELECT DISTINCT date(depart_time) FROM flight where arrive=? AND date(depart_time) > NOW() ORDER BY date(depart_time) LIMIT 25");
   $st = $dbh->execute(array('RDU'));
    }
    if (($myrow = $st->fetch())) {
?>
<div class="form">
<form method="post" action="booking-dates.php">
Select a <?= $direction ?> date:<br/>
<?php
      do {
        // echo produces output HTML:
	if ($direction == "arrival"){
           $ret =  $myrow[0] . "|" . $city . "|" . "RDU";
	}
	else{
	   $ret = $myrow[0] . "|" . "RDU" . "|" . $city;
	}
        echo "<input type='radio' name='depart_time' value='". $ret . "'/>";
        echo $myrow[0] . "<br/>";
      } while ($myrow = $st->fetch());
      // Below we will see the use of a "short open tag" that is equivalent
      // to echoing the enclosed expression.
?>
<br><?= $st->rowCount() ?> date(s) found in the database.<br/>
<div class="button"><input type="submit" value="GO!"/></div>
</form>
</div>
<?php
    } else {
      echo "There are no dates in the database.";
    }
  } catch (PDOException $e) {
    print "Database error: " . $e->getMessage() . "<br/>";
    die();
  }
?>
</body>
</html>

