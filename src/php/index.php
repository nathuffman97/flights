<?php 
	session_start();
?>
<!DOCTYPE html>
<html>
<head>
	<title>Flight Data</title>
	<link rel="stylesheet" type="text/css" href="natStyle.css">
</head>

<body>

<section class = "main-container">
	<div class = "main-wrapper">
		<center><h1>Find When to Book Your Flight</h1></center>

		<p>
		<a href="cities.php?direction=<?= True ?>">Find a flight departing from RDU</a> <br>
		<a href="cities.php?direction=<?= False?>">Find a flight arriving at RDU</a>
		</p>
	</div>
</section>

</body>
</html>
