<?php 
	session_start();
?>
<!DOCTYPE html>
<html>
<head>
	<title>Flight Data</title>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
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
						echo '<form action="login.inc.php" method = "POST">
								<input type="text" name="email" placeholder="Email">
								<input type="password" name="pwd" placeholder="Password">
								<button type="submit" name="submit">Login</button>
							</form>
							<a href="signup.php">Sign Up</a>';
					}
				?>
			</div>
		</div>
	</nav>
</header>
<section class = "main-container">
	<div class = "main-wrapper">
		<h2>Signup</h2>
		<form class="signup-form" action="signup.inc.php" method="POST">
			<input type="text" name="username" placeholder="Username">
			<input type="text" name="email" placeholder="E-mail">
			<input type="password" name="pwd" placeholder="Password">
			<button type="submit" name="submit">Sign up</button>
		</form>
	</div>
	
</section>

</body>
</html>

