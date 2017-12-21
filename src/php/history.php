<html>
<head><title>Search History</title></head>
<body>

<header>
  <nav>
    <div class = "main-wrapper">
      <ul>
        <li><a href="index.php">Home</a></li>
      </ul>
      <div class="nav-login">
        <?php
          if (isset($_SESSION['u_id'])){
            echo '<form action = "logout.inc.php" method = "POST">
                <buttontype = "submit" name = "submit">Logout</button>
              </form>
              <a href="history.php">Search History</a>';
          } else{
            header("Location: /index.php?login=false")
            exit();
          }
        ?>
      </div>
    </div>
  </nav>
</header>

<h1>Search History</h1>

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
     $st = $dbh->prepare("SELECT * FROM trip WHERE id IN (SELECT tid FROM triptaker WHERE pid = ?");
     $st->execute($_SESSION['u_id']);
     if (($myrow = $st->fetch())) {
?>


Your past searches:<br/>
<?php
      do {
        // echo produces output HTML:
        echo $myrow[3] . ", " . $myrow[4] . ",". $myrow[1] . ",". $myrow[2]. "<br/>";
	$myrow2 = $st2->fetch();
      } while ($myrow = $st->fetch());
      // Below we will see the use of a "short open tag" that is equivalent
      // to echoing the enclosed expression.
?>



<?php
    } else {
          echo "No search history found.";
        }
  } catch (PDOException $e) {
     print "Database error: " . $e->getMessage() . "<br/>";
     die();
  }
?>


</body>
</html>

