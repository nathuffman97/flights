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
<head><title>Flight <?= $direction ?> Dates</title></head>
<h1>Flight <?= $direction ?> Dates</h1>

<?php
$direction = lcfirst($direction);
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
    if ($direction = "departure"){
	$st = $dbh->query("SELECT DISTINCT date(depart_time) FROM flight where depart='RDU' ORDER BY date(depart_time)");
    }
    else{
	 $st = $dbh->query("SELECT DISTINCT date(depart_time) FROM flight where arrive='RDU' ORDER BY date(depart_time)");
    }
    if (($myrow = $st->fetch())) {
?>
<form method="post" action="booking-dates.php">
Select a <?= $direction ?> date:<br/>
<?php
      do {
        // echo produces output HTML:
	if ($direction == "arrival"){
	   $ret = $myrow[0] . "|" . $city . "|" . "RDU";
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
<?= $st->rowCount() ?> date(s) found in the database.<br/>
<input type="submit" value="GO!"/>
</form>
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

